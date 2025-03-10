from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load text data
with open("course_data.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents([raw_text])

# Use a free local embedding model instead of OpenAI
model_name = "all-MiniLM-L6-v2"  # Small, fast model
embedding_model = HuggingFaceEmbeddings(model_name=model_name)

# Create FAISS vector store
vector_store = FAISS.from_documents(docs, embedding_model)

# Save vector store
vector_store.save_local("faiss_index")

print("✅ Vector database created and stored in faiss_index/")
