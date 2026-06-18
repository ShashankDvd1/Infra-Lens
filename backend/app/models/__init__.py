from .project import Project, Source, Area, AISummary, GrowthIndicator, ProjectType, ProjectStatus, ProjectEmbedding, SourceEmbedding, AreaEmbedding
from .user import User, SavedOpportunity

# Re-export models for easier importing
__all__ = [
    "Project",
    "Source",
    "Area",
    "AISummary",
    "GrowthIndicator",
    "ProjectType",
    "ProjectStatus",
    "ProjectEmbedding",
    "SourceEmbedding",
    "AreaEmbedding",
    "User",
    "SavedOpportunity"
]
