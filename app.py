import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide"
)


API_KEY = "2c3bf2a4dba12726b500cdfbf8538042"

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url).json()

    poster_path = data['poster_path']

    return "https://image.tmdb.org/t/p/w500/" + poster_path
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    data = requests.get(url).json()

    return {
        "overview": data.get("overview", ""),
        "rating": data.get("vote_average", "N/A"),
        "release_date": data.get("release_date", "N/A"),
        "poster": "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
    }

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


st.markdown("""
<div style='text-align:center; padding:5px;'>
    <h1 style='font-size:60px; color:#E50914;'>🎬 CineMatch AI</h1>
    <h3>Find Hidden Gems And Blockbuster Movies 🍿</h3>
</div>
""", unsafe_allow_html=True)



selected_movie = st.selectbox(
    "Select a Movie",
    movies['title'].values
)
selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id

details = fetch_movie_details(selected_movie_id)

st.markdown("---")

with st.container():
    col1, col2 = st.columns([1,2])
with col1:
    st.image(details["poster"], width="stretch")
with col2:
    st.subheader(selected_movie)
    st.write(f"⭐ Rating: {details['rating']}")
    st.write(f"📅 Release Date: {details['release_date']}")
    st.write(details["overview"])

st.markdown("---")

if st.button("🍿 Get Recommendations"):
    st.subheader("🎬 Recommended For You")

    recommended_movies, recommended_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns([1.3,1.3,1.3,1.3,1.3])

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