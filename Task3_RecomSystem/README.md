# BingeBuddy: A Movie Recommendation System

**BingeBuddy** is a movie recommendation system developed to suggest movies based on user input or randomly suggest one. It utilizes content-based filtering techniques, including TF-IDF and cosine similarity, to provide personalized movie recommendations.


## Features
- **Movie Recommendations:** Suggests movies based on up to three movie titles entered by the user.
- **Random High-Rated Movies:** Provides a random high-rated movie recommendation if no titles are provided.
- **Poster Display:** Shows movie posters fetched from the web.
- **Cast Information:** Displays cast names for the recommended movies.


## Dependencies

- `pandas` - For data manipulation and analysis.
- `scikit-learn` - For machine learning utilities such as TF-IDF and cosine similarity.
- `tkinter` - For creating the graphical user interface.
- `requests` - For making HTTP requests to fetch movie posters.
- `beautifulsoup4` - For parsing HTML and extracting movie poster URLs.
- `pillow` - For image processing and displaying.

### Installation
You can install the necessary libraries using pip. Run the following command in your terminal:

```bash
- pip install pandas scikit-learn tkinter requests beautifulsoup4 pillow
```


## Technology Stack

- **Python:** Main programming language.
- **Pandas:** Data manipulation and analysis.
- **Scikit-learn:** For TF-IDF Vectorizer and cosine similarity.
- **Tkinter:** GUI framework for building the application interface.
- **Requests and BeautifulSoup:** For web scraping movie posters.
- **PIL (Pillow):** For handling and displaying images.


## Project Structure

**CodSoft Repo**
- **bingebuddy.pyw**: Main application file containing the Tkinter GUI and core logic. (pyw extension to open app without terminal window)
- **tmdb_5000_credits.csv**: dataset file for cast and credits
- **tmdb_5000_movies.csv**: dataset file for important movie details
- **README.md**: This file.


## License
This project is licensed under the MIT License - see the LICENSE file for details.


## Contact
For any questions or feedback, please contact:
- Name: Kaustubh Wagh
- Email: kaustubh.wagh@mitaoe.ac.in
- GitHub: kostawagh
