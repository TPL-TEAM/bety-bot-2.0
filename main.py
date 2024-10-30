import gspread
import requests

url = "https://football-highlights-api.p.rapidapi.com/leagues"

querystring = {"leagueName":"Premier League",}

headers = {
	"x-rapidapi-key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
	"x-rapidapi-host": "football-highlights-api.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())