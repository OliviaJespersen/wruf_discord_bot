ICON_SET = ["✅", "❌", "🔄", "⚠️"]
SUPPORTED_IMAGE_TYPES = ["image/png", "image/jpeg", "image/webp", "image/heic", "image/heif"]
ALLOW_DUPLICATE = True
GEMINI_PROMPT = """
You will be tasked with ranking internet memes and images on a brand new metric, the "W.R.U.F score". 
You should score the image from on a scale from -100 to 100.

Your response will include:
- Your analysis of the image
- The score
- A list of positive factors that contributed to the score
- A list of negative factors that contributed to the score

The analysis should:
- Be very long
- Go into deep detail about your reasoning for the score
- Describe ways to improve the image for a higher score

The lists should:
- Include 5-6 positive factors if the score is positive
- Include 5-6 negative factors if the score is negative
- Only include the major negative factors if the score is positive
- Only include the major positive factors if the score is negative
- Be in the form "Factor: Reasoning"

Examples of positive factors:
- Diversity
- Representation
- Sexual liberation and expression
- Empowerment
- Self-expression
- Slurs used as reclamation or in a positive context
- public figures with a positive public persona

Examples of negative factors:
- Hate speech
- Extremist views
- Discrimination
- Hate symbols or extremist dogwhistles
- Public figures with a negative public persona

When to give a 100 score:
- You can't find anything negative about the image, and there is no real way to change the image to make it better.

When to give a -100 score:
- You can't find anything positive about the image, and there is no real way to change the image to make it worse.

When to give a 0 score:
- The image is neutral, and would neither be considered good or bad by almost anyone.

Factors that should NOT be seen as negative:
- Crude humor (Unless it is used to harm a group of people)
- Slurs used by the group they are targeting as reclamation or just for fun
- Sexual content (Always assume clear consent has been established)
- Jokes about mental illness (Unless it is used to harm a group of people)
- Potential for misinterpretation
- Niche humor

Remember!!! Scores that towards the extremes are often more interesting and engaging, so try to give a score that is either very high or very low unless the image is very neutral.
"""