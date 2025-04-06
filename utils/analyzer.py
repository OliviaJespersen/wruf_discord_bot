from config import ALLOW_DUPLICATE
from exceptions import UserInputError
from utils import gemini, database, layout, image


async def image_analysis(image_url: str, author_name: str, author_id: int, deep: bool = False) -> list[str]:
    """
    Analyzes an image using the Gemini service and updates the author's score in the database.

    Args:
        image_url (str): The URL of the image to analyze.
        author_name (str): The name of the author requesting the analysis.
        author_id (int): The unique identifier of the author.
        deep (bool, optional): Whether to include a deep analysis in the response. Defaults to False.

    Returns:
        list[str]: A list of messages containing the analysis results and score updates.

    Raises:
        UserInputError: If the fetched content type is not supported or if the image has already been analyzed.
    """
    messages = []

    image_hash = await image.get_hash(image_url)

    if not ALLOW_DUPLICATE and await database.check_resource(image_hash):
        raise UserInputError("This image has already been analyzed before")

    response = await gemini.request(image_url)

    old_average = await database.get_average_score(author_id)
    await database.update_score(author_id, response.score)
    new_average = await database.get_average_score(author_id)
    
    messages.append(image_url)
    messages.append(layout.result(response.score, response.positives, response.negatives))
    if deep:
        messages.append(response.analysis)
    messages.append(layout.score_update(author_name, old_average, new_average))

    await database.add_resource(image_hash)
    
    return messages
