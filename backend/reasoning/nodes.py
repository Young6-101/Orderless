from backend.rag_engine.vector_store import InspiraVault
from backend.reasoning.state import GraphState
from backend.reasoning.model_client import get_llm
from backend.file_processor.image_handler import ImageDescriber
from langchain_core.prompts import ChatPromptTemplate

def retrieve_node(state: GraphState):
    """
    Node to retrieve relevant fragments from the vector store.
    
    This node:
    1. Searches for relevant text chunks based on the question
    2. Searches for relevant images based on the question
    3. Uses moondream to describe the images
    4. Combines text and image descriptions into context for the LLM
    
    Args:
        state: Current graph state containing the question
        
    Returns:
        dict: Updated state with context field populated
    """
    print("--- [AGENT] Retrieving Relevant Fragments ---")
    
    vault = InspiraVault()

    # Get relevant text chunks
    text_chunks = vault.search_clarity(state['question'])

    # Search for relevant images using the text query
    image_paths = vault.search_vision(state['question'])

    # Generate descriptions for retrieved images using moondream
    combined_context = text_chunks.copy()
    if image_paths:
        print(f"--- [AGENT] Analyzing {len(image_paths)} design samples with moondream ---")
        describer = ImageDescriber()
        
        # Use pattern analysis for design insights
        pattern_analysis = describer.analyze_design_pattern(image_paths)
        combined_context.append(f"\n--- Design Pattern Analysis ---\n{pattern_analysis}\n")

    return {"context": combined_context}

def generate_node(state: GraphState):
    """
    Node to synthesize inspiration from retrieved fragments.
    
    This node:
    1. Takes the retrieved context
    2. Uses an LLM to generate a creative career inspiration
    3. Returns the generated answer
    
    Args:
        state: Current graph state containing question and context
        
    Returns:
        dict: Updated state with answer field populated
    """
    print("--- [AGENT] Synthesizing Inspiration with LLM ---")
    
    # Get the LLM client
    llm = get_llm()
    
    # Create a prompt that injects the context
    prompt = ChatPromptTemplate.from_template("""
    You are 'Inspira', an AI design inspiration analyst.
    
    The user has uploaded design samples they like. Your task:
    1. Analyze the common patterns across all samples (color schemes, layouts, styles)
    2. Identify the user's underlying aesthetic preferences
    3. Provide concrete design recommendations based on these patterns
    
    Design Samples Analysis:
    {context}
    
    User's Question: {question}
    
    Design Insights & Recommendations:
    """)
    
    # Chain: Prompt -> LLM
    chain = prompt | llm
    response = chain.invoke({"context": state['context'], "question": state['question']})
    
    return {"answer": response.content}
