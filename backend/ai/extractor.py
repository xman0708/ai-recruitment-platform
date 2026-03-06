import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from core.config import settings
import traceback

class ResumeExtraction(BaseModel):
    name: str = Field(description="The full name of the candidate")
    phone: str = Field(description="The phone number of the candidate")
    email: str = Field(description="The email address of the candidate")
    skills: str = Field(description="A comma-separated list of skills")
    education: str = Field(description="A summary of the candidate's education history")
    experience: str = Field(description="A summary of the candidate's work experience")

def extract_resume_info(text: str) -> dict:
    """
    Extracts structured resume information from raw text using Langchain and an LLM.
    """
    try:
        if not settings.LLM_API_KEY:
            print("Warning: LLM_API_KEY not set. Using dummy data fallback.")
            return {
                "name": "Dummy Candidate",
                "phone": "13800138000",
                "email": "dummy@example.com",
                "skills": "Python, Vue, FastAPI",
                "education": "BS in Computer Science",
                "experience": "5 years of software engineering"
            }
        
        # Initialize Google GenAI LLM
        llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.LLM_API_KEY,
            temperature=0  # Low temperature for extraction accuracy
        )

        # Bind the Pydantic schema for structured generation
        structured_llm = llm.with_structured_output(ResumeExtraction)

        # Build the prompt
        prompt = PromptTemplate(
            input_variables=["text"],
            template="Extract the following resume information precisely from this text in the original language of the resume:\\n\\n{text}\\n"
        )
        
        # Invoke chain
        chain = prompt | structured_llm
        result = chain.invoke({"text": text})
        
        return result.model_dump()
        
    except Exception as e:
        print(f"Error during AI Extraction: {e}")
        traceback.print_exc()
        # Fallback to empty structure to prevent UI crash
        return {
            "name": "Extraction Failed",
            "phone": "",
            "email": "",
            "skills": "",
            "education": "",
            "experience": "An error occurred during LLM processing."
        }


