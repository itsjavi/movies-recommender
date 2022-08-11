import streamlit as st
import pandas as pd
import numpy as np
import os


title = "WBSFLIX+"
icon = "🍿"

# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title=title, page_icon=icon, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title(icon + " " + title)


@st.cache
def get_movies():
    return pd.read_csv("data/movies-tags.csv")

@st.cache
def get_genres():
    return pd.read_csv("data/genres.csv")

    return genres

@st.cache
def get_ratings():
    return pd.read_csv("data/ratings.csv")

@st.cache
def get_user_ids():
    return pd.read_csv("data/users.csv")


df = get_genres()

df

## Top movies by year (rating timestamp)
## Top movies by genre
## Item-based recommender
## User-based recommender
## 