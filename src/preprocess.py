import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

def clean_text(text):
    # Remove invalid unicode (like broken emojis)
    return text.encode("utf-8", "ignore").decode("utf-8")

def extract_metadata(post):
    template = """
        Extract metadata from the LinkedIn post.

        RULES:
        - Return ONLY valid JSON
        - No explanation, no text, no code
        - JSON must have exactly:
            line_count (number)
            language (English or Hinglish)
            tags (array of max 2 strings)

        Example Output:
        {{"line_count": 5, "language": "English", "tags": ["Job Search", "Motivation"]}}

        Post:
        {post}
        """
    pt = PromptTemplate.from_template(template)
    chain = pt | llm

    response = chain.invoke({"post": post})
    text = response.content.strip()

    try:
        parser = JsonOutputParser()
        return parser.parse(text)

    except Exception:
        # 🔥 Fallback (VERY IMPORTANT)
        import re
        import json

        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        print("⚠️ Bad LLM Output:\n", text)
        raise Exception("Error parsing LLM response")

def process_posts(raw_path, processed_path):
    with open(raw_path, encoding="utf-8") as f:
        posts = json.load(f)

    enriched = []

    for post in posts:
        cleaned_text = clean_text(post["text"])
        metadata = extract_metadata(cleaned_text)
        enriched.append({**post, **metadata})

    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=4)


if __name__ == "__main__":
    process_posts(
        "data/raw_posts.json",
        "data/processed_posts.json"
    )