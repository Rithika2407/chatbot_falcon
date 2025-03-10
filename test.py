import os
from dotenv import load_dotenv

load_dotenv()
huggingface_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print(f"Loaded API Token: {huggingface_api_token}")
