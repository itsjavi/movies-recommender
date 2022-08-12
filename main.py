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
#  layout="centered"
st.title(icon + " " + title)


genres_df = rec.get_genres()
movies_df = rec.get_movies_with_decade()
ratings_df = rec.get_ratings()
users_df = rec.get_user_ids()
total_movies = len(movies_df)
    
## Top movies:

with st.container():
    st.header("🎬 Top movies of all time")
    top_movies = rec.get_popular_movies(ratings_df, movies_df, 10, 5).reset_index()
    top_movies

## Top movies by decade
with st.container():
    st.header("🗓 Top movies by decade")
    decades_list = range(2010,1900,-10)
    decade = st.selectbox("Decade", decades_list)
    
    top_movies3 = rec.get_popular_movies(ratings_df, movies_df, total_movies, 5)
    top_movies3 = top_movies3[top_movies3['decade'] == decade]
    top_movies3 = top_movies3.head(10).reset_index()
    top_movies3

## Top movies by genre
with st.container():
    st.header("🕵️‍♀️ Top movies by genre")
    all_genres = "(All)"
    genres_list = list(genres_df['genre'])
    genres_list.insert(0, all_genres)
    genre = st.selectbox("Genre", genres_list)
    
    if genre == all_genres:
        top_movies
    else:
        top_movies2 = rec.get_popular_movies(ratings_df, movies_df, total_movies, 5)
        top_movies2 = top_movies2[top_movies2['genres'].str.contains(pat=r''+genre, case=False)]
        top_movies2 = top_movies2.head(10).reset_index()
        top_movies2
    
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
            st.write("Movies similar to '" + foundDict[selectedMovieId] + "':")
            similar_movies = rec.get_similar_movies(selectedMovieId, ratings_df, movies_df, 10, 15).reset_index()
            similar_movies
    else:
        if len(movieSearchInput) > 0:
            st.warning("No movies found")
        else:
            st.info("Enter a string to search a movie by title and hit ENTER.")
    

peopleById = {
    99: "Zhanna",
    123: "Javier",
    234: "Shravanti",
    345: "Martin",
    456: "Vinita"
}
    
## User-based recommender
with st.container():
    st.header("🤍 Based on what other users like...")
    # currentMovieId = 356 # TODO: convert to search box + "search" button
    
    #randomUserId = random.choice(list(users_df['userId']))
    #col1,col2 = st.columns([1,1])
    
    #with col1:
    #    userIdInput = st.number_input("User ID", min_value=1, max_value=users_df['userId'].max(), step=1, value=randomUserId)
    
    #col2,col3 = st.columns([1,1])
    
    #with col2: 
    #    showBtn = st.button('Show')
    #    randomizeBtn = st.button('Randomize')
    
    userSelection = st.selectbox("Who is watching?", peopleById.keys(), format_func = lambda userId : peopleById[userId])

    
    if userSelection:
        found2 = rec.get_user_recommendations(userSelection, ratings_df, movies_df, n = 10).reset_index()
        
        if len(found2) > 0:
            st.write(f"{peopleById[userSelection]}, here is a list of movies you may like: ")
            found2
        else:
            st.info("No movies found")
 
    
    #if randomizeBtn:
    #    randomUserId = random.choice(list(users_df['userId']))
        