import random
import heapq
import math
import pandas as pd
import matplotlib.pyplot as plt

artists = [
    {"id": i, "name": f"Artist {i}", "price_per_show": random.randint(1000, 10000),
     "type": random.choice(["singer", "dancer"]), "genre": random.choice(["pop", "classical", "jazz", "rock"]),
     "language": random.choice(["English", "Spanish", "French"]), "booked_dates": [f"2024-07-{random.randint(1, 30)}"],
     "other_details": f"Details for Artist {i}"} for i in range(1, 51)
]

df_artists = pd.DataFrame(artists)
csv_file_path = './artists.csv'
df_artists.to_csv(csv_file_path, index=False)
# # Display the first 5 artists to check
# for artist in artists[:5]:
#     print(artist)
def cal_normal_distribution(x):
    return math.exp(-0.5 * (x - 1)**2)

def calculate_match_score(artist, keywords):
    score = 0
    weight = {
        "price_per_show": 0.3,
        "type": 0.15,
        "genre": 0.07,
        "language": 0.15,
        "booked_dates": 0.33
    }
    
    if "price_per_show" in keywords:
        score += weight['price_per_show']*cal_normal_distribution(keywords['price_per_show']/artist['price_per_show'])
    if "type" in keywords and artist["type"] == keywords["type"]:
        score += weight["type"]
    if "genre" in keywords and artist["genre"] == keywords["genre"]:
        score += weight["genre"]
    if "language" in keywords and artist["language"] == keywords["language"]:
        score += weight["language"]
    if "booked_dates" in keywords and keywords["booked_dates"] not in artist["booked_dates"]:
        score += weight["booked_dates"]

    return score

def find_matching_artists(artists, keywords, top_n=10):
    scored_artists = []
    
    for artist in artists:
        score = calculate_match_score(artist, keywords)
        heapq.heappush(scored_artists, (-score, artist))  # Use negative score for max-heap

    top_artists = [heapq.heappop(scored_artists)[1] for _ in range(min(top_n, len(scored_artists)))]
    
    return top_artists

# Example usage
keywords = {"price_per_show": 5000, "type": "singer", "genre": "pop", "language": "English", "booked_dates": "2024-07-15"}
query_score = 1.00
artist_scores = [calculate_match_score(artist, keywords) for artist in artists]

top_artists = find_matching_artists(artists, keywords)
for artist in top_artists:
    print(artist['id'])

for artist in artists:
    print("id: ", artist['id'])
    print(artist)
    print('\n\n')

plt.figure(figsize=(12, 8))
plt.scatter(range(len(artists)), artist_scores, label='Artists')
plt.scatter(len(artists), query_score, color='red', label='Query')

# Annotate artist IDs
for i, artist in enumerate(artists):
    plt.annotate(artist["id"], (i, artist_scores[i]), textcoords="offset points", xytext=(0, 5), ha='center')

# Annotate query point
plt.annotate('Query', (len(artists), query_score), textcoords="offset points", xytext=(0, 5), ha='center', color='red')

plt.xlabel('Artists')
plt.ylabel('Score')
plt.title('Artist Scores and Query Score')
plt.legend()
plt.grid(True)
plt.show()