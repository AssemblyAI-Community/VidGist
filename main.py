import streamlit as st
from grab_videos import search_yt
from strip_audio import download_save_audio
from llm_results import *
import pandas as pd
import os

if "aai_api_key" and "search_keyword" and "analysis_submitted" not in st.session_state:
    st.session_state["aai_api_key"] = ""
    st.session_state["search_keyword"] = ""
    st.session_state["analysis_submitted"] = False
    st.session_state["video_list"] = None

## callback functions to update session states
# Streamlit apps run from to to bottom everytime user enters an input
# SessionStates are used to remember information between these runs
def save_api_key(key):
    st.session_state["aai_api_key"] = key
    print("aai api key saved")

def save_keyword(keyword):
    st.session_state["search_keyword"] = keyword
    print("search keyword saved")

def update_analysis_state(video_list):
    st.session_state["analysis_submitted"] = True
    st.session_state["video_list"] = video_list

## Title and information about the app
st.title("👀 Generate Pros and Cons from YouTube Reviews")
st.markdown("🕒 Save 100x time, get 100% of the value ⭐")
st.markdown(
    "Enter the name of the product you have your eye on, and receive the most commonly discussed pros and cons in YouTube review videos."
)

## collect user API key
keys, input = st.columns(2)

keys.markdown("#### Quick setup")
if st.session_state["aai_api_key"] == "":
    with keys.expander("Enter your API key"):
        
        st.markdown(
            "* Get a Free AssemblyAI API Key [here](https://www.assemblyai.com/?utm_source=youtube&utm_medium=referral&utm_campaign=yt_mis_69)." # and a YouTube data API key [here](https://developers.google.com/youtube/registering_an_application)."
        )
        aai_api_key = st.text_input(
            "Please input your AssemblyAI API key",
            placeholder="Your AssemblyAI API key",
            label_visibility="collapsed",
            type="password",
            value=st.session_state["aai_api_key"]
        )
        st.button("Submit", on_click=save_api_key, args=(aai_api_key,))
else:
    # once the API key is saved in the session state, we change the look of the API key entry form to inform the user
    # they can still update this API key if they like
    with keys.expander("✅ API key submitted!"):
        st.write("API key saved!")

        aai_api_key = st.text_input(
            "Update AssemblyAI API key",
            placeholder="Your AssemblyAI API key",
            label_visibility="collapsed",
            type="password",
            value=st.session_state["aai_api_key"]
        )
        st.button("Update", on_click=save_api_key, args=(aai_api_key,))


st.subheader("Which product would you like to buy?")
product = st.text_input(
    "The name of the product you'd like to analyse the reviews of.", value=st.session_state["search_keyword"][:-7]
)
search_phrase = product + " review"
st.button("Search!", on_click=save_keyword, args=(search_phrase,))

if st.session_state["aai_api_key"] == "" and st.session_state["search_keyword"] != "":
    st.error("Please fill in your AssemblyAI API Key.", icon="🚨")


if st.session_state["aai_api_key"] != "" and st.session_state["search_keyword"] != "":

    video_list = None

    if not st.session_state["analysis_submitted"]:
        yt_api_key = os.environ.get("YOUTUBE_API_KEY")
        # yt_api_key = "your own YouTube Data API Key"
        video_list = search_yt(yt_api_key, st.session_state["search_keyword"])
    else:
        video_list = st.session_state["video_list"]
    
    if video_list is None:
        st.error("Make sure your YouTube Data API Key is correct.", icon="🚨")
    else:
        with st.form("video"):
            col1, col2, col3, col4 = st.columns(4)
            col5, col6, col7, col8 = st.columns(4)

            vid1 = col1.checkbox("👇 select video", key="vid1")
            col1.image(video_list[0]["video_thumbnail"])
            col1.write(video_list[0]["video_title"])

            vid2 = col2.checkbox("👇 select video", key="vid2")
            col2.image(video_list[1]["video_thumbnail"])
            col2.write(video_list[1]["video_title"])

            vid3 = col3.checkbox("👇 select video", key="vid3")
            col3.image(video_list[2]["video_thumbnail"])
            col3.write(video_list[2]["video_title"])

            vid4 = col4.checkbox("👇 select video", key="vid4")
            col4.image(video_list[3]["video_thumbnail"])
            col4.write(video_list[3]["video_title"])

            vid5 = col5.checkbox("👇 select video", key="vid5")
            col5.image(video_list[4]["video_thumbnail"])
            col5.write(video_list[4]["video_title"])

            vid6 = col6.checkbox("👇 select video", key="vid6")
            col6.image(video_list[5]["video_thumbnail"])
            col6.write(video_list[5]["video_title"])

            vid7 = col7.checkbox("👇 select video", key="vid7")
            col7.image(video_list[6]["video_thumbnail"])
            col7.write(video_list[6]["video_title"])

            vid8 = col8.checkbox("👇 select video", key="vid8")
            col8.image(video_list[7]["video_thumbnail"])
            col8.write(video_list[7]["video_title"])

            submitted = st.form_submit_button("Submit", on_click=update_analysis_state, args=(video_list,))

        if st.session_state["analysis_submitted"]:
            # gives a list of True or False based on which checkboxes were checked
            print(vid1, vid2, vid3, vid4, vid5, vid6, vid7, vid8)
            bool_list = [vid1, vid2, vid3, vid4, vid5, vid6, vid7, vid8]

            video_df = pd.DataFrame(video_list)
            selected_videos = video_df[bool_list]
            urls = selected_videos["video_link"].tolist()

            print(urls)
            id_list = []

            for url in urls:
                filename = download_save_audio(url)
                filename = url
                id = transcribe(st.session_state["aai_api_key"], filename)
                id_list.append(id)

            pros, cons = group_analyse(id_list)

            # show results of llm analysis
            pros_col, cons_col = st.columns(2)

            pros_col.subheader("✅ Pros")
            pros_col.markdown(pros)

            cons_col.subheader("❌ Cons")
            cons_col.markdown(cons)