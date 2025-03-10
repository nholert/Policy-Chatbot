from flask import Flask, request, jsonify, render_template
import openai
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

app = Flask(__name__)

# Load or create the index from private submodule documents
DATA_DIR = "policy_documents"
INDEX_DIR = "policy_index"

# Check if the index already exists
if os.path.exists(INDEX_DIR):
    storage_context = StorageContext.from_defaults(persist_dir=INDEX_DIR)
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=INDEX_DIR)

query_engine = index.as_query_engine()

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# API to handle user queries
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("question")
    if not user_input:
        return jsonify({"error": "No question provided"}), 400

    response = query_engine.query(user_input)
    return jsonify({"answer": response.response})

if __name__ == "__main__":
    app.run(debug=True)