import streamlit as st
import numpy as np
import pandas as pd
import os
import base64
import plotly.express as px
import requests

# Background image CSS
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://images.unsplash.com/photo-1541963463532-d68292c34b19?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2788&q=80");
    background-size: 100%;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: local;
}}

[data-testid="stHeader"] {{
    background:
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}

.css-1n76uvr .e1tzin5v0 {{
  background: rgba(255,255,255,0.5)
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#Front header
st.markdown("""# NO SPOIL ZONE
## by the Tadpoles
smooth slopes and no spoilers""")
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#drop down boxs for Authors and Books and Chapters
with st.container():
    # User input
    author_name = st.selectbox("Select Author", ["Austen, Jane", "Shakespeare, William", "Twain, Mark"])
    book_name = st.selectbox("Select Book", ["Emma", "Hamlet", "Tom Sawyer"])
    chapter_number = st.number_input("Enter Chapter Number:", min_value=1, value=1)

    # authorz = df_books['Author'].sort_values().unique()
    # selected_author = st.selectbox('Author', authorz)
    # filtered_bookz = df_books[df_books['Author'] == selected_author]
    # titles_for_author = filtered_bookz['Title'].sort_values().unique()
    # selected_title = st.selectbox('Book', titles_for_author)

    # Input for the number of chapters
    num_chapters = int(st.text_input('Total Number of Chapters'))
#-------------------------------------------------------------------------------------------------------------------------------------------------------
  #API Params PULLLMEH

    url = 'http://gcpurl/summary'

    params = {
        'title': selected_title, # 0 for Sunday, 1 for Monday, ...
        'autohor': filtered_bookz
    }

    response = requests.get(url, params=params)
    response.json() #=> {wait: 64}
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Main Summary
    st.subheader("Main Summary")
    if book_summary_reponse.status_code == 200:
        book_summary = book_summary_reponse.json()
        st.write(book_summary)
    else:
        st.write("Error retrieving summary")

#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Summary Breakdown
    st.subheader("Chapter Breakdown")
    if chapter_response.status_code == 200:
        chapter_data = chapter_response.json()
        st.write(f"Chapter Title: {chapter_data['title']}")
        st.subheader("Topic Analysis")
        for topic, summary in chapter_data['topics'].items():
            st.write(f"Topic: {topic}")
            st.write(f"Summary: {summary}")
    else:
        st.write("Unable to fetch chapter details.")


    # Define text content for different slides based on BOX input
    slide_content = [f"Chapter {i}" for i in range(1, num_chapters+1)]

    # Create tabs
    tabs = [f"Chapter {i}" for i in range(1, num_chapters+1)]
    selected_tab = st.radio("Select a Chapter:", tabs)


    # Get the index of the selected tab
    selected_slide_index = tabs.index(selected_tab)
    # Display the content of the selected slide
    st.text_area("Chapter Content", value=slide_content[selected_slide_index], height=300, key=selected_slide_index)


#things to do:
#1. widen page
