import streamlit as st
import pandas as pd
import requests
import pickle

with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]

    # top-10 similar indices, skip the first (same movie)
    sim_scores   = list(enumerate(cosine_sim[idx]))
    sim_scores   = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]

    # return **rows** so you still have movie_id, genres, etc.
    return movies.loc[movie_indices, ['movie_id', 'title']]


# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '3003e52880c3e815a8a64d0e2977593d'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path


# Streamlit UI
st.title("Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)

    cols = st.columns(5)
    for j, row in recommendations.reset_index(drop=True).iterrows():
        col = cols[j % 5]         # use 5-column grid
        with col:
            poster_url = fetch_poster(row['movie_id'])
            st.image(poster_url, width=130)
            st.caption(row['title'])

