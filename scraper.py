from langchain.document_loaders import UnstructuredURLLoader

# Define the URL
urls = ["https://brainlox.com/courses/category/technical"]

# Load and extract data
loader = UnstructuredURLLoader(urls=urls)
documents = loader.load()

# Save extracted text to a file
with open("course_data.txt", "w", encoding="utf-8") as f:
    f.write(documents[0].page_content)

print("✅ Data scraped and saved to course_data.txt")
