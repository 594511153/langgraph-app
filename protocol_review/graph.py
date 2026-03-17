from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from .skills import (
    build_summary,
    identifier_naming_skill,
    name_naming_skill,
    protocol_description_skill,
)
from .state import ProtocolReviewState


def build_protocol_review_graph():
    workflow = StateGraph(ProtocolReviewState)

    workflow.add_node("name_naming_review", name_naming_skill)
    workflow.add_node("identifier_naming_review", identifier_naming_skill)
    workflow.add_node("protocol_description_review", protocol_description_skill)
    workflow.add_node("build_summary", build_summary)

    workflow.add_edge(START, "name_naming_review")
    workflow.add_edge("name_naming_review", "identifier_naming_review")
    workflow.add_edge("identifier_naming_review", "protocol_description_review")
    workflow.add_edge("protocol_description_review", "build_summary")
    workflow.add_edge("build_summary", END)

    return workflow.compile()


def review_protocol(protocol_name: str, identifiers: list[str], description: str):
    graph = build_protocol_review_graph()
    initial_state: ProtocolReviewState = {
        "protocol_name": protocol_name,
        "identifiers": identifiers,
        "description": description,
        "reviews": {},
        "summary": {},
    }
    return graph.invoke(initial_state)
