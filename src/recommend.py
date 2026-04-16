import pickle

# Load saved files
model = pickle.load(open('models/model.pkl', 'rb'))
pivot = pickle.load(open('models/pivot.pkl', 'rb'))

def recommend_books(book_name):
    if book_name not in pivot.columns:
        return ["Book not found"]

    book_index = list(pivot.columns).index(book_name)

    distances, indices = model.kneighbors(
        pivot.T.iloc[book_index].values.reshape(1, -1),
        n_neighbors=5
    )

    recommendations = []
    for i in indices[0]:
        recommendations.append(pivot.columns[i])

    return recommendations