import matplotlib.pyplot as plt
import random
import math

# Define the weight for each feature
weights = {
    "price_per_show": 0.3,
    "type": 0.15,
    "genre": 0.07,
    "language": 0.15,
    "booked_dates": 0.33
}

def cal_normal_distribution(x):
    return math.exp(-0.5 * (x)**2)

# Function to calculate individual feature scores
def calculate_feature_scores(artist, keywords):
    score = 0
    feature_scores = {}
    
    if "price_per_show" in keywords and artist["price_per_show"] <= keywords["price_per_show"]:
        feature_scores["price_per_show"] = weights["price_per_show"]*cal_normal_distribution(1 - (keywords['price_per_show']/artist['price_per_show']))
        score += weights["price_per_show"]*cal_normal_distribution(1 - (keywords['price_per_show']/artist['price_per_show']))
    else:
        feature_scores["price_per_show"] = 0

    if "type" in keywords and artist["type"] == keywords["type"]:
        feature_scores["type"] = weights["type"]
        score += weights["type"]
    else:
        feature_scores["type"] = 0

    if "genre" in keywords and artist["genre"] == keywords["genre"]:
        feature_scores["genre"] = weights["genre"]
        score += weights["genre"]
    else:
        feature_scores["genre"] = 0

    if "language" in keywords and artist["language"] == keywords["language"]:
        feature_scores["language"] = weights["language"]
        score += weights["language"]
    else:
        feature_scores["language"] = 0

    if "booked_dates" in keywords and keywords["booked_dates"] not in artist["booked_dates"]:
        feature_scores["booked_dates"] = weights["booked_dates"]
        score += weights["booked_dates"]
    else:
        feature_scores["booked_dates"] = 0

    return feature_scores, score

# Calculate feature scores for each artist and the query
artists = [
    {"id": i, "name": f"Artist {i}", "price_per_show": random.randint(1000, 10000),
     "type": random.choice(["singer", "dancer"]), "genre": random.choice(["pop", "classical", "jazz", "rock"]),
     "language": random.choice(["English", "Spanish", "French"]), "booked_dates": [f"2024-07-{random.randint(1, 30)}"],
     "other_details": f"Details for Artist {i}"} for i in range(1, 51)
]
keywords = {"price_per_show": 5000, "type": "singer", "genre": "pop", "language": "English", "booked_dates": "2024-07-15"}

artist_feature_scores, artist_score_ = [calculate_feature_scores(artist, keywords) for artist in artists]
query_feature_scores, _ = calculate_feature_scores(keywords, keywords)


# Plotting
plt.figure(figsize=(14, 8))
markers = ["o", "s", "D", "^", "v"]
colors = ["blue", "green", "orange", "purple", "cyan"]
features = ["price_per_show", "type", "genre", "language", "booked_dates"]

for i, feature in enumerate(features):
    artist_scores = [scores[feature] for scores in artist_feature_scores]
    query_score = query_feature_scores[feature]
    
    plt.scatter(range(len(artists)), artist_scores, marker=markers[i], color=colors[i], label=f'Artists - {feature}')
    plt.scatter(len(artists), query_score, marker=markers[i], color='red', label=f'Query - {feature}')
    
    for j, artist in enumerate(artists):
        plt.annotate(artist["id"], (j, artist_scores[j]), textcoords="offset points", xytext=(0, 5), ha='center')

# Annotate query point
plt.annotate('Query', (len(artists), query_score), textcoords="offset points", xytext=(0, 5), ha='center', color='red')

plt.xlabel('Artists')
plt.ylabel('Score')
plt.title('Artist Feature Scores and Query Score')
plt.legend()
plt.grid(True)
plt.show()
