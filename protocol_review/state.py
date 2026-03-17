from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class ReviewItem(TypedDict):
    compliant: bool
    score: int
    issues: List[str]
    suggestions: List[str]


class ProtocolReviewState(TypedDict):
    protocol_name: str
    identifiers: List[str]
    description: str
    reviews: Dict[str, ReviewItem]
    summary: Dict[str, Any]
