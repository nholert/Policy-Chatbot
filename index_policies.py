from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
import os

# Load documents from a folder
def extract_text_from_pdfs(directory):
    documents = []
    reader = SimpleDirectoryReader(input_dir=directory)
    docs = reader.load_data()
    for doc in docs:
        documents.append(doc)
    return documents

# Set the directory containing policy documents
docs = extract_text_from_pdfs("policy_documents")

# Use OpenAI embeddings (or swap with a local model)
embedding_service = OpenAIEmbedding()

# Create an index for searching
index = VectorStoreIndex.from_documents(docs, embed_model=embedding_service)

# Save index to disk
index.storage_context.persist("policy_index")

print("Indexing complete! The policy chatbot is ready.")
