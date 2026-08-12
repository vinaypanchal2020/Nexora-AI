from fastapi import UploadFile
from app.rag.document_processor import process_document
from app.rag.chunker import chunk_text
from app.rag.text_cleaner import clean_text
from app.rag.embedding import create_embeddings
from app.rag.vector_db import store_embeddings
from app.rag.retriever import retrieve_chunks
from app.rag.prompt_builder import prompt_builder
from app.rag.llm import generate_response

async def general_chat(message: str, history=None):
    response = await generate_response(message, history=history)
    return {
        "mode": "General Chat",
        "response": response
    }

async def rag_chat(message: str, file: UploadFile, history=None):
    text = await process_document(file)
    text = clean_text(text)
    chunks = chunk_text(text)
    embeddings = create_embeddings(chunks)
    store_embeddings(chunks, embeddings)
    relevant_chunks = retrieve_chunks(message)
    prompt = prompt_builder(message, relevant_chunks)
    response = await generate_response(prompt, history=history)
    return {
        "mode": "RAG",
        "message": message,
        "response": response,
        "sources": relevant_chunks
    }