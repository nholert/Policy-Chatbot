from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.query_engine import RetrieverQueryEngine

# Load the stored index
storage_context = StorageContext.from_defaults(persist_dir="policy_index")
index = load_index_from_storage(storage_context)

# Set up the query engine
retriever = index.as_retriever(similarity_top_k=3)
query_engine = RetrieverQueryEngine(retriever)

def ask_policy_bot(question):
    """Retrieve policy information based on a user's question."""
    response = query_engine.query(question)
    return response.response

# Example query
if __name__ == "__main__":
    query = input("Ask a question about college policies: ")
    answer = ask_policy_bot(query)
    print("\nAnswer:", answer)
