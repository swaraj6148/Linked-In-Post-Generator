from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

#print(os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model='gemini-3.6-flash'
    )

if __name__ == "__main__":
    output = llm.invoke("What are the two main ingredients in samosa ?")
    print(output.content[0]['text'])