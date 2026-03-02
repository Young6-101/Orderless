from langchain_ollama import ChatOllama

def get_llm(model: str = "llama3", temperature: float = 0.7):
    """
    Initialize and return the LLM client.
    
    Args:
        model: The Ollama model name to use
        temperature: Controls randomness in generation (0.0 = deterministic, 1.0 = creative)
    
    Returns:
        ChatOllama: Configured LLM client
    """
    return ChatOllama(model=model, temperature=temperature)
