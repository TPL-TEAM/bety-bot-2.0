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
    print("EID")
    url_mecz = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"

    querystring_mecz = {"Eid":f"{EID}","Category":"soccer"}

    headers_mecz = {
	"x-rapidapi-key": "330f4d824fmshc955406d10d09cfp150f9ejsn3d0799cfeccb",
	"x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    print("EID")
