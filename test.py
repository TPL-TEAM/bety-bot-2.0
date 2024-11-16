import requests
import json

url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

querystring = {"Category":"soccer","Date":f"{20201028}","Timezone":"-7"}

headers = {
"X-RapidAPI-Key": "e97c4e8315mshb8683f3f9365d39p1c9e33jsnac8b822da9c5",
"X-RapidAPI-Host": "livescore6.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)  
mecze = json.loads(response.text)
for liga in mecze["Stages"]:
    print(mecze)