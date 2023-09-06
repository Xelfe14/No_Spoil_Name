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
    author_name = st.selectbox("Select Author", ["Jane Austen", "Shakespeare, William", "Twain, Mark"])
    book_name = st.selectbox("Select Book", ["Emma", "Hamlet", "Tom Sawyer"])
    chapter_number = int(st.text_input('Total Number of Chapters'))
#-------------------------------------------------------------------------------------------------------------------------------------------------------
# PARAMS

dummy_dict={
    'master_sum': 'sumssunfovnzonzrnojvoizjfoznocnzoecizecinzoiczopejozjfojaofjaozj)ajfàjaoiefjoiejfoijfoinekon'
    }
dummy_dict_2={
    "chapter_sum": 'jfpefpzkfoz,foz,io,zf,zofnozfioze,foz,eiof,zepfk,pze,',
    "topics": {
        "persons" :['j','o','r'],
        "places": ['a','b','h'],
        "general": ['x','z','w']
        }
    }
params = {
    'author_name': author_name,
    'book_name': book_name,
    'chapter': chapter_number
    }
url_chapter_summary='https://api-no-spoil-zone-vr5zz4u7ca-uc.a.run.app/master_summary?author_name=ane%20Austen&book_name=Emma&chapter_number=2'

# url_main_summary=f'https://api-no-spoil-zone-vr5zz4u7ca-uc.a.run.app/master_summary?author_name={author_name}&book_name={book_name}&chapter_number={chapter_number}'
url_main_summary= 'https://api-no-spoil-zone-vr5zz4u7ca-uc.a.run.app/chapter_summary?author_name=Jane%20Austen&book_name=Emma&chapter_number=2'
main_summary_response= requests.get(url_main_summary).json()
chapter_summary_response= requests.get(url_chapter_summary).json()

#-------------------------------------------------------------------------------------------------------------------------------------------------------



if st.button("Run Summarization 🏄🏼"):
    st.spinner('Running! No sploils here :😉:')
    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Main Summary

    if chapter_number == 1:
        st.header(f"🧐💭 What happens in the first chapter of {book_name}?")
        st.markdown(main_summary_response['master_sum'])
    else:
        st.header(f"🧐💭 What happens in the first: {chapter_number} chapters of {book_name}?")
        st.markdown(main_summary_response['master_sum'])
        st.markdown("###---")


    # if book_summary_reponse.status_code == 200:
    #     book_summary = book_summary_reponse.json()
    #     st.write(book_summary)
    # else:
    #     st.write("Error retrieving summary")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------
    # #Summary Breakdown

    st.title("Chapter Breakdown")
    for i in range(chapter_number):
        # Display topics for the current chapter
        st.markdown(f"### Topics for Chapter {i + 1}")
        for topic, value in chapter_summary_response.items():
            st.write(f"**{topic}**: {', '.join(value)}")

         # Display the summary for the current chapter
        st.markdown(f"### Summary for Chapter {i + 1}")
        st.write(chapter_summary_response['chapter_sum'])

    # Add a horizontal line to separate chapters
    st.markdown("---")
