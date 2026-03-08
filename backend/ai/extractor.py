import json
from anthropic import Anthropic
from core.config import settings
import traceback

def extract_resume_info(text: str) -> dict:
    """
    Extracts structured resume information from raw text using Anthropic SDK (Minimax API format).
    """
    try:
        if not settings.LLM_API_KEY:
            print("Warning: LLM_API_KEY not set. Using dummy data fallback.")
            return _get_fallback_data()
        
        # Initialize Anthropic SDK
        client = Anthropic(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL
        )

        tools = [
            {
                "name": "extract_resume_details",
                "description": "Extract structured information from a candidate's resume",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The full name of the candidate"
                        },
                        "phone": {
                            "type": "string",
                            "description": "The phone number of the candidate"
                        },
                        "email": {
                            "type": "string",
                            "description": "The email address of the candidate"
                        },
                        "skills": {
                            "type": "string",
                            "description": "A comma-separated list of candidate's skills"
                        },
                        "education": {
                            "type": "string",
                            "description": "A short summary of the candidate's education history (e.g., BS in Computer Science)"
                        },
                        "experience": {
                            "type": "string",
                            "description": "A short summary of the candidate's work experience (e.g., 5 years of software engineering)"
                        },
                        "ai_score": {
                            "type": "integer",
                            "description": "A score from 0 to 100 indicating the quality and completeness of the resume"
                        },
                        "ai_reasoning": {
                            "type": "string",
                            "description": "A short sentence explaining the rationale behind the ai_score"
                        }
                    },
                    "required": ["name", "phone", "email", "skills", "education", "experience", "ai_score", "ai_reasoning"]
                }
            }
        ]

        messages = [
            {"role": "user", "content": f"You are an expert HR assistant. Your task is to extract precise information from the following resume text and format it into a structured output.\n\nResume Text:\n\n{text}"}
        ]

        response = client.messages.create(
            model=settings.LLM_MODEL,
            max_tokens=1024,
            messages=messages,
            tools=tools,
            temperature=0.1,
            tool_choice={"type": "tool", "name": "extract_resume_details"}
        )

        # Extract the tool use payload
        for block in response.content:
            if block.type == "tool_use" and block.name == "extract_resume_details":
                return block.input
        
        # Fallback if no tool use found
        print("No tool use block found in the response")
        return _get_fallback_data("Model failed to invoke extraction tool.")
        
    except Exception as e:
        print(f"Error during AI Extraction: {e}")
        traceback.print_exc()
        return _get_fallback_data("An error occurred during LLM processing.")

def _get_fallback_data(error_msg: str = "Fallback triggered") -> dict:
    return {
        "name": "Extraction Failed",
        "phone": "",
        "email": "",
        "skills": "",
        "education": "",
        "experience": error_msg,
        "ai_score": 0,
        "ai_reasoning": "解析失败"
    }
