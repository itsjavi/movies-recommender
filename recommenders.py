import pandas as pd
import numpy as np
import streamlit as st

"""
TODOS:
 - Ability to search by movie title (match as "OR" by every word)  
   
 - Add a "year" column to the ratings, based on "timestamp" column, 
   so we can display most popular movies by year.
   
 - Create functions for linear-regression and Knn algorithms
 
 
OPTIMIZATIONS:

 - To have a more optimal web application, we could save the ratings means and the
   merge with the movies as csv file, and load that one instead of calculating
   everything again over and over. The same for the users ratings.
 
 - That would make our app "static", but in a real world scenario the data would be dynamic
   and loaded from an API or Database, so it would be calculated on the fly.

"""

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


def get_ratings_means_count(ratings_df):
    ratings = pd.DataFrame(ratings_df.groupby('movieId')['rating'].mean())
    ratings['rating_count'] = ratings_df.groupby('movieId')['rating'].count()
    
    return ratings


# simple ranking
def get_popular_movies(ratings_df, movies_df, n = 10, min_ratings = 5):
    ratings = get_ratings_means_count(ratings_df)
    
    popular_movies = (ratings
        .merge(movies_df, on='movieId')
        .sort_values(["rating_count", "rating"], ascending=[False, False])
    )
    
    return popular_movies[popular_movies['rating_count']>=min_ratings].head(n)


# get movie index,id tuple from highest ranged
def get_most_popular_movie(popular_movies):
    mostPopularMovie = popular_movies.head(1)
    mostPopularMovieIdx = mostPopularMovie.index[0]
    mostPopularMovieId = mostPopularMovie['movieId'][mostPopularMovieIdx]
    
    return [mostPopularMovieIdx, mostPopularMovieId]


# item-based recommender
def get_similar_movies(movieId, ratings_df, movies_df, n = 10, min_ratings = 10):
    ratings_mean_df = get_ratings_means_count(ratings_df)
    movies_crosstab = pd.pivot_table(data=ratings_df, values='rating', index='userId', columns='movieId')
    
    # Replace NaNs with zeros
         # not doing this gives different results??
    movies_crosstab = movies_crosstab.fillna(0, inplace=False)
    
    popular_ratings = movies_crosstab[movieId]
    popular_ratings[popular_ratings>=0] # exclude NaNs in the pivot table cross tab
    
    # Find PearsonR correlation
    similar_corr = pd.DataFrame(movies_crosstab.corrwith(popular_ratings), columns=['PearsonR_Value'])
    similar_corr = similar_corr.dropna(inplace=False) # exclude NaNs in the corr matrix
    
    similar_summary = similar_corr.join(ratings_mean_df['rating_count'])
    similar_summary = similar_summary.drop(
        movieId, inplace=False
    ) # drop popular movie itself
    
    return (similar_summary[similar_summary['rating_count']>=min_ratings]
            .sort_values(['PearsonR_Value', 'rating_count'], ascending=[False,False])
            .merge(movies_df, left_index=True, right_on="movieId")
            .head(n)
          )

# user-based recommender
def get_user_recommendations(for_user_id, ratings_df, movies_df, n = 10):
    # Create the big users-items table, using the userId as index.
    users_items = pd.pivot_table(data=ratings_df, values='rating', index='userId', columns='movieId')
    
    # Replace NaNs with zeros
    users_items = users_items.fillna(0, inplace=False)
    
    # Compute pairwise cosine similarities
    user_similarities = pd.DataFrame(
        cosine_similarity(users_items),
        columns=users_items.index, 
        index=users_items.index
    )
    
    # build recommender system
    ## compute weights, excluding target user
    
    user_similarities_excl = user_similarities.query("userId!=@for_user_id")[for_user_id]
    user_similarities_excl_sums = sum(user_similarities_excl)
    weights = (user_similarities_excl / user_similarities_excl_sums)
    
    ## find movies that target user did not rate yet
    users_items.loc[for_user_id,:]==0

    not_rated_movies = users_items.loc[users_items.index!=for_user_id, users_items.loc[for_user_id,:]==0]

    ## predict/compute the ratings target user would give to those unrated restaurants.
    
    ### dot product between the not-rated-movies and the weights
    weighted_averages = pd.DataFrame(not_rated_movies.T.dot(weights), columns=["predicted_rating"])
    
    ## find the top N movies from the rating predictions
    recommendations = weighted_averages.merge(movies_df, left_index=True, right_on="movieId")
    recommendations = recommendations.sort_values("predicted_rating", ascending=False).head(n)
    
    return recommendations

