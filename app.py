import streamlit as st
import pickle
import requests


API_KEY = "2c3bf2a4dba12726b500cdfbf8538042"

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url).json()

    poster_path = data['poster_path']

    return "https://image.tmdb.org/t/p/w500/" + poster_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_posters


st.title("🎬 CineMatch AI")
st.markdown("### 🎬 Find Hidden Gems And Blockbuster movies 🎥 ")

selected_movie = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

if st.button("Recommend"):

    recommended_movies, recommended_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommended_posters[0], use_container_width=True)
        st.caption(recommended_movies[0])

    with col2:
        st.image(recommended_posters[1], use_container_width=True)
        st.caption(recommended_movies[1])

    with col3:
        st.image(recommended_posters[2], use_container_width=True)
        st.caption(recommended_movies[2])

    with col4:
        st.image(recommended_posters[3], use_container_width=True)
        st.caption(recommended_movies[3])

    with col5:
       st.image(recommended_posters[4], use_container_width=True)
       st.caption(recommended_movies[4])