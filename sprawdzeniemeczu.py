import json
import os
import sys
import requests
import gspread

def resource_path(relpath):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relpath)

#sa = gspread.service_account(filename=resource_path("service_account.json"))
#sh = sa.open("Wyniki statystyk")
#bartek_arkusz = sh.worksheet("bartek")

def dany_mecz(EID):
    url_mecz = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"

    querystring_mecz = {"Eid":f"{EID}","Category":"soccer"}

    headers_mecz = {
	"x-rapidapi-key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
    	"x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    print(EID)
