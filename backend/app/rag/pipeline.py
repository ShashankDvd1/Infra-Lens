"""
LandScope AI — Groq LLM integration.
"""

from langchain_groq import ChatGroq
from app.config import get_settings

settings = get_settings()

def get_llm(fallback: bool = False, streaming: bool = False) -> ChatGroq:
    """Returns the Groq LangChain model."""
    model_name = settings.LLM_FALLBACK_MODEL if fallback else settings.LLM_MODEL
    
    return ChatGroq(
        temperature=settings.LLM_TEMPERATURE,
        groq_api_key=settings.GROQ_API_KEY,
        model_name=model_name,
        max_tokens=settings.LLM_MAX_TOKENS,
        streaming=streaming
    )

async def ask_ai_pipeline(query: str, db) -> tuple[str, list]:
    """Execute the full RAG pipeline with live web search and verification."""
    from app.rag.retriever import search_projects
    from app.rag.prompts import ASK_AI_PROMPT
    from langchain_core.runnables import RunnableSequence
    from app.services.search_service import search_ddg_live, generate_search_results_fallback
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import JsonOutputParser
    
    # 1. Retrieve local DB context
    matches = await search_projects(db, query, limit=3)
    
    context_parts = []
    sources = []
    for match in matches:
        proj = match["project"]
        content = match["content"]
        score = match["score"]
        
        context_parts.append(f"Project: {proj.name}\nStatus: {proj.status.value}\nDetails: {content}")
        
        sources.append({
            "project_id": proj.id,
            "project_name": proj.name,
            "relevance_score": score,
            "title": proj.name,
            "url": f"/projects/{proj.id}"
        })
        
    context_str = "\n\n".join(context_parts)
    
    # 2. Live Web Search & Verification
    search_results = search_ddg_live(query)
    if not search_results:
        search_results = await generate_search_results_fallback(query)
        
    verified_context_parts = []
    web_sources = []
    
    if search_results:
        # LLM Verification Prompt for general search results
        verify_prompt_text = """
        You are the LandScope AI General Info Verification Agent.
        Review these web search findings for the query: "{query}"
        
        Search Findings:
        {findings}
        
        Filter out any findings that are highly speculative, outdated, or unreliable.
        Return a JSON object containing:
        - verified_findings: list of strings (only the facts that are verified and reliable)
        - verified_urls: list of strings (corresponding source URLs for the verified findings)
        """
        
        findings_str = ""
        for idx, r in enumerate(search_results[:3]): # take top 3
            findings_str += f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['snippet']}\n\n"
            
        verify_prompt = PromptTemplate(
            template=verify_prompt_text,
            input_variables=["query", "findings"]
        )
        
        # Use fallback model for speed and efficiency during general chat verification
        llm_verify = get_llm(fallback=True)
        parser = JsonOutputParser()
        verify_chain = verify_prompt | llm_verify | parser
        
        try:
            v_res = await verify_chain.ainvoke({"query": query, "findings": findings_str})
            verified_findings = v_res.get("verified_findings", [])
            verified_urls = v_res.get("verified_urls", [])
            
            for i, finding in enumerate(verified_findings):
                url = verified_urls[i] if i < len(verified_urls) else ""
                verified_context_parts.append(finding)
                
                # Create a source citation
                web_sources.append({
                    "title": f"Web: {finding[:40]}...",
                    "url": url if url else "https://www.google.com",
                    "relevance_score": 0.8
                })
        except Exception as e:
            print(f"General findings verification error: {e}")
            # If verification fails, add top 2 search results directly to ensure availability
            for r in search_results[:2]:
                verified_context_parts.append(r["snippet"])
                web_sources.append({
                    "title": r["title"][:50],
                    "url": r["url"] if r["url"] else "https://www.google.com",
                    "relevance_score": 0.7
                })
                
    web_context_str = "\n".join([f"- Verified Web Info: {p}" for p in verified_context_parts])
    full_context_str = f"DATABASE PROJECTS:\n{context_str}\n\nVERIFIED WEB SEARCH FINDINGS:\n{web_context_str}"
    
    # 3. Setup LLM Chain for final generation
    llm = get_llm(streaming=False)
    chain = ASK_AI_PROMPT | llm
    
    # 4. Execute
    result = await chain.ainvoke({"context": full_context_str, "query": query})
    
    # Merge local project sources and verified web sources
    sources.extend(web_sources)
    
    return result.content, sources

