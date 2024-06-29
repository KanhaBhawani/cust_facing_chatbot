import requests
import json
from artist_recomendation import find_artist

def extract_keywords(open_api_key, user_text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {open_api_key}",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": """
                You are an AI designed to extract specific keywords from a given text where a user is looking to book an artist for their special occasion. The text may include information about the date, budget, type of artist, genre, and other relevant details. Your task is to identify and extract the following keywords:
                
                1. **date**: The specific date or time period when the user wants to book the artist in '%Y-%m-%d' formate. If year is not mentioned, use current year ie. 2024
                2. **price_per_show**: The amount of money the user is willing to spend on the artist. Value should not contain any currency sign or any word (like thousand or million), it must be a integer value.
                3. **type**: The category of the artist, such as a singer, dancer, band, magician, etc. This value must only be 'singer', 'dancer', 'anchor', 'magician', etc..
                4. **genre**: The specific genre or style the user prefers, such as pop, classical, hip-hop, etc.
                5. **occasion**: The special event for which the user is booking the artist, such as a wedding, birthday party, corporate event, etc.
                6. **location**: The place or venue where the event will be held.
                7. **language**: Language of the artist
                8. **Other Specific Requirements**: Any additional preferences or requirements mentioned by the user.
                
                Extract the relevant keywords from the text and format them in JSON. Each keyword should be labeled according to its category. If any category is not mentioned in the text, you can leave it out.
                """
            },
            {
                "role": "user",
                "content": user_text,
            },
        ],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        output = response.json()['choices'][0]['message']['content']
        # print(output)
        return output
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return 404

# Example usage
open_api_key = ""
query = "I'm looking to book a pop singer for my wedding on July 15th. My budget is around $5000. The event will be held at Central Park in New York. I also need a sound system to be provided. Language should be Hindi"
# query = "Find a dancer for 9th june. I have a budget of 30 thousand"
response = extract_keywords(open_api_key, query)

if(response != 404):
    print(type(response))
    print(response)
    keywords = json.loads(response)
    print(type(keywords))
    print(keywords)
    find_artist(keywords)
