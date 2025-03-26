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

sa = gspread.service_account(filename=resource_path("service_account.json"))
sh = sa.open("Wyniki statystyk")
bartek_arkusz = sh.worksheet("bartek")

def ogolne(data):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

    querystring = {"Category":"soccer","Date":f"{data}","Timezone":"-7"}

    headers = {
	    "x-rapidapi-key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
	    "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    mecze_dnia=json.loads(response.text)
    for ligi in mecze_dnia['Stages']:
        if ligi['CompId'] == '65' or ligi['CompId'] == '67' or ligi['CompId'] == '75' or ligi['CompId'] == '68' or ligi['CompId'] == '77':
            liga_Ccd=ligi['Ccd']
            liga_Scd=ligi['Scd']
            for liga in ligi['Events']:
                for mecz_dnia in liga:
                    id_meczu=mecz_dnia['Eid']
                    for druzyna1 in mecz_dnia['T1']:
                        url_ostatnie= "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"
                        querystring_ostatnie = {"Category":"soccer","Ccd":f"{liga_Ccd}","Scd":f"{liga_Scd}","Timezone":"-7"}
                        headers_ostatnie = {
	                        "x-rapidapi-key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
	                        "x-rapidapi-host": "livescore6.p.rapidapi.com"
                        }   
                        resposne_ostatnie = requests.get(url_ostatnie, headers=headers_ostatnie, params=querystring_ostatnie)
                        statystyki = json.loads(resposne_ostatnie.text)
                        for dana_liga in statystyki['Stages']:
                            for mecz in dana_liga['Events']:
                                if id_meczu == mecz['Eid']:
                                    pass
                                if mecz['t1'] == :
                                    mecz_sprawdzenie = 
