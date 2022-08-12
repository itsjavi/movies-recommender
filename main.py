import streamlit as st
import pandas as pd
import numpy as np
import os
import recommenders as rec
import random


title = "WBSFLIX+"
icon = "🍿"

# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title=title, page_icon=icon, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title(icon + " " + title)


genres_df = rec.get_genres()
movies_df = rec.get_movies()
ratings_df = rec.get_ratings()
users_df = rec.get_user_ids()

## Top movies:

with st.container():
    st.header("Top movies of all time")
    top_movies = rec.get_popular_movies(ratings_df, movies_df, 10, 5)
    top_movies

## Top movies by year (rating timestamp)
## Top movies by genre
with st.container():
    st.header("Top movies by Genre")
    all_genres = "(All)"
    genres_list = list(genres_df['genre'])
    genres_list.insert(0, all_genres)
    genre = st.selectbox("Genre", genres_list)
    
    if genre == all_genres:
        top_movies
    else:
        top_movies2 = rec.get_popular_movies(ratings_df, movies_df, 5000, 5)
        top_movies2 = top_movies2[top_movies2['genres'].str.match(pat=r''+genre, case=False)]
        top_movies2 = top_movies2.head(10)
        top_movies2
    
## Item-based recommender
with st.container():
    st.header("Similar movies")
    # currentMovieId = 356 # TODO: convert to search box + "search" button
    
    movieSearchInput = st.text_input("Movie title")
    
    if st.button('Search') and len(movieSearchInput) > 0:
        found = movies_df[movies_df['title'].str.match(pat=r''+movieSearchInput, case=False)]
        found = found.head(1)
        
        if len(found) > 0:
            found = found.reset_index().iloc[0]
            st.write("Movies similar to '" + found['title'] + "':")
            similar_movies = rec.get_similar_movies(found['movieId'], ratings_df, movies_df, 10, 15)
            similar_movies
        else:
            st.info("No movies found")
    

## User-based recommender
with st.container():
    st.header("Based on what other users like...")
    # currentMovieId = 356 # TODO: convert to search box + "search" button
    
    randomUserId = random.choice(list(users_df['userId']))
    
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        userIdInput = st.number_input("User ID", min_value=1, max_value=users_df['userId'].max(), step=1, value=randomUserId)
    
    with col2: 
        showBtn = st.button('Show')
    
    with col3:
        randomizeBtn = st.button('Randomize')

    
    if showBtn or userIdInput > 0:
        found2 = rec.get_user_recommendations(userIdInput, ratings_df, movies_df, n = 10)
        
        if len(found2) > 0:
            st.write(f"Recommendations based on user '{userIdInput}':")
            found2
        else:
            st.info("No movies found")
 
    
    if randomizeBtn:
        randomUserId = random.choice(list(users_df['userId']))
        