import os
from dotenv import load_dotenv
import openai
import streamlit as st
from google_search_results import GoogleSearch

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up SerpApi client
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
params = {
    "engine": "google",
    "api_key": serpapi_api_key
}
search = GoogleSearch(params)

def generate_blog_article(topic, word_count, keywords):
    prompt = f"Write a blog article on the topic '{topic}' with a word count of around {word_count} words. Include the following keywords: {', '.join(keywords)}."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=word_count * 2,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.7,
    )

    article = response.choices[0].text.strip()
    return article

def fetch_search_results(query):
    params.update({"q": query})
    search_results = search.get_dict()
    return search_results

def main():
    st.title("Blog Article Writer with SERP Scraper")

    topic = st.text_input("Enter the blog topic:")
    word_count = st.number_input("Enter the desired word count:", min_value=100, step=50)
    keywords = st.text_input("Enter SEO keywords (comma-separated):")
    search_query = st.text_input("Enter a search query for SERP scraping:")

    if st.button("Generate Article"):
        if topic and word_count and keywords:
            keywords = [kw.strip() for kw in keywords.split(",")]
            article = generate_blog_article(topic, word_count, keywords)
            st.markdown(f"## Generated Blog Article on '{topic}'")
            st.write(article)
        else:
            st.warning("Please fill in all the required fields.")

    if search_query:
        search_results = fetch_search_results(search_query)
        st.write(search_results)

if __name__ == "__main__":
    main()

