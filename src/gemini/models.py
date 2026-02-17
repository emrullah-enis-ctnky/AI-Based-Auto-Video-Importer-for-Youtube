from dataclasses import dataclass, field
from typing import List

@dataclass
class VideoMetadata:
    """
    Structured metadata for a YouTube video.
    """
    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "tags": self.tags
        }
