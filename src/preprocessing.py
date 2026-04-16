import pandas as pd

def load_and_clean_data():
    # Load data
    books = pd.read_csv('data/books.csv')
    ratings = pd.read_csv('data/ratings.csv')

    # Merge datasets
    data = ratings.merge(books, on='book_id')

    # Remove duplicates
    data.drop_duplicates(inplace=True)

    # Remove users with very few ratings
    user_counts = data['user_id'].value_counts()
    data = data[data['user_id'].isin(user_counts[user_counts > 5].index)]

    return data