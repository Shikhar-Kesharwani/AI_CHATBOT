"""
Route identifier model.
"""

from pydantic import BaseModel, Field
from typing import Literal


class RouteIdentifier(BaseModel):
    """Model for routing queries to appropriate nodes."""

    route: Literal['index', 'search', 'general'] = Field(
        ...,
        description="The route to send the query to. Must be 'index' for document retrieval, 'search' for web search, or 'general' for general conversational LLM."
    )
