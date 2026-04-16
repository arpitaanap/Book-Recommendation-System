import pickle
from sklearn.neighbors import NearestNeighbors
from src.preprocessing import load_and_clean_data

def train_model():
    data = load_and_clean_data()

    pivot = data.pivot_table(index='user_id', columns='title', values='rating')
    pivot.fillna(0, inplace=True)

    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(pivot.T)

    # Save files
    pickle.dump(model, open('models/model.pkl', 'wb'))
    pickle.dump(pivot, open('models/pivot.pkl', 'wb'))

    print("Model trained and saved!")

if __name__ == "__main__":
    train_model()