import streamlit as st
from grab_videos import search_yt
import pandas as pd
from strip_audio import download_save_audio
from llm_results import *

if 'product_name_submitted' not in st.session_state:
    st.session_state['product_name_submitted'] = False

st.title("Pros and Cons from YouTube Reviews")
st.markdown("Enter the name of the product you have your eye on, and receive the most commonly discussed pros and cons in YouTube review videos.")


st.subheader("Quick setup.")
aai_col, yt_col = st.columns(2)
aai_api_key = aai_col.text_input("Please input your AssemblyAI API key", placeholder="Your AssemblyAI API key", label_visibility="collapsed")
yt_api_key = yt_col.text_input("Please input your Google YouTube Data API key", placeholder="Your Google YouTube Data API key", label_visibility="collapsed")


# get keyword from user
product = st.text_input("The name of the product you'd like to analyse the reviews of.")
search_phrase = product + " review"

if st.button("Search for review videos on YouTube"):
    st.session_state['product_name_submitted'] = True

if st.session_state['product_name_submitted']:
    # send keyword to yt and get video links
    video_list = search_yt(yt_api_key, search_phrase)

    # # instead of above line - remove later
    # import ast

    # with open('outputfile') as f:
    #     data = ast.literal_eval(f.read())
    # ########################


    # have user select videos
    video_data = pd.DataFrame(video_list)
    with st.form("data"):
        selected_df = st.data_editor(video_data,
                    column_config={
                "video_thumbnail": st.column_config.ImageColumn(
                "Video Thumbnail", help="Streamlit app preview screenshots"
                ),
                "video_selected": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select videos to analyse",
                    default=False,
                )
            },
            hide_index=True
        )
        submitted = st.form_submit_button("Submit")

    # send video links to strip audio and send audio files to llm

    if submitted:
        urls = selected_df[selected_df["video_selected"]=="True"]["video_link"].tolist()

        id_list = []

        for url in urls:
            filename = download_save_audio(url)
            id = transcribe(aai_api_key, filename)
            id_list.append(id)

        pros, cons = group_analyse(id_list)

        # # f = open("text.txt", "a")
        # # f.write(analysis_result)
        # # f.close()

        # with open('text.txt', 'r') as file:
        #     analysis_result = file.read()

    # show results of llm analysis
        pros_col, cons_col = st.columns(2)

        pros_col.subheader("✅ Pros")
        pros_col.markdown(pros)

        cons_col.subheader("❌ Cons")
        cons_col.markdown(cons)