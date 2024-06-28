import random
import heapq
import math
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


''' variables '''
# weight = {
#     "price_per_show": 0.275,
#     "type": 0.2,
#     "genre": 0.05,
#     "language": 0.2,
#     "date": 0.275
# }
weight = {
    "price_per_show": 0.15,
    "type": 0.20,
    "genre": 0.10,
    "language": 0.25,
    "date": 0.3
}
num_artist = 100
num_top = 10

class Artist:
    def __init__(self):
        self.artists = [
            {
                "id": i,
                "name": f"Artist {i}",
                "price_per_show": random.randint(1000, 10000),
                "type": random.choice(["singer", "dancer", "anchor", "musician", "comedian"]),
                "genre": random.choice(["pop", "classical", "jazz", "rock", "melody", "hiphop"]),
                "language": random.choice(["English", "Spanish", "French", "hindi", "sanskrit"]),
                "booked_dates": [f"2024-07-{random.randint(1, 30)}"],
                "other_details": f"Details for Artist {i}"
            } for i in range(1, num_artist)
        ]
        # Convert date strings to datetime objects
        for artist in self.artists:
            artist["booked_dates"] = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in artist["booked_dates"]]

    def get_artist(self):
        return self.artists

def cal_normal_distribution(x):
    return math.exp(-0.5 * (x - 1)**2)



def calculate_match_score(artist, keywords):
    score = 0
    
    if "price_per_show" in keywords:
        score += weight['price_per_show'] * cal_normal_distribution(keywords['price_per_show'] / artist['price_per_show'])
    if "type" in keywords and artist["type"] == keywords["type"]:
        score += weight["type"]
    if "genre" in keywords and artist["genre"] == keywords["genre"]:
        score += weight["genre"]
    if "language" in keywords and artist["language"] == keywords["language"]:
        score += weight["language"]
    if "date" in keywords:
        query_date = datetime.strptime(keywords["date"], "%Y-%m-%d")
        days_diff = min([abs((query_date - booked_date).days) for booked_date in artist["booked_dates"]])
        score += weight["date"] * cal_normal_distribution(days_diff)

    return score

def cal_query_score(keywords):
    score = 0
    
    if "price_per_show" in keywords:
        score += weight['price_per_show']
    if "type" in keywords:
        score += weight["type"]
    if "genre" in keywords:
        score += weight["genre"]
    if "language" in keywords:
        score += weight["language"]
    if "date" in keywords:
        score += weight["date"] 

    return score

def find_matching_artists(artists, keywords, top_n=num_top):
    scored_artists = []
    
    for artist in artists:
        score = calculate_match_score(artist, keywords)
        # print(score)
        # print(type(score))
        heapq.heappush(scored_artists, (-score, artist['id']))  # Use negative score for max-heap

    top_artists = [heapq.heappop(scored_artists)[1] for _ in range(min(top_n, len(scored_artists)))]

    return top_artists 

# Example usage
def find_artist(keywords):
    artist = Artist()
    artists = artist.get_artist()
    # for artist in artists:
    #     print(artist['id'])
    #     print(artist)
    #     print()

    query_score = cal_query_score(keywords)
    print("query score= ", query_score)
    print(type(keywords['price_per_show']))
    artist_scores = [calculate_match_score(artist, keywords) for artist in artists]

    top_artists = find_matching_artists(artists, keywords)
    for id in top_artists:
        print(id, ", similarity: ", artist_scores[id - 1], " ", artist_scores[id - 1]/query_score)


    ''' Show Data '''
    data = []
    for id in top_artists:
        artist = artists[id-1]
        data.append({
            "ID": id,
            "Name": artist['name'],
            "Price per Show": artist['price_per_show'],
            "Type": artist['type'],
            "Genre": artist['genre'],
            "Language": artist['language'],
            "Booked Dates": ", ".join([date.strftime("%Y-%m-%d") for date in artist['booked_dates']]),
            "Other Details": artist['other_details'],
            "Score": calculate_match_score(artist, keywords)
        })
    
    query_data = [{
        "ID": "Query",
        "Name": "Query",
        "Price per Show": keywords.get('price_per_show', "N/A"),
        "Type": keywords.get('type', "N/A"),
        "Genre": keywords.get('genre', "N/A"),
        "Language": keywords.get('language', "N/A"),
        "Booked Dates": keywords.get('date', "N/A"),
        "Other Details": "N/A",
        "Score": query_score
    }]
    
    data = query_data + data
    df = pd.DataFrame(data)
    
    # Display the DataFrame
    print(df)


    ''' Plotting '''
    # plt.figure(figsize=(12, 8))
    # plt.scatter(range(len(artists)), artist_scores, label='Artists')
    # plt.scatter(len(artists), query_score, color='red', label='Query')

    # # Annotate artist IDs
    # for i, artist in enumerate(artists):
    #     plt.annotate(artist["id"], (i, artist_scores[i]), textcoords="offset points", xytext=(0, 5), ha='center')

    # # Annotate query point
    # plt.annotate('Query', (len(artists), query_score), textcoords="offset points", xytext=(0, 5), ha='center', color='red')

    # plt.xlabel('Artists')
    # plt.ylabel('Score')
    # plt.title('Artist Scores and Query Score')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

# Example keywords
if __name__ == "__main__":
    keywords = {'date': '2024-07-09', 'price_per_show': 5000, 'type': 'dancer', 'genre': "pop", "language": "English"}
    find_artist(keywords)
