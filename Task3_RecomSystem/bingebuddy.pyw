# importing required libraries
import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
import random

# Load and preprocess dataset
movies_df = pd.read_csv('tmdb_5000_movies.csv')
credits_df = pd.read_csv('tmdb_5000_credits.csv')
dataset = pd.merge(movies_df, credits_df, left_on='id', right_on='id', how='inner')

# Preprocessing steps
dataset['genres'] = dataset['genres'].apply(lambda x: ast.literal_eval(x))
dataset['spoken_languages'] = dataset['spoken_languages'].apply(lambda x: ast.literal_eval(x))
dataset['cast'] = dataset['cast'].apply(lambda x: ast.literal_eval(x))
dataset['crew'] = dataset['crew'].apply(lambda x: ast.literal_eval(x))

# Extracting genre names, language names, cast names, and director names
dataset['genre_names'] = dataset['genres'].apply(lambda x: [genre['name'] for genre in x])
dataset['language_names'] = dataset['spoken_languages'].apply(lambda x: [language['name'] for language in x])
dataset['cast_names'] = dataset['cast'].apply(lambda x: [cast_member['name'] for cast_member in x])
dataset['director_names'] = dataset['crew'].apply(lambda x: [crew_member['name'] for crew_member in x if crew_member['job'] == 'Director'])

dataset['combined_features'] = dataset['genre_names'].apply(lambda x: ' '.join(x)) + ' ' + \
                               dataset['language_names'].apply(lambda x: ' '.join(x)) + ' ' + \
                               dataset['cast_names'].apply(lambda x: ' '.join(x))


# ITF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(dataset['combined_features'])

# cosine Similarity matriex to calc. similar resutls
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get posters 
def scrape_poster_url(movie_title, release_date):
    query = f"{movie_title} {release_date} poster original"
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    image_tags = soup.find_all("img")
    if len(image_tags) > 1:  # Skip the first image as it's often the Google logo
        return image_tags[1]['src']  # Return the URL of the first image after the Google logo
    
    return None

#_-------------------------------------------------------------------------------

# Function to recommend movies
def recommend_movies(titles, cosine_sim=cosine_sim):
    sim_scores_aggregate = {}

    for title in titles:
        try:
            idx = dataset.index[dataset['title_x'].str.lower() == title.lower()].tolist()[0]
            sim_scores = list(enumerate(cosine_sim[idx]))

            for i, score in sim_scores:
                if i in sim_scores_aggregate:
                    sim_scores_aggregate[i] += score
                else:
                    sim_scores_aggregate[i] = score

        except IndexError:
            continue

    sim_scores_aggregate = sorted(sim_scores_aggregate.items(), key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in sim_scores_aggregate[:10]]

    # adding more recoms if <4 based on genres
    if len(movie_indices) < 4:
        remaining_needed = 4 - len(movie_indices)
        genres_of_titles = []
        for title in titles:
            try:
                idx = dataset.index[dataset['title_x'].str.lower() == title.lower()].tolist()[0]
                genres_of_titles.extend(dataset.loc[idx, 'genre_names'])
            except IndexError:
                pass
        
        genres_of_titles = list(set(genres_of_titles))
        genre_filtered_df = dataset[dataset['genre_names'].apply(lambda x: any(genre in x for genre in genres_of_titles))]
        genre_filtered_df = genre_filtered_df.sort_values(by='vote_average', ascending=False)
        additional_movies = genre_filtered_df[~genre_filtered_df['title_x'].str.lower().isin([dataset.loc[i, 'title_x'].lower() for i in movie_indices])]
        additional_movie_indices = additional_movies.head(remaining_needed).index.tolist()
        movie_indices.extend(additional_movie_indices)


    if len(movie_indices) < 4:
        remaining_needed = 4 - len(movie_indices)
        genre_filtered_df = dataset[dataset['genre_names'].apply(lambda x: any(genre in x for genre in genres_of_titles))]
        genre_filtered_df = genre_filtered_df[~genre_filtered_df['title_x'].str.lower().isin([dataset.loc[i, 'title_x'].lower() for i in movie_indices])]
        additional_movies = genre_filtered_df.sample(n=remaining_needed, random_state=1)
        additional_movie_indices = additional_movies.index.tolist()
        movie_indices.extend(additional_movie_indices)

    recommended_movies = dataset.iloc[movie_indices]
    recommended_movies = recommended_movies[~recommended_movies['title_x'].str.lower().isin([title.lower() for title in titles])]
    

    # Adding poster URL and cast names
    recommended_movies['poster_url'] = recommended_movies.apply(
        lambda row: scrape_poster_url(row['title_x'], row['release_date']), axis=1
    )
    recommended_movies['cast_names'] = recommended_movies['id'].map(dataset.set_index('id')['cast_names'])
    
    return recommended_movies[['title_x', 'overview', 'release_date', 'poster_url', 'cast_names']]



