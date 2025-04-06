import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

from config import GEMINI_PROMPT
from utils import image


load_dotenv(override=True)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
class AnalysisSchema(BaseModel):
    """
    Schema for parsing the analysis response from the Gemini API.

    Attributes:
        analysis (str): The analysis result as a string.
        score (int): The score associated with the analysis.
        positives (list[str]): A list of positive aspects identified.
        negatives (list[str]): A list of negative aspects identified.
    """
    analysis: str
    score: int
    positives: list[str]
    negatives: list[str]

async def request(image_url: str) -> AnalysisSchema:
    """
    Sends a request to the Gemini API to analyze an image.

    Args:
        image_url (str): The URL of the image to be analyzed.

    Returns:
        AnalysisSchema: The parsed analysis result from the Gemini API.

    Raises:
        UserInputError: If the fetched content type is not supported.
    """
    image_content, content_type = await image.fetch(image_url)

    response = await client.aio.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=[GEMINI_PROMPT,
                types.Part.from_bytes(data=image_content, mime_type=content_type)],
        config={
            'response_mime_type': 'application/json',
            'response_schema': AnalysisSchema,
            'safety_settings': [
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                )
            ]
        }
    )
    
    analysis: AnalysisSchema = response.parsed

    return analysis
