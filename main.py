import streamlit as st
import pandas as pd
import numpy as np
import os
import recommenders as rec
import random


title = "WBSFLIX+"
icon = "🍿"

# https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config
st.set_page_config(page_title=title, page_icon=icon, layout="wide", initial_sidebar_state="auto", menu_items=None) #  layout="centered"
st.title(icon + " " + title)


genres_df = rec.get_genres()
movies_df = rec.get_movies_with_decade()
ratings_df = rec.get_ratings()
users_df = rec.get_user_ids()
total_movies = len(movies_df)
peopleById = {
    0: "...",
    99: "Zhanna",
    123: "Javier",
    234: "Shravanti",
    345: "Martin",
    456: "Vinita"
}



## Top movies
with st.container():
    st.header("🎬 Popular movies")
    all_genres = "..."
    genres_list = list(genres_df['genre'])
    genres_list.insert(0, all_genres)
    
    
    with st.form("filters_form"):
        st.write("Filters")
        
        col1, col2 = st.columns([1,1])

        with col1:
            genre = st.selectbox("🕵️‍♀️ Genre", genres_list)

        with col2:
            decade = st.slider("🗓 Decade", min_value=1900, max_value=2010, step=10, value=2010)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Apply")
        
    if submitted:
        clearFilters = st.button("Clear")
    
    movies_by_popularity = rec.get_popular_movies(ratings_df, movies_df, total_movies, 5)
    
    if submitted:
        if genre != all_genres:
            movies_by_popularity = movies_by_popularity[movies_by_popularity['genres'].str.contains(pat=r''+genre, case=False)]

        if decade:
            movies_by_popularity = movies_by_popularity[movies_by_popularity['decade'] == decade]
    
    movies_by_popularity = movies_by_popularity.head(10).reset_index()
    movies_by_popularity


## Item-based recommender
with st.container():
    st.header("👯 Similar movies")
    # currentMovieId = 356 # TODO: convert to search box + "search" button
    
    movieSearchInput = st.text_input("Search movie by title")
    foundTopN = pd.DataFrame([])
    selectedMovieId = None
    maxResults = 10
    
    if len(movieSearchInput) > 0:
        foundTopN = movies_df[movies_df['title'].str.contains(pat=r''+movieSearchInput, case=False)]
        foundTopN = foundTopN.head(maxResults)
        
    if len(foundTopN) > 0:
        foundDict = {}
        for i,found in foundTopN.iterrows():
            foundDict.update({found['movieId']: found['title']})

        selectedMovieId = st.radio("Select a result", foundDict.keys(), format_func = lambda movieId : foundDict[movieId])

        if selectedMovieId:
            st.success("Movies similar to '" + foundDict[selectedMovieId] + "'")
            similar_movies = rec.get_similar_movies(selectedMovieId, ratings_df, movies_df, 10, 15).reset_index()
            similar_movies
    else:
        if len(movieSearchInput) > 0:
            st.warning("No movies found")
        else:
            st.info("Enter a string to search a movie by title and hit ENTER.")


## User-based recommender
with st.container():
    st.header("🤍 Based on what other users like...")
    userSelection = st.selectbox("Who is watching?", peopleById.keys(), format_func = lambda userId : peopleById[userId])

    
    if userSelection > 0:
        found2 = rec.get_user_recommendations(userSelection, ratings_df, movies_df, n = 10).reset_index()
        
        if len(found2) > 0:
            st.success(f"{peopleById[userSelection]}, here is a list of movies you may like: ")
            found2
        else:
            st.info("No movies found")
    else:
        st.info("Select a user profile")

