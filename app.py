from flask import Flask, request, jsonify, render_template_string
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.query_engine import RetrieverQueryEngine
import os

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def home():
    """Simple HTML interface for asking questions."""
    if request.method == "POST":
        question = request.form["question"]
        answer = ask_policy_bot(question)
        return render_template_string("""
            <h2>Answer:</h2>
            <p>{{ answer }}</p>
            <a href='/'>Ask another question</a>
        """, answer=answer)

    return render_template_string("""
        <form method="post">
            <label>Ask a question about college policies:</label><br>
            <input type="text" name="question" required><br><br>
            <input type="submit" value="Ask">
        </form>
    """)

@app.route("/ask", methods=["POST"])
def ask():
    """API endpoint for asking questions."""
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = ask_policy_bot(question)
    return jsonify({"question": question, "answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
