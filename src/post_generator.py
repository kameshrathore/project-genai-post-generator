from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


def get_length_str(length):
    return {
        "Short": "1-5 lines",
        "Medium": "6-10 lines",
        "Long": "11-15 lines"
    }[length]


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f"""
    Generate a LinkedIn post.

    Topic: {tag}
    Length: {length_str}
    Language: {language}

    If Hinglish, use English script.
    """

    examples = few_shot.get_filtered_posts(length, language, tag)

    if examples:
        prompt += "\nUse style from examples:\n"

    for i, post in enumerate(examples[:2]):
        prompt += f"\nExample {i+1}:\n{post['text']}\n"

    return prompt


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Motivation"))