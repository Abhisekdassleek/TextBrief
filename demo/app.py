import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import arxiv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = "AIzaSyDSvSN87YizAHtqClnGBYInlwpVQL7CQ2I"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def getResponse(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def search_arxiv(query):
    search = arxiv.Search(
        query=query,
        max_results=5,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id,
            "authors": ", ".join([author.name for author in result.authors]),
            "published": result.published.date()
        })
    return results

st.set_page_config(page_title="TextBrief", page_icon="📑", layout='centered', initial_sidebar_state='collapsed')
st.header("TextBrief")

input_text = st.text_input("Enter the Topic")
col1, col2 = st.columns([5, 5])
col3, col4 = st.columns([5, 5])
with col1:
    style = st.selectbox('Content type', ('story', 'poem', 'essay', 'role play', 'blog'))
with col2:
    for_whom = st.selectbox('Writing the content for', ('Researchers', 'Engineer', 'Student', 'Professor', 'Common People'), index=0)
with col3:
    number = st.text_input('No of lines/words')
with col4:
    ln = st.selectbox('Content in specified', ('words', 'lines', 'paragraphs'))

submit = st.button("Generate")

if submit:
    prompt = f"Write a {style} for {for_whom} on the topic {input_text} within {number} {ln}."
    response = getResponse(prompt)
    st.write(response.replace('\n', '\n\n'))

    st.header("arXiv Search Results")
    arxiv_results = search_arxiv(input_text)
    for result in arxiv_results:
        st.subheader(result["title"])
        st.write(result["summary"])
        st.write(f"Authors: {result['authors']}")
        st.write(f"Published: {result['published']}")
        st.write(f"[Read more]({result['url']})")

