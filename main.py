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
ligi = sh.worksheet("LIGI")
liczenie = sh.worksheet("Zyixu")
wyniki = sh.worksheet("wynik nowy")
i=0

def multicheck(Data):
    list1d = []
    ids = []
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

    querystring = {"Category":"soccer","Date":f"{Data}","Timezone":"-7"}

    headers = {
	"X-RapidAPI-Key": "e97c4e8315mshb8683f3f9365d39p1c9e33jsnac8b822da9c5",
	"X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    url1 = "https://livescore6.p.rapidapi.com/teams/get-table"
    headers1 = {
    "X-RapidAPI-Key": "e97c4e8315mshb8683f3f9365d39p1c9e33jsnac8b822da9c5",
	"X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }


    response = requests.get(url, headers=headers, params=querystring)  
    dane = json.loads(response.text)
    for events in dane["Stages"]: #events - liga
        for teams in events["Events"]: #tam gdzie sa teamy
            try:
                if(events['CompId'] == '65' or events['CompId'] == '67' or events['CompId'] == '75' or events['CompId'] == '68' or events['CompId'] == '77'): 
                    for team1 in teams['T1']:
                        querystring1 = {"ID":f"{team1['ID']}","Type":"short"} 
                        tabela = requests.get(url1, headers=headers1, params=querystring1) #tabela z danej ligi
                        tab = json.loads(tabela.text)
                        for i in range(0, 3):
                            lig1 = tab["LeagueTable"]["L"][0]["Tables"][0]["team"][i]['Tid']
                            if(lig1==team1['ID']):
                                rnk1 = tab["LeagueTable"]["L"][0]["Tables"][0]["team"][i]['rnk']
                                id1 = team1['ID']
                                break
                    for team2 in teams['T2']:
                        querystring1 = {"ID":f"{team2['ID']}","Type":"short"}
                        tabela = requests.get(url1, headers=headers1, params=querystring1)
                        tab = json.loads(tabela.text)
                        for i in range(0, 3):
                            lig2 = tab["LeagueTable"]["L"][0]["Tables"][0]["team"][i]['Tid']
                            if(lig2==team2['ID']):
                                rnk2 = tab["LeagueTable"]["L"][0]["Tables"][0]["team"][i]['rnk']
                                id2 = team2['ID']
                                break

                    if(abs(int(rnk1)-int(rnk2))>=5):
                        list1d.append(events['CompId'])
                        list1d.append(tab['Snm'])
                        list1d.append(id1)


                        list1d.append(id2)

            

                        ids.append(list1d)
                        list1d = []
            except:
                pass
    return(ids)


def importdata(Data):
    
    url = "https://livescore6.p.rapidapi.com/teams/get-team-stats"
    headers = {
	"X-RapidAPI-Key": "a8559155bbmsh63f4aa4a13fdd64p1edaecjsn43b00d3bfa30",
	"X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    check = multicheck(Data)
    for i in range(len(check)):
        if(check[i][0] == '12'):
            print("Nie posiadamy statystyk dla danego meczu(rozjebane api)")
            continue
        querystring = {"ID":f"{check[i][2]}","CompId":f"{check[i][0]}"}
        response = requests.get(url, headers=headers, params=querystring)
        data = json.loads(response.text)
        ostatnia = ligi.acell('A1').value
        cells = ligi.range("D"f"{ostatnia}:L"f"{ostatnia}")
        mecz = data['Pnm']+'-'
        strzaly = ''
        rozne = ''
        kartki = ''
        try:
            for events in data["statsGroup"]:
                if(events['name']== 'ATTACKING'):
                    for st in events["stats"]:
                        if(st['name'] == 'Shots'):
                            strzaly = str(st['pgValue'])
                        if(st['name'] == 'Shots on target'):
                            strzaly += '('+str(st['pgValue'])+')'
                        if(st['name'] == 'Corner Kicks'):
                            rozne = str(st['pgValue'])
                if(events['name']== 'DISCIPLINE'):
                    for st in events["stats"]:
                        if(st['name'] == 'Total cards'):
                            kartki = str(st['pgValue'])
            cells[3].value = strzaly
            cells[4].value = rozne
            cells[5].value = kartki
        except:
            print("Requesty się skończyły skurwysynu!")
        



        querystring = {"ID":f"{check[i][3]}","CompId":f"{check[i][0]}"}
        response = requests.get(url, headers=headers, params=querystring)
        data = json.loads(response.text)
        mecz += data['Pnm']
        strzaly = ''
        rozne = ''
        kartki = ''
        cells[0].value = check[i][1]
        cells[1].value = mecz
        try:
            for events in data["statsGroup"]:
                if(events['name']== 'ATTACKING'):
                    for st in events["stats"]:
                        if(st['name'] == 'Shots'):
                            strzaly = str(st['pgValue'])
                        if(st['name'] == 'Shots on target'):
                            strzaly += '('+str(st['pgValue'])+')'
                        if(st['name'] == 'Corner Kicks'):
                            rozne = str(st['pgValue'])
                if(events['name']== 'DISCIPLINE'):
                    for st in events["stats"]:
                        if(st['name'] == 'Total cards'):
                            kartki = str(st['pgValue'])
            cells[6].value = strzaly
            cells[7].value = rozne
            cells[8].value = kartki
            ligi.update_cells(cells)
            ligi.update_cell(1,1,int(ostatnia)+1)
        except:
            print("Requesty się skończyły skurwysynu!")

    print("Plik został zaktualizowany!")

# check = multicheck(20231216)
# print(check)

def szukanie(Data):
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

    querystring = {"Category":"soccer","Date":f"{Data}","Timezone":"-7"}

    headers = {
	    "X-RapidAPI-Key": "e97c4e8315mshb8683f3f9365d39p1c9e33jsnac8b822da9c5",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)  
    mecze = json.loads(response.text)
    for liga in mecze["Stages"]: #liga - tam gdzie jest CompId, Scd, Ccd
        for teams in liga["Events"]: #teams - element listy Events np. 0,1,2,3
            if(liga['CompId'] == '65' or liga['CompId'] == '67' or liga['CompId'] == '75' or liga['CompId'] == '68' or liga['CompId'] == '77'):
                Scd = liga["Scd"]
                Ccd = liga["Ccd"]
                Eid = teams["Eid"]



                querystring2 = {"Category":"soccer","Ccd":f"{Ccd}","Scd":f"{Scd}","Timezone":"-7"}
                url2 = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"
                headers2 = {
                    "X-RapidAPI-Key": "a8559155bbmsh63f4aa4a13fdd64p1edaecjsn43b00d3bfa30",
                    "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
                }
                response2 = requests.get(url2, headers=headers2, params=querystring2)
                statystyki = json.loads(response2.text)
                for liga2 in statystyki["Stages"]:
                    i = 0
                    for mecze2 in liga2["Events"]:
                        i += 1 
                        l = 0
                    
                        if mecze2['Eid']==Eid:
                            nr_mecz = i-1
                            team1_id = mecze2['T1'][0]['ID']
                            liczenie.update_cell(2,2,mecze2['T1'][0]['Nm'])
                            team2_id = mecze2['T2'][0]['ID']
                            liczenie.update_cell(2,6,mecze2['T2'][0]['Nm'])
                            g = int(liczenie.acell('A1').value)
                            h = int(liczenie.acell('A1').value)
                            print(l)
                            for mecze[nr_mecz] in liga2["Events"]:
                                if l == 20:
                                    break
                                
                                if mecze[nr_mecz]["T1"][0]["ID"] == team1_id:
                                    Eid2 = mecze[nr_mecz]["Eid"]

                                    url3 = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"

                                    headers3 = {
                                        "x-rapidapi-key": "c0cdcdef80mshc6be2a405fd46bdp19b6a0jsn46d775938a6b",
                                        "x-rapidapi-host": "livescore6.p.rapidapi.com"
                                    }
                                    
                                    querystring3 = {"Eid":f"{Eid2}","Category":"soccer"}
                                    
                                    response3 = requests.get(url3, headers=headers3, params=querystring3)
                                    wynik =  json.loads(response3.text)

                                    ilosc1 = int(wynik['Stat'][0]["Shon"]) + int(wynik['Stat'][0]["Shof"]) + int(wynik['Stat'][0]["Shbl"])
                                    liczenie.update_cell(g,2,ilosc1)

                                    ilosc2 = int(wynik['Stat'][1]["Shon"]) + int(wynik['Stat'][1]["Shof"]) + int(wynik['Stat'][1]["Shbl"])
                                    liczenie.update_cell(g,3,ilosc2)

                                    g += 1
                                    l += 1
                                
                                elif mecze[nr_mecz]["T2"][0]["ID"] == team1_id:
                                    Eid2 = mecze[nr_mecz]["Eid"]

                                    url3 = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"
                                    headers3 = {
                                        "x-rapidapi-key": "2407aecf96msh7ce6584ba4c80bap1ad1f9jsnf68f23cb6231",
                                        "x-rapidapi-host": "livescore6.p.rapidapi.com"
                                    }
                                    
                                    querystring3 = {"Eid":f"{Eid2}","Category":"soccer"}
                                    
                                    response3 = requests.get(url3, headers=headers3, params=querystring3)
                                    wynik =  json.loads(response3.text)
                                    
                                    ilosc1 = int(wynik['Stat'][0]["Shon"]) + int(wynik['Stat'][0]["Shof"]) + int(wynik['Stat'][0]["Shbl"])
                                    liczenie.update_cell(g,3,ilosc1)

                                    ilosc2 = int(wynik['Stat'][1]["Shon"]) + int(wynik['Stat'][1]["Shof"]) + int(wynik['Stat'][1]["Shbl"])
                                    liczenie.update_cell(g,2,ilosc2)

                                    g += 1
                                    l += 1


                                if mecze[nr_mecz]["T1"][0]["ID"] == team2_id:
                                    Eid2 = mecze[nr_mecz]["Eid"]

                                    url3 = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"

                                    headers3 = {
                                        "x-rapidapi-key": "cab57cb943msha12e2fe8f2b1e51p12c634jsn4e25e38d131b",
                                        "x-rapidapi-host": "livescore6.p.rapidapi.com"
                                    }
                                    
                                    querystring3 = {"Eid":f"{Eid2}","Category":"soccer"}
                                    
                                    response3 = requests.get(url3, headers=headers3, params=querystring3)
                                    wynik =  json.loads(response3.text)

                                    ilosc1 = int(wynik['Stat'][0]["Shon"]) + int(wynik['Stat'][0]["Shof"]) + int(wynik['Stat'][0]["Shbl"])
                                    liczenie.update_cell(h,6,ilosc1)

                                    ilosc2 = int(wynik['Stat'][1]["Shon"]) + int(wynik['Stat'][1]["Shof"]) + int(wynik['Stat'][1]["Shbl"])
                                    liczenie.update_cell(h,7,ilosc2)

                                    h += 1
                                    l += 1
                                    
                                elif mecze[nr_mecz]["T2"][0]["ID"] == team2_id:
                                    Eid2 = mecze[nr_mecz]["Eid"]
                                    
                                    url3 = "https://livescore6.p.rapidapi.com/matches/v2/get-statistics"

                                    headers3 = {
                                        "x-rapidapi-key": "02e6ed8605msh19d3aa305f9a302p1c5aabjsn70f9932c045a",
                                        "x-rapidapi-host": "livescore6.p.rapidapi.com"
                                    }
                                    
                                    querystring3 = {"Eid":f"{Eid2}","Category":"soccer"}
                                    
                                    response3 = requests.get(url3, headers=headers3, params=querystring3)
                                    wynik =  json.loads(response3.text)

                                    ilosc1 = int(wynik['Stat'][0]["Shon"]) + int(wynik['Stat'][0]["Shof"]) + int(wynik['Stat'][0]["Shbl"])
                                    liczenie.update_cell(h,7,ilosc1)

                                    ilosc2 = int(wynik['Stat'][1]["Shon"]) + int(wynik['Stat'][1]["Shof"]) + int(wynik['Stat'][1]["Shbl"])
                                    liczenie.update_cell(h,6,ilosc2)
                                    
                                    h += 1
                                    l += 1
                wyniki1()                
                                
                                
                                
                                
                                
                               

def wyniki1():
    ostatnia = int(wyniki.acell('A1').value)
    komorki = wyniki.range("C"f"{ostatnia}:J"f"{ostatnia}")
    komorki[0].value = liczenie.acell('B2').value
    komorki[1].value = liczenie.acell('B27').value
    komorki[2].value = liczenie.acell('B29').value
    komorki[3].value = liczenie.acell('B31').value
    komorki[4].value = liczenie.acell('F2').value
    komorki[5].value = liczenie.acell('F27').value
    komorki[6].value = liczenie.acell('F29').value
    komorki[7].value = liczenie.acell('F31').value

    wyniki.update_cells(komorki)

    komorki = ligi.range("C"f"{ostatnia+1}:J"f"{ostatnia+1}")
    komorki[0].value = "oponent"
    komorki[1].value = liczenie.acell('C27').value
    komorki[2].value = liczenie.acell('C29').value
    komorki[3].value = liczenie.acell('C31').value
    komorki[4].value = "oponent"
    komorki[5].value = liczenie.acell('G27').value
    komorki[6].value = liczenie.acell('G29').value
    komorki[7].value = liczenie.acell('G31').value

    wyniki.update_cells(komorki)
    wyniki.update_cell(1,1,ostatnia+1)
    

while True:
    szukanie(input("Wypisz date: "))

    print()
    input("Kliknij aby kontunułować")
    print()
    print()
    print()