from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from backend.rag_engine.vector_store import InspiraVault
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

class GraphState(TypedDict):
    question: str
    context: list[str]
    answer: str

# Initialize the "Brain"
llm = ChatOllama(model="llama3", temperature=0.7)

def retrieve_node(state: GraphState):
    """
    Node to retrieve relevant fragments from the vector store.
    """
    print("--- [AGENT] Retrieving Relevant Fragments ---")
    
    vault = InspiraVault()

    relevant_chunks = vault.search_clarity(state['question'])

    return {"context": relevant_chunks}

def generate_node(state: GraphState):
    """
    Node to synthesize inspiration from retrieved fragments.
    """
    print("--- [AGENT] Synthesizing Inspiration with LLM ---")
    
    # Create a prompt that injects the context
    prompt = ChatPromptTemplate.from_template("""
    You are 'Inspira', a creative AI career coach. 
    Using the retrieved fragments from the user's background below, 
    provide a unique insight or a career inspiration suggestion.
    
    Context: {context}
    Question: {question}
    
    Inspiration:
    """)
    
    # Chain: Prompt -> LLM
    chain = prompt | llm
    response = chain.invoke({"context": state['context'], "question": state['question']})
    
    return {"answer": response.content}

# Update the Workflow
workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)
workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate") # Retrieve -> Generate
workflow.add_edge("generate", END)        # Generate -> End

app = workflow.compile()