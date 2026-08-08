import json
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.core.logging import logger

def create_persona_graph(post_generator_fn, memory_engine_fn):
    """
    Creates an autonomous LangGraph StateGraph orchestration pipeline.
    Nodes:
    1. memory_check -> 2. editorial_gate -> 3. persona_generation -> 4. memory_persist
    """
    workflow = StateGraph(AgentState)

    def memory_check_step(state: AgentState) -> AgentState:
        logger.info(f"LangGraph [Node: memory_check] checking memory for topic: {state.get('topic', {}).get('title', '')[:40]}")
        context = memory_engine_fn().get_full_persona_context()
        state["memory_context"] = context
        return state

    def editorial_gate_step(state: AgentState) -> AgentState:
        decision = state.get("editorial_eval", {}).get("decision", "REJECT")
        logger.info(f"LangGraph [Node: editorial_gate] decision={decision}")
        if decision != "PUBLISH":
            state["status"] = "REJECTED"
            state["error"] = "Topic failed editorial scoring threshold."
        else:
            state["status"] = "APPROVED"
        return state

    def persona_generation_step(state: AgentState) -> AgentState:
        if state.get("status") == "REJECTED":
            return state

        logger.info("LangGraph [Node: persona_generation] generating LinkedIn post in Ada's voice...")
        post_data = post_generator_fn(state["topic"], state["editorial_eval"])
        state.update(post_data)
        state["status"] = "GENERATED"
        return state

    def memory_persist_step(state: AgentState) -> AgentState:
        if state.get("status") == "GENERATED":
            logger.info("LangGraph [Node: memory_persist] post generated successfully.")
            state["status"] = "COMPLETED"
        return state

    def should_continue(state: AgentState) -> str:
        if state.get("status") == "REJECTED":
            return "end"
        return "continue"

    workflow.add_node("memory_check", memory_check_step)
    workflow.add_node("editorial_gate", editorial_gate_step)
    workflow.add_node("persona_generation", persona_generation_step)
    workflow.add_node("memory_persist", memory_persist_step)

    workflow.set_entry_point("memory_check")
    workflow.add_edge("memory_check", "editorial_gate")
    
    workflow.add_conditional_edges(
        "editorial_gate",
        should_continue,
        {
            "continue": "persona_generation",
            "end": END
        }
    )
    workflow.add_edge("persona_generation", "memory_persist")
    workflow.add_edge("memory_persist", END)

    return workflow.compile()
