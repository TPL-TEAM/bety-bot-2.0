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

def ostatnie(liga_Ccd,liga_Scd,mecz_dnia, T1ID, T2ID):
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
                mecz_wlidze=0
                if mecz_dnia == mecz['Eid']:
                    mecz_wlidze-=1
                    licznik_T1=5
                    licznik_T1=5 
                    for i in dana_liga['Events']:
                        mecz_wlidze-=1
                        if T1ID == mecz_dnia['T1'] or T1ID == mecz_dnia['T2']:
                            licznik_T1 -=1
                            

                        if T2ID == mecz_dnia['T1'] or T2ID == mecz_dnia['T2']:
                            licznik_T2 -=1

                else:
                    mecz_wlidze+=1