# Function to get a random high-rated movie (randomized)
def get_random_high_rated_movie():
    high_rated_df = dataset[dataset['vote_average'] >= 7.0]  # Adjust the rating threshold as needed
    random_movie = high_rated_df.sample(n=1).iloc[0]
    
    poster_url = scrape_poster_url(random_movie['title_x'], random_movie['release_date'])
    
    # Ensure `cast_names` is available
    cast_names = dataset.loc[dataset['id'] == random_movie['id'], 'cast_names'].values[0]
    cast_names = cast_names[:3]  # Get the first 3 cast members
    
    return pd.DataFrame([{
        'title_x': random_movie['title_x'],
        'overview': random_movie['overview'],
        'release_date': random_movie['release_date'],
        'poster_url': poster_url,
        'cast_names': cast_names
    }])


# GUI initialization
root = tk.Tk()
root.title("BingeBuddy: A Movie Recommendation System")
root.geometry("800x600")
root.resizable(False, False)

# colors
background_color = "#2E2E2E"  # Dark gray
frame_color = "#3C3C3C"  # light light gray
button_color = "#4CAF50"  # Green
button_text_color = "#ffffff"  # White
label_text_color = "#E0E0E0"  # Light gray

# INPUT FRAME
# Frame for movies input
frame_input = tk.Frame(root, padx=10, pady=10, relief=tk.RIDGE, borderwidth=2, bg=frame_color)
frame_input.pack(pady=10, fill=tk.X)
label_movies = tk.Label(frame_input, text="Enter up to 3 Movie Titles (Leave Blank for Random):", font=("Arial", 12), bg=frame_color, fg=label_text_color)
label_movies.pack(anchor=tk.W)

# Input fields for movie titles
entry_movie1 = tk.Entry(frame_input, font=("Arial", 12))
entry_movie1.pack(fill=tk.X, pady=5)

entry_movie2 = tk.Entry(frame_input, font=("Arial", 12))
entry_movie2.pack(fill=tk.X, pady=5)

entry_movie3 = tk.Entry(frame_input, font=("Arial", 12))
entry_movie3.pack(fill=tk.X, pady=5)


# RECOM FRAME
frame_recommendations = tk.Frame(root, padx=10, pady=10, bg=background_color)
frame_recommendations.pack(pady=10, fill=tk.BOTH, expand=True)

# canvas + scrollbar
canvas = tk.Canvas(frame_recommendations, bg=background_color, highlightthickness=0)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = ttk.Scrollbar(frame_recommendations, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a frame inside the canvas to hold recommendations
recommendation_frame = tk.Frame(canvas, bg=background_color)
canvas.create_window((0, 0), window=recommendation_frame, anchor='nw')

recommendation_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)



# Function for mouse wheel scrolling (was disabled due to canvas)
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
root.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows and macOS



# Function to display the recommendations
def display_recommendations(recommendations):
    for widget in recommendation_frame.winfo_children():
        widget.destroy()
    
    for idx, row in recommendations.iterrows():
        title = row['title_x']
        overview = row['overview']
        release_date = row['release_date']
        poster_url = row['poster_url']
        cast_names = row.get('cast_names', [])[:3]  # Get the first 3 cast members
        
        cast_display = ", ".join(cast_names) if cast_names else "Cast information not available"

        frame = tk.Frame(recommendation_frame, bg=frame_color)
        frame.pack(fill=tk.X, pady=10)
        
        # addign the poster
        try:
            response = requests.get(poster_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 150), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
            poster_label = tk.Label(frame, image=img_tk, bg=frame_color)
            poster_label.image = img_tk
            poster_label.pack(side=tk.LEFT, padx=10)
        except:
            poster_label = tk.Label(frame, text="Poster Not Available", bg=frame_color)
            poster_label.pack(side=tk.LEFT, padx=10)
        
        title_label = tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg=frame_color, fg=label_text_color)
        title_label.pack(anchor=tk.W)

        overview_label = tk.Label(frame, text=overview, font=("Arial", 10), wraplength=600, justify=tk.LEFT, bg=frame_color, fg=label_text_color)
        overview_label.pack(anchor=tk.W)
        
        release_date_label = tk.Label(frame, text=f"Release Date: {release_date}", font=("Arial", 10), bg=frame_color, fg=label_text_color)
        release_date_label.pack(anchor=tk.W)

        cast_label = tk.Label(frame, text=f"Cast: {cast_display}", font=("Arial", 10), bg=frame_color, fg=label_text_color)
        cast_label.pack(anchor=tk.W)


# Get recoms function 
def get_recommendations():
    titles = [entry_movie1.get(), entry_movie2.get(), entry_movie3.get()]
    titles = [title for title in titles if title.strip() != ""]

    if titles:
        recommendations = recommend_movies(titles)
    else:
        recommendations = get_random_high_rated_movie()
        
    display_recommendations(recommendations)


# recommend button

recom_btn = tk.Button(frame_input, text="Get Recommendations", command=get_recommendations, font=("Arial", 12), bg=button_color, fg=button_text_color)
recom_btn.pack(pady=10)

# run the main loop
root.mainloop()
