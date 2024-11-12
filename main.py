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
wks = sh.worksheet("LIGI")

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
    for events in dane["Stages"]:
        for teams in events["Events"]:
            try:
                if(events['CompId'] == '65' or events['CompId'] == '67' or events['CompId'] == '75' or events['CompId'] == '68' or events['CompId'] == '77'): 
                    for team1 in teams['T1']:
                        querystring1 = {"ID":f"{team1['ID']}","Type":"short"}
                        tabela = requests.get(url1, headers=headers1, params=querystring1)
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
        ostatnia = wks.acell('A1').value
        cells = wks.range("D"f"{ostatnia}:L"f"{ostatnia}")
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
            wks.update_cells(cells)
            wks.update_cell(1,1,int(ostatnia)+1)
        except:
            print("Requesty się skończyły skurwysynu!")

    print("Plik został zaktualizowany!")

# check = multicheck(20231216)
# print(check)
while True:
    importdata(input("Wypisz date: "))

    print()
    input("Kliknij aby kontunułować")
    print()
    print()
    print()