import json
import os
import sys
import requests
import gspread
from ostatnie import ostatnie_check

def resource_path(relpath):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relpath)

#sa = gspread.service_account(filename=resource_path("service_account.json"))
#sh = sa.open("Wyniki statystyk")
#bartek_arkusz = sh.worksheet("bartek")

def ogolne(data):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

    querystring = {"Category":"soccer","Date":f"{data}","Timezone":"-7"}

    headers = {
	    "x-rapidapi-key": "330f4d824fmshc955406d10d09cfp150f9ejsn3d0799cfeccb",
	    "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    mecze_dnia=json.loads(response.text)
    for ligi in mecze_dnia['Stages']:
        try:
            if ligi['CompId'] == '65' or ligi['CompId'] == '67' or ligi['CompId'] == '75' or ligi['CompId'] == '68' or ligi['CompId'] == '77' or ligi['CompId'] == '60':
                liga_Ccd=ligi['Ccd']
                liga_Scd=ligi['Scd']
                for liga in ligi['Events']:
                                id_meczu= int(liga["Eid"])
                                T1ID = liga['T1'][0]['ID']
                                T2ID = liga['T2'][0]['ID']
                                ostatnie_check(liga_Ccd,liga_Scd,id_meczu,T1ID,T2ID)      
            else:
                pass
        except:
             pass  

ogolne(input('wpisz date'))            