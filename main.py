import streamlit as st
import pandas as pd
import numpy as np
import os
import recommenders as rec


title = "WBSFLIX+"
icon = "🍿"

# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title=title, page_icon=icon, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title(icon + " " + title)


genres_df = rec.get_genres()
movies_df = rec.get_movies()
ratings_df = rec.get_ratings()

## Top movies
top_movies = rec.get_popular_movies(ratings_df, movies_df)
top_movies

## Top movies by year (rating timestamp)
## Top movies by genre
## Item-based recommender
## User-based recommender
## 