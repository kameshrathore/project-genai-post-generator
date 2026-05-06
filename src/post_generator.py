from src.llm_helper import get_llm_response
from src.few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    elif length == "Medium":
        return "6 to 10 lines"
    else:
        return "11 to 15 lines"


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f"""
Generate a LinkedIn post.

Topic: {tag}
Length: {length_str}
Language: {language}

If language is Hinglish, use English script.

No preamble.
"""

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "\nUse writing style similar to below examples:\n"

    for i, post in enumerate(examples[:2]):
        prompt += f"\nExample {i+1}:\n{post['text']}\n"

    return prompt


# ✅ THIS FUNCTION WAS MISSING / BROKEN
def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    return get_llm_response(prompt)