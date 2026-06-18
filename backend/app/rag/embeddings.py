"""
LandScope AI — RAG Embeddings Service.
Uses sentence-transformers to generate embeddings locally.
"""

from sentence_transformers import SentenceTransformer
import torch
from typing import List

from app.config import get_settings

settings = get_settings()

class EmbeddingService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._init_model()
        return cls._instance
        
    def _init_model(self):
        print(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL, device=device)
        print(f"Model loaded on {device}")
        
    def embed_text(self, text: str) -> List[float]:
        """Embed a single string."""
        return self.model.encode(text, normalize_embeddings=True).tolist()
        
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of strings."""
        return self.model.encode(texts, normalize_embeddings=True).tolist()

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

async def generate_all_embeddings():
    from app.db.session import async_session
    from sqlalchemy import select, delete
    from app.models import Project, Source, Area, ProjectEmbedding, SourceEmbedding, AreaEmbedding
    
    service = get_embedding_service()
    
    async with async_session() as session:
        print("Clearing old embeddings...")
        await session.execute(delete(ProjectEmbedding))
        await session.execute(delete(SourceEmbedding))
        await session.execute(delete(AreaEmbedding))
        
        print("Generating embeddings for Projects...")
        projects = (await session.execute(select(Project))).scalars().all()
        for p in projects:
            # Simple embedding of name + description
            text = f"{p.name}. {p.description or ''}"
            emb = service.embed_text(text)
            session.add(ProjectEmbedding(project_id=p.id, content=text, embedding=emb))
        
        print("Generating embeddings for Sources...")
        sources = (await session.execute(select(Source))).scalars().all()
        for s in sources:
            text = f"{s.title}. {s.content_text or ''}"
            emb = service.embed_text(text)
            session.add(SourceEmbedding(source_id=s.id, content=text, embedding=emb))
            
        print("Generating embeddings for Areas...")
        areas = (await session.execute(select(Area))).scalars().all()
        for a in areas:
            text = f"{a.name}. {a.description or ''}"
            emb = service.embed_text(text)
            session.add(AreaEmbedding(area_id=a.id, content=text, embedding=emb))
            
        await session.commit()
        print("All embeddings generated and saved!")

if __name__ == "__main__":
    import asyncio
    import sys
    
    if "--generate-all" in sys.argv:
        asyncio.run(generate_all_embeddings())
