from flask import Flask, request, jsonify, render_template
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
import json
import warnings

warnings.simplefilter("ignore", FutureWarning)

# Initialize Flask App
app = Flask(__name__, template_folder="templates", static_folder="static")

# Load environment variables
load_dotenv()
huggingface_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Load and Process Course Data from JSON
def load_course_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

course_data = load_course_data("course_data.json")

# Convert JSON data into text format for embedding
def format_course_data(course_data):
    formatted_text = ""
    for category, courses in course_data.items():
        formatted_text += f"{category.replace('_', ' ')}:\n"
        for course in courses:
            formatted_text += (
                f"- {course['Course_Name']} | Price: ${course['Price_per_Session']} | Lessons: {course['Lessons']}\n"
            )
    return formatted_text

course_text = format_course_data(course_data)

# Split Text into Chunks
def chunk_text(text, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)

text_chunks = chunk_text(course_text)

# Embed Text Chunks
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Create FAISS Vector Store
vector_store = FAISS.from_texts(text_chunks, embedding_model)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# Initialize Falcon LLM
llm = HuggingFaceEndpoint(
    repo_id="tiiuae/falcon-7b-instruct",
    huggingfacehub_api_token=huggingface_api_token,
    max_new_tokens=512,
    temperature=0.2
)

# Conversation Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

# Initialize Conversational Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

# Generate Response
def generate_response(user_message):
    greetings = ["hello", "hi", "hey"]
    if user_message.lower() in greetings:
        return "Hello! How can I assist you today?"

    response = qa_chain.invoke({"question": user_message, "chat_history": []})
    answer = response.get("answer", "I'm sorry, but I couldn't retrieve a proper answer from the course data.")

    return answer  

# Route for Web Chat Interface
@app.route("/")
def home():
    return render_template("index.html")

# Flask API Route for Chatbot
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    response_text = generate_response(user_message)
    return jsonify({"response": response_text})

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
