import pandas as pd
import pickle

# Load datasets
articles = pd.read_csv('data/shared_articles.csv')
interactions = pd.read_csv('data/users_interactions.csv')

# Load trained recommendation model
with open('models/model.pkl', 'rb') as f:
    model = pickle.load(f)

def get_recommendations(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return []

    # Get all unique articles
    all_articles = articles['contentId'].unique()

    # Get articles the user has already interacted with
    seen_articles = interactions[interactions['personId'] == user_id]['contentId'].unique()

    # Predict scores for unseen articles
    predictions = []
    for article_id in all_articles:
        if article_id not in seen_articles:
            pred = model.predict(user_id, article_id)
            predictions.append((article_id, pred.est))

    # Sort by highest predicted rating
    top_articles = sorted(predictions, key=lambda x: x[1], reverse=True)[:10]

    # Fetch recommended article details
    recommended_articles = articles[articles['contentId'].isin([a[0] for a in top_articles])][['contentId', 'title', 'url']]

    return recommended_articles.to_dict(orient='records')
