import csv
from imdb import IMDb

# Create an instance of the IMDb class
ia = IMDb()

# Define a function to bin the ratings
def bin_rating(rating):
    if rating is None:
        return None
    elif rating >= 8:
        return 4
    elif rating >= 7:
        return 3
    elif rating >= 4:
        return 2
    elif rating > 3:
        return 1
    else:
        return 0

# Open the CSV file
with open('./project_data/test_dataset.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # Create a new CSV file for writing the results
    with open('results.csv', 'w', newline='') as resultfile:
        fieldnames = ['id', 'imdb_score_binned']
        writer = csv.DictWriter(resultfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            movie_title = row['movie_title']
            movie_year = row['title_year']
            # Search for the movie by title
            movies = ia.search_movie(movie_title)
            if movies:
                # Filter movies by year if provided
                if movie_year:
                    filtered_movies = [movie for movie in movies if movie_year in str(movie.get('year', ''))]
                    if filtered_movies:
                        movie = filtered_movies[0]
                    else:
                        print(f"No movie found with title '{movie_title}' and year '{movie_year}'.")
                        writer.writerow({'id': row['id'], 'imdb_score_binned': -1})
                        continue
                else:
                    movie = movies[0]
                # Get movie rating
                ia.update(movie)
                rating = movie.data.get('rating')
                bin_number = bin_rating(float(rating)) if rating else None
                print(f"{movie_title} | {movie_year}' | {bin_number}")
                writer.writerow({'id': row['id'], 'imdb_score_binned': bin_number})
            else:
                print(f"No movie found with title '{movie_title}'.")