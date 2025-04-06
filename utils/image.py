import aiohttp
import hashlib

from config import SUPPORTED_IMAGE_TYPES
from exceptions import UserInputError

session: aiohttp.ClientSession | None = None

def create_session() -> None:
    """
    Creates a new aiohttp session if one does not already exist.
    """
    global session 
    if session is None or session.closed:
        session = aiohttp.ClientSession()

async def close_session() -> None:
    """
    Closes the aiohttp session if it exists and is open.
    """
    global session
    if session and not session.closed:
        await session.close()

async def fetch(image_url: str) -> tuple[bytes, str]:
    """
    Fetches the content of an image from the given URL.

    Args:
        image_url (str): The URL of the image to fetch.
    
    Returns:
        tuple[bytes, str]: A tuple containing the image content as bytes and the content type as a string.
    
    Raises:
        UserInputError: If the fetched content type is not supported.
    """
    global session 
    async with session.get(image_url) as response:
        if response.status != 200:
            raise Exception(f"Failed to fetch image: {response.status}")

        mime_type = response.content_type
        image_bytes = await response.read()
    
    if mime_type not in SUPPORTED_IMAGE_TYPES:
        raise UserInputError(f"Unsupported image type: {mime_type}")

    return image_bytes, mime_type

async def get_hash(image_url: str) -> str:
    """
    Fetches an image from the given URL, processes it, and computes its perceptual hash.
    
    Args:
        image_url (str): The URL of the image to be fetched and hashed.
    
    Returns:
        str: The perceptual hash of the image as a string.
    
    Raises:
        UserInputError: If the fetched content type is not supported.
    """
    image_bytes = (await fetch(image_url))[0]
    image_hash = hashlib.blake2b(image_bytes, digest_size=16).hexdigest()
    
    return image_hash
