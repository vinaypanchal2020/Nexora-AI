def prompt_builder(query: str, relevant_chunks: list[str]) -> str:
    
    context = "\n\n".join(relevant_chunks)
    
    prompt = f"""
    You are an AI Assistant answering questions based on the provided document context.
    
    Use the context below to answer the user questions.
    If the answer is not present in the context, say that you could not find the answer in the provided document. 
    
    Context:
    {context}
    
    User Question:
    {query}
    
    Answer:
    """
    
    return prompt