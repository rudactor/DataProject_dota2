import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import data.cfg as cfg

st.set_page_config(page_title="Dota Analysis", page_icon=":video_game:", layout="wide")

@st.cache_data
def get_top_heroes_data(top_n: int):
    resp = requests.get(cfg.GET_TOP_HEROES_URL, params={"top_n": top_n})
    if resp.status_code == 200:
        data = resp.json()
        return pd.DataFrame(data)
    else:
        st.error("Failed to fetch hero data.")
        return pd.DataFrame()

@st.cache_data
def get_chat_activity_data():
    resp = requests.get(cfg.GET_CHAT_ACTIVITY_URL)
    if resp.status_code == 200:
        data = resp.json()
        return pd.DataFrame(data)
    else:
        st.error("Failed to fetch chat activity data.")
        return pd.DataFrame()

@st.cache_data
def get_bad_message_percentage():
    resp = requests.get(cfg.GET_BAD_MSG_PERCENT_URL)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("bad_message_percentage", None)
    else:
        st.error("Failed to fetch bad message percentage.")
        return None

@st.cache_data
def get_matches_stats():
    resp = requests.get(cfg.GET_MATCHES_STATS_URL)
    if resp.status_code == 200:
        return resp.json()
    else:
        st.error("Failed to fetch matches stats.")
        return {}

st.sidebar.title("Navigation")
pages = ["Introduction", "Analytics", "Hypothesis & Complex Graphs", "Add Record"]
page = st.sidebar.radio("Go to:", pages)

if page == "Introduction":
    st.title("Welcome to the Dota Data Analysis")
    st.markdown("""
    ### About this Project
    This project analyzes Dota 2 match data, including popular heroes, chat activity, and message quality.
    You can explore the data, view charts, and even add your own record to the dataset.
    """)

    st.markdown("""
    ### Navigation
    - **Introduction:** Overview
    - **Analytics:** Charts & insights
    - **Add Record:** Submit hero and chat message
    - **Hypothesis & Complex Graphs:** Deeper analysis & comparisons
    """)

elif page == "Analytics":
    st.title("Data Analytics")

    st.subheader("Top Heroes")
    top_n = st.slider("Select number of top heroes:", 1, 20, 10)
    df_heroes = get_top_heroes_data(top_n)
    if not df_heroes.empty:
        st.dataframe(df_heroes)
        fig_heroes = px.bar(df_heroes, x="localized_name", y="count", title="Top Heroes")
        st.plotly_chart(fig_heroes, use_container_width=True)
    else:
        st.warning("No hero data available.")

    st.subheader("Chat Activity")
    df_chat = get_chat_activity_data()
    if not df_chat.empty:
        st.dataframe(df_chat.head())
        fig_chat = px.histogram(df_chat, x="percent_players_in_chat", nbins=20, title="Distribution of % Players in Chat")
        st.plotly_chart(fig_chat, use_container_width=True)
    else:
        st.warning("No chat activity data.")

    st.subheader("Matches Stats")
    stats = get_matches_stats()
    if stats:
        labels = ['Matches with chat', 'Matches without chat']
        sizes = [stats["matches_with_chat"], stats["matches_without_chat"]]
        fig_matches = px.pie(values=sizes, names=labels, title="Percentage of Matches with Chat")
        st.plotly_chart(fig_matches, use_container_width=True)
    else:
        st.warning("No match stats data.")

    st.subheader("Bad Message Percentage")
    percentage = get_bad_message_percentage()
    if percentage is not None:
        st.write(f"**{percentage:.2f}%** of messages are profane.")
        labels = ['Profane', 'Not Profane']
        values = [percentage, 100 - percentage]
        fig_bad_msgs = px.pie(values=values, names=labels, title="Profane vs Non-Profane Messages")
        st.plotly_chart(fig_bad_msgs, use_container_width=True)
    else:
        st.warning("No profanity data available.")

elif page == "Hypothesis & Complex Graphs":
    st.title("Hypothesis and Complex Comparisons")

    st.markdown("""
    **Hypothesis:**  
    Teams that acquire Boots of Speed earlier have a higher chance of winning. Also, a higher early GPM 
    for the top 5 most popular heroes correlates with an increased likelihood of victory.
    """)

    st.subheader("First Boots of Speed Purchase Time: Winners vs Losers")
    resp_boots = requests.get("http://127.0.0.1:8000/api/boots_compare/")
    if resp_boots.status_code == 200:
        df_boots = pd.DataFrame(resp_boots.json())
        if not df_boots.empty:
            fig_box = px.box(df_boots, x='category', y='time', points='all',
                             title='First Boots of Speed Purchase Time: Winners vs Losers')
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.warning("No boots purchase data available.")
    else:
        st.error("Failed to fetch boots compare data.")

    st.markdown("""
    Interpretation:
    - If winners consistently show a lower median boots purchase time, it supports that early mobility helps win.
    """)

    st.subheader("Win Probability vs Early GPM for Top 5 Heroes")
    resp_gpm = requests.get("http://127.0.0.1:8000/api/hero_gpm_scatter_data/")
    if resp_gpm.status_code == 200:
        df_gpm = pd.DataFrame(resp_gpm.json())
        if not df_gpm.empty:
            fig_scatter = px.scatter(df_gpm, x='gpm_bin_center', y='win', color='hero_id', trendline='ols',
                                     title='Win Probability vs Early GPM for Top 5 Heroes')
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No hero GPM data available.")
    else:
        st.error("Failed to fetch hero GPM scatter data.")

    st.markdown("""
    Interpretation:
    - A positive trend suggests that higher early GPM in top heroes correlates with a higher win probability.
    """)

elif page == "Add Record":
    st.title("Add a New Record")
    st.markdown("Use the form below to add a hero and a chat message to the dataset.")

    with st.form("add_record_form"):
        hero_id = st.number_input("Hero ID", min_value=1, step=1)
        hero_name = st.text_input("Hero Name")
        chat_message = st.text_area("Chat Message")
        
        submitted = st.form_submit_button("Submit")
    
    if submitted:
        if hero_name.strip() == '' or chat_message.strip() == '':
            st.error("Hero name and chat message cannot be empty.")
        else:
            record_data = {
                "hero_id": hero_id,
                "hero_name": hero_name,
                "chat_message": chat_message
            }
            response = requests.post(cfg.ADD_RECORD_URL, json=record_data)
            if response.status_code == 200:
                st.success("Record added successfully!")
                st.json(response.json())
            else:
                st.error("Failed to add record.")
