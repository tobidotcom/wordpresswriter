import os
from dotenv import load_dotenv
import openai
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_blog_article(topic, word_count):
    prompt = f"Write a blog article on the topic '{topic}' with a word count of around {word_count} words."
    prompt += "\n\nBlog article:"

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=word_count * 2,
        n=1,
        stop=None,
        temperature=0.7,
    )

    article = response.choices[0].text.strip()
    return article

def generate_topics(keyword, num_topics=5):
    prompt = f"Suggest {num_topics} interesting blog article topics related to the keyword '{keyword}':"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    topics = response.choices[0].text.strip().split("\n")
    return topics

def main():
    st.title("Blog Article Generator")

    if "topic" not in st.session_state:
        st.session_state["topic"] = ""
    if "word_count" not in st.session_state:
        st.session_state["word_count"] = 500
    if "keyword" not in st.session_state:
        st.session_state["keyword"] = ""

    topic = st.text_input("Enter a topic for the blog article:", value=st.session_state["topic"], key="topic_input")
    word_count = st.number_input("Enter the desired word count:", min_value=100, step=50, value=st.session_state["word_count"], key="word_count_input")
    keyword = st.text_input("Enter a keyword to generate suggested topics:", value=st.session_state["keyword"], key="keyword_input")

    if st.button("Generate Topics"):
        if keyword:
            suggested_topics = generate_topics(keyword)
            st.write(f"Suggested Topics for '{keyword}':")
            for topic in suggested_topics:
                st.write(f"- {topic}")
        else:
            st.warning("Please enter a keyword to generate suggested topics.")

    if st.button("Generate Article"):
        if topic and word_count:
            article = generate_blog_article(topic, word_count)
            st.markdown(f"## Generated Blog Article on '{topic}'")
            st.write(article)
        else:
            st.warning("Please enter a topic and word count.")

if __name__ == "__main__":
    main()



