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
    """Execute the full RAG pipeline for a query."""
    from app.rag.retriever import search_projects
    from app.rag.prompts import ASK_AI_PROMPT
    from langchain_core.runnables import RunnableSequence
    
    # 1. Retrieve context
    matches = await search_projects(db, query, limit=5)
    
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
            "relevance_score": score
        })
        
    context_str = "\n\n".join(context_parts)
    
    # 2. Setup LLM Chain
    llm = get_llm(streaming=False)
    chain = ASK_AI_PROMPT | llm
    
    # 3. Execute
    result = await chain.ainvoke({"context": context_str, "query": query})
    
    return result.content, sources
