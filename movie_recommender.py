import pandas as pd
import ast

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load datasets
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# Merge datasets
movies = movies.merge(credits, on='title')

# Select useful columns
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# Remove null values
movies.dropna(inplace=True)

# Convert genres and keywords
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

# Take top 3 cast members
def convert3(obj):
    L = []
    counter = 0

    for i in ast.literal_eval(obj):
        if counter != 3:
            L.append(i['name'])
            counter += 1
        else:
            break

    return L

# Extract director
def fetch_director(obj):
    L = []

    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            L.append(i['name'])
            break

    return L

# Apply transformations
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert3)
movies['crew'] = movies['crew'].apply(fetch_director)

# Convert overview to list
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# Remove spaces
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Create tags
movies['tags'] = (
    movies['overview']
    + movies['genres']
    + movies['keywords']
    + movies['cast']
    + movies['crew']
)

# New dataframe
new_df = movies[['movie_id', 'title', 'tags']]

# Convert tags list to string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# Convert to lowercase
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
new_df = new_df.head(1000)
# Vectorization
cv = CountVectorizer(max_features=5000, stop_words='english')

vectors = cv.fit_transform(new_df['tags']).toarray()

print("Vector Shape:", vectors.shape)

# Cosine Similarity
similarity = cosine_similarity(vectors)

print("Similarity Shape:", similarity.shape)

# Recommendation Function
def recommend(movie):

    movie_index = new_df[new_df['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    print("\nRecommended Movies:\n")

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

# Test
recommend('Avatar')
import pickle

# Save movie dataframe
pickle.dump(new_df, open('movie_list.pkl', 'wb'))

# Save similarity matrix
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Pickle files created successfully!")