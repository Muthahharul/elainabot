from dotenv import load_dotenv
import os

load_dotenv(override=True)  

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
