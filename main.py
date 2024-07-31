import streamlit as st
from grab_videos import search_yt
import pandas as pd
from strip_audio import download_save_audio
from llm_results import *
import os

st.set_page_config()

if "product_name_submitted" not in st.session_state:
    st.session_state["product_name_submitted"] = False

# intro, explanation = st.columns(2)
st.title("👀 Generate Pros and Cons from YouTube Reviews")
st.markdown("🕒 Save 100x time, get 100% of the value ⭐")
st.markdown(
    "Enter the name of the product you have your eye on, and receive the most commonly discussed pros and cons in YouTube review videos."
)

keys, input = st.columns(2)

keys.markdown("#### Quick setup")

with keys.expander("Enter your API key"):
    # aai_col, yt_col = keys.columns(2)
    st.markdown(
        "* Get a Free AssemblyAI API Key [here](https://www.assemblyai.com/?utm_source=youtube&utm_medium=referral&utm_campaign=yt_mis_69)."# and a YouTube data API key [here](https://developers.google.com/youtube/registering_an_application)."
    )
    aai_api_key = st.text_input(
        "Please input your AssemblyAI API key",
        placeholder="Your AssemblyAI API key",
        label_visibility="collapsed",
        type="password",
    )
    # yt_api_key = st.text_input(
    #     "Please input your Google YouTube Data API key",
    #     placeholder="Your Google YouTube Data API key",
    #     label_visibility="collapsed",
    #     type="password",
    # )
    yt_api_key = os.environ.get("YOUTUBE_API_KEY")
    yt_api_key = "AIzaSyD56dGte-_Fy_F7sNh8VUeg9zdpEyHBdi4"

# get keyword from user
st.subheader("Which product would you like to buy?")
product = st.text_input(
    "The name of the product you'd like to analyse the reviews of."
)
search_phrase = product + " review"

if st.button("Search for review videos on YouTube"):
    st.session_state["product_name_submitted"] = True

if st.session_state["product_name_submitted"]:
    # send keyword to yt and get video links
    video_list = search_yt(yt_api_key, search_phrase)

    if video_list is None:
        st.error("Make sure your YouTube Data API Key is correct.", icon="🚨")

    else:

        # have user select videos
        video_data = pd.DataFrame(video_list)
        with st.form("data"):
            selected_df = st.data_editor(
                video_data,
                column_config={
                    "video_thumbnail": st.column_config.ImageColumn(
                        "Video Thumbnail", help="Streamlit app preview screenshots"
                    ),
                    "video_selected": st.column_config.CheckboxColumn(
                        "Select", help="Select videos to analyse", default=False
                    ),
                    "video_link": st.column_config.LinkColumn(
                        "Link to the video", disabled=True
                    ),
                    "channel_link": st.column_config.LinkColumn(
                        "Link to the channel", disabled=True
                    ),
                },
                hide_index=True,
            )
            submitted = st.form_submit_button("Submit")

        # send video links to strip audio and send audio files to llm

        if submitted:
            urls = selected_df[selected_df["video_selected"] == "True"][
                "video_link"
            ].tolist()

            id_list = []

            for url in urls:
                filename = download_save_audio(url)
                id = transcribe(aai_api_key, filename)
                id_list.append(id)

            pros, cons = group_analyse(id_list)

            # show results of llm analysis
            pros_col, cons_col = st.columns(2)

            pros_col.subheader("✅ Pros")
            pros_col.markdown(pros)

            cons_col.subheader("❌ Cons")
            cons_col.markdown(cons)
