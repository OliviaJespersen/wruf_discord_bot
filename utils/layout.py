def result(score: int, positives: list[str], negatives: list[str]) -> str:
    """
    Generates a formatted string summarizing the W.R.U.F score, positive factors, and negative factors.

    Args:
        score (int): The W.R.U.F score as a percentage.
        positives (list[str]): A list of positive factors.
        negatives (list[str]): A list of negative factors.

    Returns:
        str: A formatted string displaying the score, positive factors, and negative factors.
    """
    for list in [positives, negatives]:
        if len(list) == 0:
            list.append("None")

    return "\n".join([
        f"# W.R.U.F Score: {score}%",
        "## ✅ Positive Factors:",
        _bullet_point(positives),
        "## ❌ Negative Factors",
        _bullet_point(negatives)
    ])

def _bullet_point(lst: list) -> str:
    """
    Converts a list of strings into a bullet-point formatted string.

    Args:
        lst (list): A list of strings to format.

    Returns:
        str: A string with each item in the list prefixed by a bullet point.
    """
    return "\n".join(f"- {item}" for item in lst)

def leaderboard(leaderboard: list[tuple[str,int]]) -> str:
    """
    Generates a formatted leaderboard string from a list of tuples.

    Args:
        leaderboard (list[tuple[str, int]]): A list of tuples where each tuple contains a name and score.

    Returns:
        str: A formatted leaderboard string.
    """
    for i in range(len(leaderboard)):
        leaderboard[i] = f"{i+1}. **{leaderboard[i][0]}** - **{round(leaderboard[i][1], 2)}** W.R.U.F Points!"

    return "\n".join([
        "## W.R.U.F Leaderboard",
        _bullet_point(leaderboard)
    ])

def score_update(name: str, old_average: float, new_average: float) -> str:
    """
    Generates a formatted string summarizing a user's score update.

    Args:
        name (str): The name of the user.
        earned_score (int): The score the user earned or lost.
        total_score (int): The user's total score after the update.

    Returns:
        str: A formatted string describing the score update.
    """
    return f"**{name}'s** W.R.U.F score went from **{round(old_average, 2)}** to **{round(new_average, 2)}**!"

def score(name: str, score: float) -> str:
    """
    Generates a formatted string summarizing a user's score.

    Args:
        name (str): The name of the user.
        score (float): The user's score.

    Returns:
        str: A formatted string describing the user's score.
    """
    return f"""**{name}** has a W.R.U.F score of **{round(score, 2)}**!"""

def error(message: str, description: str = "") -> str:
    """
    Generates a formatted error message.

    Args:
        message (str): The error message.
        description (str, optional): A description of the error. Defaults to None.

    Returns:
        str: A formatted error message.
    """
    message = f"💔 {message} (x_x)\n{description}"
    if description:
        message += f"\n{description}"

    return message