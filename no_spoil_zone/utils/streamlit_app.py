import streamlit as st
import numpy as np
import pandas as pd
import os
import base64
import plotly.express as px
import requests

def main():
    st.markdown(
        "<h1 style='text-align: center; color: #E31727 ;'>💯 No Sploil Zone! 💯</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='text-align: center;'>knowledge now, spoils later 🤫</div>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    author_book_dict = {
        "G. A. Henty": ["A Knight of the White Cross: A Tale of the Siege of Rhodes", "All But Lost: A Novel. Vol. 2 of 3",\
        "Among Malay Pirates : a Tale of Adventure and Peril", "At Aboukir and Acre: A Story of Napoleon's Invasion of Egypt",\
        "At Aboukir and Acre: A Story of Napoleon's Invasion of Egypt", "Beric the Briton : a Story of the Roman Invasion",\
        "Bonnie Prince Charlie : a Tale of Fontenoy and Culloden", "By England's Aid; or, the Freeing of the Netherlands",\
        "By Pike and Dyke: a Tale of the Rise of the Dutch Republic","By Sheer Pluck: A Tale of the Ashanti War", "Colonel Thorndyke's Secret",\
        "Facing Death; Or, The Hero of the Vaughan Pit: A Tale of the Coal Mines", "In Freedom's Cause : A Story of Wallace and Bruce",\
        "In the Hands of the Cave-Dwellers", "Out with Garibaldi: A story of the liberation of Italy", "Rujub, the Juggler",\
        "The Bravest of the Brave — or, with Peterborough in Spain", "The Lion of the North: A Tale of the Times of Gustavus Adolphus", "The Queen's Cup"],
        "Henri Rene Guy de Maupassant": ["Yvette"],
        "Honore de Balzac": ["A Daughter of Eve"],
        "Jane Austen": ["Emma"]
    }
    col1, col2, col3 = st.columns(3)
    with col1:
        author_name = st.selectbox("Select Author", ["G. A. Henty", "Henri Rene Guy de Maupassant", "Honore de Balzac", "Jane Austen"])
    with col2:
        book_name = st.selectbox("Select Book", author_book_dict[author_name])
    with col3:
        chapter_number = st.number_input("Enter Chapter Number:", min_value=1, value=1)
    st.markdown("---")
    if st.button("Run Summarization 🚀"):
        with st.spinner('Running! No sploils here 😉'):
            try:
                # Making API request for Master Summary
                master_url = f"https://api-no-spoil-zone-vr5zz4u7ca-uc.a.run.app/"
                master_summary_response = requests.get(f"{master_url}master_summary?author_name={author_name}&book_name={book_name}&chapter_number={chapter_number}")
                if master_summary_response.status_code == 200:
                    master_summary_data = master_summary_response.json()
                    # Assuming the summary is returned in 'summary' key in JSON response
                    master_summary = master_summary_data.get('master_sum', '')
                    if chapter_number == 1:
                       st.subheader(f"🧐💭 What happens in the first chapter of {book_name}?")
                    else:
                        st.subheader(f"🧐💭 What happens in the first {chapter_number} chapters of {book_name}?")
                    st.markdown(master_summary)
                # else:
                #     st.error(f"Failed to get Master Summary. Status Code: {master_summary_response.status_code}")
                st.markdown("---")
                # Similarly, you can make API requests for individual chapter summaries here.
                for i in range(1, chapter_number + 1):
                    chapter_summary_response = requests.get(f"{master_url}chapter_summary?author_name={author_name}&book_name={book_name}&chapter_number={i}")
                    if chapter_summary_response.status_code == 200:
                        chapter_summary_data = chapter_summary_response.json()
                        chapter_summary = chapter_summary_data.get('chapter_sum', '')
                        topic_dict = chapter_summary_data.get('topics', '')
                        st.subheader(f"Chapter {i}")
                        st.write("=========================================================================")
                        st.subheader("People 👨‍👩‍👦‍👦, Places 🏢, and Things ♟")
                        st.markdown(f"**People:** {', '.join(topic_dict['persons'])}")
                        st.markdown(f"**Places:** {', '.join(topic_dict['places'])}")
                        st.markdown(f"**Things:** {', '.join(topic_dict['general'])}")
                        st.subheader(f"Summary 📝")
                        st.markdown(chapter_summary)
                        st.markdown("---")
                    else:
                        st.subheader(f"Chapter {i} Summary")
                        st.markdown("Not found")
            except Exception as e:
                st.error(f"An error occurred: {e}")
if __name__ == '__main__':
    main()
