import streamlit as st
import requests

def main():
    st.markdown(
        "<h1 style='text-align: center; color: white;'>💯 No Sploil Zone! 💯</h1>",
        unsafe_allow_html=True
    )

    st.markdown("### 📚 Choose a Book and Discover Its Summary and Topics 📚")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        author_name = st.selectbox("Select Author", ["Jane Austen", "William Shakespear", "Mark Twain"])
    with col2:
        book_name = st.selectbox("Select Book", ["Emma", "Hamlet", "Tom Sawyer"])
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
                       st.subheader(f"🤔💭 What happens in the first chapter of {book_name}?")
                    else:
                        st.subheader(f"🤔💭 What happens in the first {chapter_number} chapters of {book_name}?")
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
                        st.subheader(f"Chapter {i} People, Places, and Things")
                        st.write("========================================================================================")
                        st.markdown(f"**People:** {', '.join(topic_dict['persons'])}")
                        st.markdown(f"**Places:** {', '.join(topic_dict['places'])}")
                        st.markdown(f"**Things:** {', '.join(topic_dict['general'])}")
                        st.subheader(f"Chapter {i} Summary")
                        st.write("========================================================================================")
                        st.markdown(chapter_summary)
                    else:
                        st.subheader(f"Chapter {i} Summary")
                        st.markdown("Not found")



            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
