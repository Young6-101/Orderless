from typing import TypedDict

class GraphState(TypedDict):
    """
    Represents the state of the reasoning graph.
    
    Attributes:
        question: The user's input question
        context: Retrieved fragments from the vector store
        answer: The final generated answer from the LLM
    """
    question: str
    context: list[str]
    answer: str
