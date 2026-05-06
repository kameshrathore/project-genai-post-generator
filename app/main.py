import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.few_shot import FewShotPosts
from src.post_generator import generate_post


def main():
    st.title("🚀 LinkedIn Post Generator")

    fs = FewShotPosts()

    col1, col2, col3 = st.columns(3)

    with col1:
        tag = st.selectbox("Topic", fs.get_tags())

    with col2:
        length = st.selectbox("Length", ["Short", "Medium", "Long"])

    with col3:
        language = st.selectbox("Language", ["English", "Hinglish"])

    if st.button("Generate"):
        post = generate_post(length, language, tag)
        st.write(post)


if __name__ == "__main__":
    main()