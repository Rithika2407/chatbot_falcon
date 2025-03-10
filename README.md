
# Falcon Chatbot

This is a Flask-based chatbot that leverages LangChain, FAISS vector search, and the Falcon-7B LLM from Hugging Face to provide intelligent conversational responses based on course data.

 **Features**
- Uses `Falcon-7B-Instruct` for natural language understanding
- Embeds course data into FAISS for fast retrieval
- Conversational memory with `ConversationBufferMemory`
- Flask API for chatbot interaction
- Web interface for easy testing

**Requirements**
Make sure you have the following installed:
- Python 3.8+
- `pip`
- `git`
- `virtualenv` (optional but recommended)

### Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/falcon-chatbot.git
   cd falcon-chatbot
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv chatbot_env
   chatbot_env\Scripts\activate  # Windows
   # OR
   source chatbot_env/bin/activate  # Mac/Linux
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**
   - Create a `.env` file in the root directory.
   - Add your Hugging Face API token:
     ```plaintext
     HUGGINGFACEHUB_API_TOKEN=your_api_key_here
     ```

5. **Run Initial Setup Scripts:**
   Before running the chatbot, first test your API key and ensure embeddings are working.
   
   - **Run the scraper:**
     ```bash
     python scraper.py
     ```
   - **Generate the vector store:**
     ```bash
     python vector_store.py
     ```
   - **Verify API key with `test.py`:**
     ```bash
     python test.py
     ```
     If it prints a valid response, your API key is working correctly.

6. **Run the Chatbot:**
   ```bash
   python app.py
   ```
   The chatbot should now be running on `http://127.0.0.1:5000/`.


** Deployment**
If you want to deploy the chatbot so others (e.g., recruiters) can test it, consider using:
- **Render** (free Flask hosting)
- **Railway.app**
- **Hugging Face Spaces**

**Challenges Faced & Solutions**
 1. **Hugging Face API Key Not Updating**
- Initially, the chatbot was still using an old API key even after updating `.env`.
- Fixed by ensuring `.env` is loaded correctly and restarting the terminal.

 2. **Pushing to GitHub Without Exposing `.env`**
- Accidentally tried to push `.env`, which would expose the API key.
- Fixed by adding `.env` to `.gitignore` before committing.

 3. **FAISS Not Storing Data Correctly**
- Had issues where FAISS wasn’t retrieving the correct text.
- Resolved by checking the text chunking strategy and ensuring the embeddings were consistent.

** Future Improvements**
- Deploying to a cloud service for easy access
- Adding a UI with Streamlit for a better experience
- Improving chatbot responses with better prompt engineering

**Contributing**
Feel free to fork this repository, make improvements, and submit a pull request!

 **Contact**
For any issues or suggestions, reach out via GitHub or email "rithikabollapragada5@gmail.com".

