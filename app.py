import os
from dotenv import load_dotenv
import openai
import streamlit as st
import serpapi
import re

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up SerpApi client
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
client = serpapi.Client(api_key=serpapi_api_key)

def generate_blog_article(topic, word_count, keywords):
    # Fetch search results from SerpAPI
    search_query = f"{topic} {' '.join(keywords)}"
    search_results = fetch_search_results(search_query)

    # Extract relevant information from search results
    top_results = [result["title"] for result in search_results.get("organic_results", [])]
    related_questions = [question["query"] for question in search_results.get("related_questions", [])]

    # Construct the prompt with SerpAPI data
    prompt = f"Write a blog article on the topic '{topic}' with a word count of around {word_count} words. Include the following keywords: {', '.join(keywords)}.\n\n"
    prompt += f"Top search results for '{search_query}':\n\n" + "\n".join(top_results) + "\n\n"
    prompt += f"Related questions:\n\n" + "\n".join(related_questions) + "\n\n"
    prompt += "Blog article:"

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

def fetch_search_results(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_api_key
    }
    search_results = client.search(params)
    return search_results

def suggest_topics(search_query):
    search_results = fetch_search_results(search_query)
    topics = []
    for result in search_results.get("organic_results", []):
        title = result["title"]
        cleaned_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        topics.append(cleaned_title)
    return list(set(topics))

def main():
    st.title("Blog Article Writer with SERP Scraper")

    search_query = st.text_input("Enter a search query for topic suggestions:")
    suggested_topics = []

    if st.button("Suggest Topics"):
        suggested_topics = suggest_topics(search_query)

    if "topic" not in st.session_state:
        st.session_state["topic"] = None
    if "word_count" not in st.session_state:
        st.session_state["word_count"] = 100
    if "keywords" not in st.session_state:
        st.session_state["keywords"] = ""

    topic_index = 0 if st.session_state["topic"] is None else suggested_topics.index(st.session_state["topic"])
    topic = st.selectbox("Select a topic:", suggested_topics, index=topic_index, key="topic_selectbox")

    if topic != st.session_state["topic"]:
        st.session_state["topic"] = topic
        st.session_state["word_count"] = 100
        st.session_state["keywords"] = ""

    word_count = st.number_input("Enter the desired word count:", min_value=100, step=50, value=st.session_state["word_count"], key="word_count_input")
    keywords = st.text_input("Enter SEO keywords (comma-separated):", value=st.session_state["keywords"], key="keywords_input")

    if st.button("Generate Article"):
        if word_count and keywords:
            keywords = [kw.strip() for kw in keywords.split(",")]
            article = generate_blog_article(topic, word_count, keywords)
            st.markdown(f"## Generated Blog Article on '{topic}'")
            st.write(article)
        else:
            st.warning("Please fill in the word count and keywords.")

if __name__ == "__main__":
    main()

