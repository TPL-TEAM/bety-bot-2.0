import json
import discord
import requests
from discord.ext import commands
from discord import app_commands
import gspread
import os

PREFIX = 'bet.'
INTENTS = discord.Intents().all()
bot = commands.Bot(command_prefix = PREFIX, intents = INTENTS)
TOKEN = 'MTE3NDY3OTQ5NTc3MzUxOTk2Mw.G76s8L.Xmy-19JWj2n1fIpj_KFbZdMgmiUjSycDzbjD9I'
limit = 0
channel = 1175378219277496341

sa = gspread.service_account(filename="service_account.json")
sh = sa.open("Wyniki statystyk")
wks = sh.worksheet("LIGI")

def checkid(Data, team):
    
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

    querystring = {"Category":"soccer","Date":f"{Data}","Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)  
    data = json.loads(response.text)
    for events in data["Stages"]:
        try:
            compid = events["CompId"]
        except:
            compid = 12 
        for teams in events["Events"]:
            team1 = teams["T1"]
            team2 = teams["T2"]
            id1 = team1[0]["ID"]
            id2 = team2[0]["ID"]
            name1 = team1[0]["Nm"]
            name2 = team2[0]["Nm"]
            if name1 == team or name2 == team:
                # print(id1, id2)
                # print(name1, name2)
                # print(compid)
                return (id1, id2, compid)


def multicheck(Data):
    list1d = []
    ids = []
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"

    querystring = {"Category":"soccer","Date":f"{Data}","Timezone":"-7"}

    headers = {
        "X-RapidAPI-Key": "fb7333cf2fmsh68563e68f422bcep1a2071jsncb99c4caaf88",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)  
    dane = json.loads(response.text)
    for events in dane["Stages"]:
        for teams in events["Events"]:
            try:
                list1d.append(events['CompId'])
            except:
                list1d.append('12')
                continue
            for team1 in teams['T1']:
                list1d.append(team1['ID'])

            for team2 in teams['T2']:
                list1d.append(team2['ID'])

            ids.append(list1d)
            list1d = []
    return(ids)



@bot.tree.command(name="check")
@app_commands.describe(rok="Podaj rok meczu" ,miesiac="Podaj miesiac meczu", dzien="Podaj dzien meczu", team="podaj druzyne")
async def check(
    interaction: discord.Interaction,
    rok: app_commands.Range[int, 1000, 9999],
    miesiac: app_commands.Range[int, 1, 12],
    dzien: app_commands.Range[int, 1, 31],
    team: str
):
    if(miesiac<10 and len(str(miesiac))<2):
        miesiac='0'+str(miesiac)
    if(dzien<10 and len(str(dzien))<2):
        dzien='0'+str(dzien)
    Data=str(rok)+str(miesiac)+str(dzien)
    check = checkid(Data, team)
    if(check[2] == '12'):
        await interaction.response.send("Nie posiadamy statystyk dla danego meczu(rozjebane api)")
    url = "https://livescore6.p.rapidapi.com/teams/get-team-stats"
    headers = {
        "X-RapidAPI-Key": "b737119a51mshe4651cd13badc03p18b663jsnab1f3e78a151",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    querystring = {"ID":f"{check[0]}","CompId":f"{check[2]}"}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    # print(data)
    await interaction.channel.send(f'# {data["Pnm"]}')
    prt = ''
    try:
        for events in data["statsGroup"]:
            prt += f'## {events["name"]} \n\n'
            for st in events["stats"]:
                prt += f'### {st["name"]} \n'
                try:
                    prt += f'Ilość: {st["totalValue"]} Średnia: {st["pgValue"]} Ranga w lidze: {st["rank"]}\n'
                except:
                    prt += f'Ilość: {st["totalValue"]} Średnia: --- Ranga w lidze: {st["rank"]}\n'
        await interaction.channel.send(f'{prt}')
    except:
        await interaction.channel.send(f"Nie posiadamy statystyk dla {check[3]} (rozjebane api)")                


    querystring = {"ID":f"{check[1]}","CompId":f"{check[2]}"}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    await interaction.channel.send(f'# {data["Pnm"]}')
    prt = ''
    try:
        for events in data["statsGroup"]:
            prt += f'## {events["name"]} \n\n'
            for st in events["stats"]:
                prt += f'### {st["name"]} \n'
                try:
                    prt += f'Ilość: {st["totalValue"]} Średnia: {st["pgValue"]} Ranga w lidze: {st["rank"]}\n'
                except:
                    prt += f'Ilość: {st["totalValue"]} Średnia: --- Ranga w lidze: {st["rank"]}\n'
        await interaction.channel.send(f'{prt}')
    except:
        await interaction.channel.send(f"Nie posiadamy statystyk dla {check[4]} (rozjebane api)")

@bot.tree.command(name="importdata")
@app_commands.describe(rok="Podaj rok meczu" ,miesiac="Podaj miesiac meczu", dzien="Podaj dzien meczu", team="podaj druzyne")
async def importdata(
    interaction: discord.Interaction,
    rok: app_commands.Range[int, 1000, 9999],
    miesiac: app_commands.Range[int, 1, 12],
    dzien: app_commands.Range[int, 1, 31],
    team: str
):
    if(miesiac<10 and len(str(miesiac))<2):
        miesiac='0'+str(miesiac)
    if(dzien<10 and len(str(dzien))<2):
        dzien='0'+str(dzien)
    Data=str(rok)+str(miesiac)+str(dzien)
    url = "https://livescore6.p.rapidapi.com/teams/get-team-stats"
    headers = {
        "X-RapidAPI-Key": "b737119a51mshe4651cd13badc03p18b663jsnab1f3e78a151",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    check = checkid(Data, team)
    if(check[2] == '12'):
        await interaction.response.send("Nie posiadamy statystyk dla danego meczu(rozjebane api)")
    querystring = {"ID":f"{check[0]}","CompId":f"{check[2]}"}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    ostatnia = wks.acell('A1').value
    mecz = data['Pnm']+'-'
    strzaly = ''
    rozne = ''
    kartki = ''
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
    wks.update_cell(ostatnia, 7, strzaly)
    wks.update_cell(ostatnia, 8, rozne)
    wks.update_cell(ostatnia, 9, kartki)



    querystring = {"ID":f"{check[1]}","CompId":f"{check[2]}"}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    mecz += data['Pnm']
    strzaly = ''
    rozne = ''
    kartki = ''
    wks.update_cell(ostatnia, 5, mecz)
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
    wks.update_cell(ostatnia, 10, strzaly)
    wks.update_cell(ostatnia, 11, rozne)
    wks.update_cell(ostatnia, 12, kartki)
    wks.update(range_name='A1', values=int(ostatnia)+1)

    await interaction.channel.send("Plik został zaktualizowany!")


##################################################################################
##################################################################################
##################################################################################
##################################################################################

@bot.tree.command(name="multiimport")
@app_commands.describe(rok="Podaj rok meczu" ,miesiac="Podaj miesiac meczu", dzien="Podaj dzien meczu")
async def importdata(
    interaction: discord.Interaction,
    rok: app_commands.Range[int, 1000, 9999],
    miesiac: app_commands.Range[int, 1, 12],
    dzien: app_commands.Range[int, 1, 31],
):
    if(miesiac<10 and len(str(miesiac))<2):
        miesiac='0'+str(miesiac)
    if(dzien<10 and len(str(dzien))<2):
        dzien='0'+str(dzien)
    Data=str(rok)+str(miesiac)+str(dzien)
    url = "https://livescore6.p.rapidapi.com/teams/get-team-stats"
    headers = {
        "X-RapidAPI-Key": "b737119a51mshe4651cd13badc03p18b663jsnab1f3e78a151",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    check = multicheck(Data)
    for i in range(len(check)):
        if(check[i][0] == '12'):
            await interaction.channel.send("Nie posiadamy statystyk dla danego meczu(rozjebane api)")
            continue
        querystring = {"ID":f"{check[i][1]}","CompId":f"{check[i][0]}"}
        response = requests.get(url, headers=headers, params=querystring)
        data = json.loads(response.text)
        ostatnia = wks.acell('A1').value
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
            wks.update_cell(ostatnia, 7, strzaly)
            wks.update_cell(ostatnia, 8, rozne)
            wks.update_cell(ostatnia, 9, kartki)
        except:
            pass



        querystring = {"ID":f"{check[i][2]}","CompId":f"{check[i][0]}"}
        response = requests.get(url, headers=headers, params=querystring)
        data = json.loads(response.text)
        mecz += data['Pnm']
        strzaly = ''
        rozne = ''
        kartki = ''
        try:
            wks.update_cell(ostatnia, 5, mecz)
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
            wks.update_cell(ostatnia, 10, strzaly)
            wks.update_cell(ostatnia, 11, rozne)
            wks.update_cell(ostatnia, 12, kartki)
            wks.update(range_name='A1', values=int(ostatnia)+1)
        except:
            pass

    await interaction.channel.send("Plik został zaktualizowany!")


##################################################################################
##################################################################################
##################################################################################
##################################################################################

@bot.tree.command(name="multiimport")
@app_commands.describe(rok="Podaj rok meczu" ,miesiac="Podaj miesiac meczu", dzien="Podaj dzien meczu")
async def importdata(
    interaction: discord.Interaction,
    rok: app_commands.Range[int, 1000, 9999],
    miesiac: app_commands.Range[int, 1, 12],
    dzien: app_commands.Range[int, 1, 31],
):
    if(miesiac<10 and len(str(miesiac))<2):
        miesiac='0'+str(miesiac)
    if(dzien<10 and len(str(dzien))<2):
        dzien='0'+str(dzien)
    Data=str(rok)+str(miesiac)+str(dzien)
    url = "https://livescore6.p.rapidapi.com/teams/get-team-stats"
    headers = {
        "X-RapidAPI-Key": "b737119a51mshe4651cd13badc03p18b663jsnab1f3e78a151",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com"
    }
    check2 = multicheck(Data)
    for i in range(len(check2)):
        if(check[i][0] == '12'):
            await interaction.channel.send("Nie posiadamy statystyk dla danego meczu(rozjebane api)")
            continue



@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Ready!")
    

bot.run(TOKEN)

