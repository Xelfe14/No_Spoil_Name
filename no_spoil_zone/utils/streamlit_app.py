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
st.markdown(
        "<h1 style='text-align: center; color: black;'>💯 No Sploil Zone! 💯</h1>",
        unsafe_allow_html=True
    )
st.markdown("### 📚 Choose a Book and Discover Its Summary and Topics 📚")
st.markdown("---")

with st.container():
    # User input
    author_name = st.selectbox("Select Author", ["Austen, Jane", "Shakespeare, William", "Twain, Mark"])
    book_name = st.selectbox("Select Book", ["Emma", "Hamlet", "Tom Sawyer"])
    chapter_number = int(st.text_input('Total Number of Chapters'))
#-------------------------------------------------------------------------------------------------------------------------------------------------------
# PARAMS

dumy_dict={ 'master_sum': 'sumssunfovnzonzrnojvoizjfoznocnzoecizecinzoiczopejozjfojaofjaozj)ajfàjaoiefjoiejfoijfoinekon'}
dumy_dict_2={ "chapter_sum": 'jfpefpzkfoz,foz,io,zf,zofnozfioze,foz,eiof,zepfk,pze,' , "topics": {"persons" :['j','o','r'],"places": ['a','b','h'], "general": ['x','z','w'] } }
params = {
    'author_name': author_name,
    'book_name': book_name,
    'chapter': chapter_number
    }
url_main_summary= 'none'
url_chapter_summary='none'
# main_summary_response= requests.get(url_main_summary, params=params)
# chapter_summary_response= requests.get(url_chapter_summary, params=params)

#-------------------------------------------------------------------------------------------------------------------------------------------------------



if st.button("Run Summarization :🏄🏼:"):
    # with st.spinner('Running! No sploils here :😉:'):
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Main Summary

    if chapter_number == 1:
        st.subheader(f":pensif::bulle_de_pensée: What happens in the first chapter of {book_name}?")
    else:
        st.subheader(f":pensif::bulle_de_pensée: What happens in the first {chapter_number} chapters of {book_name}?")
        st.markdown(dummy_dict['master_sum'])
        st.markdown("---")


    # if book_summary_reponse.status_code == 200:
    #     book_summary = book_summary_reponse.json()
    #     st.write(book_summary)
    # else:
    #     st.write("Error retrieving summary")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Summary Breakdown
    st.subheader("Chapter Breakdown")
        # for i in range(chapter_number):
        #     i=1
        #     st.markdown(f"### Topics for Chapter {i}")
        #     for topic, value in dummy_dict_2['topics'].items():
        #         st.write(f"**{topic}**: {', '.join(value)}"

        #     st.markdown(f"### Summary for Chapter {i}")
        #     st.write(dummy_dict_2['chapter_sum'])
        #     st.markdown("---")
        #     i+=1

    for i in range(chapter_number):
        # Display topics for the current chapter
        st.markdown(f"### Topics for Chapter {i + 1}")
        for topic, value in dummy_dict_2['topics'].items():
            st.write(f"**{topic}**: {', '.join(value)}")

            # Display the summary for the current chapter
            st.markdown(f"### Summary for Chapter {i + 1}")
            st.write(dummy_dict_2['chapter_sum'])

    # Add a horizontal line to separate chapters
    st.markdown("---")





    # if chapter_response.status_code == 200:
    #     chapter_data = chapter_response.json()
    #     st.write(f"Chapter Title: {chapter_data['title']}")
    #     st.subheader("Topic Analysis")
    #     for topic, summary in chapter_data['topics'].items():
    #         st.write(f"Topic: {topic}")
    #         st.write(f"Summary: {summary}")
    # else:
    #     st.write("Unable to fetch chapter details.")


    # # Define text content for different slides based on BOX input
    # slide_content = [f"Chapter {i}" for i in range(1, num_chapters+1)]

    # # Create tabs
    # tabs = [f"Chapter {i}" for i in range(1, num_chapters+1)]
    # selected_tab = st.radio("Select a Chapter:", tabs)


    # # Get the index of the selected tab
    # selected_slide_index = tabs.index(selected_tab)
    # # Display the content of the selected slide
    # st.text_area("Chapter Content", value=slide_content[selected_slide_index], height=300, key=selected_slide_index)
