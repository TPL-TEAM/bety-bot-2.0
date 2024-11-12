import gspread
import requests

url = "https://allsportsapi2.p.rapidapi.com/api/tournament/8/schedules/31/10/2024"

headers = {
	"x-rapidapi-key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
	"x-rapidapi-host": "allsportsapi2.p.rapidapi.com"
}

response = requests.get(url, headers=headers)

print(response.json())