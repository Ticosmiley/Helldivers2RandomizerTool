import PySimpleGUI as sg
import random
import pandas as pd
from collections import namedtuple

Stratagem = namedtuple('Stratagem', ['name', 'isBackpack', 'isSupportWeapon', 'isEagle', 'isOHS', 'isVehicle'])
Weapon = namedtuple('Weapon', ['name', 'weaponType', 'isOneHanded'])

allStratagems = []
allWeapons = []
allBoosters = []
allArmorPassives = []

stratIncludeList = []
weaponIncludeList = []
boosterToInclude = ''
armorPassiveToInclude = ''
banList = []

lockedInStrats = []
lockedInWeapons = []
lockedInBooster = ''
lockedInArmorPassive = ''

stratLoadout = [None, None, None, None]
stratLoadoutInfo = {'hasSW' : False, 'hasBP' : False, 'hasE' : False, 'hasV' : False}

weaponLoadout = [None, None, None]
oneHandedRequired = False

boosterLoadout = ''

armorPassiveLoadout = ''

#General helper functions

def findNamedTuple(name, listToSearch):
    for item in listToSearch:
        if item.name == name:
            return item
        
    return None

def readFileToList(file, l):
    with open(file, 'r') as file:
        for line in file:
            if line.strip() != '':
                l.append(line.strip())

def writeListToFile(l, file):
    with open(file, 'w') as file:
        for item in l:
            file.write(item + '\n')

#File reading

with open('Stratagem List.csv', 'r') as file:
    df = pd.read_csv(file, escapechar="\\")
    for index, row in df.iterrows():
        allStratagems.append(Stratagem.__new__(Stratagem, row['Name'], bool(row['isBackpack']), bool(row['isSupportWeapon']), \
                                               bool(row['isEagle']), bool(row['isOneHandedShield']), bool(row['isVehicle'])))

with open('Weapon List.csv', 'r') as file:
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        allWeapons.append(Weapon.__new__(Weapon, row['Name'], int(row['weaponType']), bool(row['isOneHanded'])))
        
readFileToList('Booster List.csv', allBoosters)
readFileToList('Armor Passive List.csv', allArmorPassives)
readFileToList('Ban List.csv', banList)
readFileToList('Stratagem Include List.csv', stratIncludeList)
readFileToList('Weapon Include List.csv', weaponIncludeList)

with open('Booster Include.csv') as file:
    boosterToInclude = file.readline().strip()

with open('Armor Passive Include.csv') as file:
    armorPassiveToInclude = file.readline().strip()

#Generation functions

def checkStratCompatibility(strat):
    if strat.isSupportWeapon and stratLoadoutInfo['hasSW']:
        return False
    
    if strat.isBackpack and stratLoadoutInfo['hasBP']:
        return False
    
    if strat.isEagle and stratLoadoutInfo['hasE']:
        return False
    
    if strat.isVehicle and stratLoadoutInfo['hasV']:
        return False
    
    return True

def updateStratLoadoutInfo(strat):
    global stratLoadoutInfo
    
    if strat.isSupportWeapon:
        stratLoadoutInfo['hasSW'] = True
    
    if strat.isBackpack:
        stratLoadoutInfo['hasBP'] = True
    
    if strat.isEagle:
        stratLoadoutInfo['hasE'] = True
    
    if strat.isVehicle:
        stratLoadoutInfo['hasV'] = True

def generateStratagemLoadout():
    global stratLoadout
    global stratLoadoutInfo
    global oneHandedRequired
    stratLoadout = [None, None, None, None]
    stratLoadoutInfo = {'hasSW' : False, 'hasBP' : False, 'hasE' : False, 'hasV' : False}
    oneHandedRequired = False
    
    if lockedInStrats:
        for i in range(len(lockedInStrats)):
            stratLoadout[lockedInStrats[i][0]] = lockedInStrats[i][1]
            updateStratLoadoutInfo(lockedInStrats[i][1])
    
    if stratIncludeList:
        for strat in stratIncludeList:
            tempStrat = findNamedTuple(strat, allStratagems)
            for index in range(len(stratLoadout)):
                if stratLoadout[index] == None and checkStratCompatibility(tempStrat):
                    if tempStrat.isOHS:
                        oneHandedRequired = True
                    stratLoadout[index] = tempStrat
                    updateStratLoadoutInfo(tempStrat)
                    break
    
    for index in range(len(stratLoadout)):
        while stratLoadout[index] == None:
            tempStrat = allStratagems[random.randint(0, len(allStratagems) - 1)]
            
            if tempStrat in stratLoadout or tempStrat.name in banList:
                continue
            
            if checkStratCompatibility(tempStrat):
                if tempStrat.isOHS:
                    oneHandedRequired = True
                stratLoadout[index] = tempStrat
                updateStratLoadoutInfo(tempStrat)

def generateWeaponLoadout():
    global weaponLoadout
    weaponLoadout = [None, None, None]
    
    if lockedInWeapons:
        for item in lockedInWeapons:
            weaponLoadout[item.weaponType] = item
            
    if weaponIncludeList:
        for weapon in weaponIncludeList:
            tempWeapon = findNamedTuple(weapon, allWeapons)
            if weaponLoadout[tempWeapon.weaponType] == None:
                weaponLoadout[tempWeapon.weaponType] = tempWeapon
                
    for index in range(len(weaponLoadout)):
        while weaponLoadout[index] == None:
            tempWeapon = allWeapons[random.randint(0, len(allWeapons) - 1)]
            
            if tempWeapon in weaponLoadout or tempWeapon.name in banList:
                continue
            
            if index == 0 and oneHandedRequired:
                if not tempWeapon.isOneHanded:
                    continue
            
            if tempWeapon.weaponType == index:
                weaponLoadout[index] = tempWeapon

def generateBoosterLoadout():
    global boosterLoadout
    boosterLoadout = ''
    
    if lockedInBooster:
        boosterLoadout = lockedInBooster
        
    elif boosterToInclude:
        boosterLoadout = boosterToInclude
        
    else:
        while boosterLoadout == '':
            tempBooster = allBoosters[random.randint(0, len(allBoosters) - 1)]
            
            if tempBooster not in banList:
                boosterLoadout = tempBooster
                
def generateArmorPassiveLoadout():
    global armorPassiveLoadout
    armorPassiveLoadout = ''
    
    if lockedInArmorPassive:
        armorPassiveLoadout = lockedInArmorPassive
        
    elif armorPassiveToInclude:
        armorPassiveLoadout = armorPassiveToInclude
        
    else:
        while armorPassiveLoadout == '':
            tempArmorPassive = allArmorPassives[random.randint(0, len(allArmorPassives) - 1)]
            
            if tempArmorPassive not in banList:
                armorPassiveLoadout = tempArmorPassive

#DO GUI THINGS

#Main Window Layouts
frame1 = [   
            [sg.CBox('', key=0, disabled=True, enable_events=True), sg.Text("", key="Loadout1.1")],
            [sg.CBox('', key=1, disabled=True, enable_events=True), sg.Text("", key="Loadout1.2")],
            [sg.CBox('', key=2, disabled=True, enable_events=True), sg.Text("", key="Loadout1.3")],
            [sg.CBox('', key=3, disabled=True, enable_events=True), sg.Text("", key="Loadout1.4")],
            [sg.Button('Random Stratagems')]  
         ]
           
frame2 = [   
            [sg.CBox('', key=4, disabled=True, enable_events=True), sg.Text("", key="Loadout2.1")],
            [sg.CBox('', key=5, disabled=True, enable_events=True), sg.Text("", key="Loadout2.2")],
            [sg.CBox('', key=6, disabled=True, enable_events=True), sg.Text("", key="Loadout2.3")],
            [sg.Button('Random Weapons')]  
         ]
             
frame3 = [   
            [sg.CBox('', key=7, disabled=True, enable_events=True), sg.Text("", key="Loadout3.1")],
            [sg.Button('Random Booster')]  
         ]
             
frame4 = [   
            [sg.CBox('', key=8, disabled=True, enable_events=True), sg.Text("", key="Loadout4.1")],
            [sg.Button('Random Armor Passive')]  
         ]

column1 = [  
             [sg.Frame("Stratagems", frame1, expand_x=True, title_color='light blue')],
             [sg.Frame('Weapons', frame2, expand_x=True, title_color='light blue')],
             [sg.Frame('Booster', frame3, expand_x=True, title_color='light blue')],
             [sg.Frame('Armor Passive', frame4, expand_x=True, title_color='light blue')] 
          ]

layout = [  
            [sg.Column(column1, expand_x=True)],
            [sg.Button('Generate All', pad=(6, 5)), sg.Button('Clear', pad=(6, 5)), sg.Button('Exclude', pad=(6, 5)), sg.Button('Include', pad=(6, 5))]  
         ]

window = sg.Window('Stratagem Generator 9001', layout)

#GUI helper functions

def updateDisplay():
    if all(stratLoadout):
        window["Loadout1.1"].update(stratLoadout[0].name)
        window["Loadout1.2"].update(stratLoadout[1].name)
        window["Loadout1.3"].update(stratLoadout[2].name)
        window["Loadout1.4"].update(stratLoadout[3].name)
    else:
        window["Loadout1.1"].update('')
        window["Loadout1.2"].update('')
        window["Loadout1.3"].update('')
        window["Loadout1.4"].update('')
    if all(weaponLoadout):
        window['Loadout2.1'].update(weaponLoadout[0].name)
        window['Loadout2.2'].update(weaponLoadout[1].name)
        window['Loadout2.3'].update(weaponLoadout[2].name)
    else:
        window['Loadout2.1'].update('')
        window['Loadout2.2'].update('')
        window['Loadout2.3'].update('')
    if boosterLoadout != '':
        window['Loadout3.1'].update(boosterLoadout)
    else:
        window['Loadout3.1'].update('')
    if armorPassiveLoadout != '':
        window['Loadout4.1'].update(armorPassiveLoadout)
    else:
        window['Loadout4.1'].update('')

def makeExcludeMenu(win):
    menuColumn1 = []
    menuColumn2 = []
    menuColumn3 = []
    menuColumn4 = []
    for item in allStratagems:
        menuColumn1.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=1, default=(item.name in banList))])
        
    for item in allWeapons:
        menuColumn2.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=2, default=(item.name in banList))])
        
    for item in allBoosters:
        menuColumn3.append([sg.CBox(item, key=item, enable_events=True, metadata=3, default=(item in banList))])
        
    for item in allArmorPassives:
        menuColumn4.append([sg.CBox(item, key=item, enable_events=True, metadata=4, default=(item in banList))])
    
    menuLayout = [  
                    [ sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn1, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(245, 300), key='menuColumn1')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn2, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(235, 300), key='menuColumn2')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn3, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(230, 300), key='menuColumn3')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn4, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(160, 300), key='menuColumn4')]]) ]  
                 ] 
    pos = list(win.current_location())
    pos[0] -= 300
    pos[1] += 85
    pos = tuple(pos)
    return sg.Window('Exclude', menuLayout, modal=True, location=pos)

def makeIncludeMenu(win):
    menuColumn1 = []
    menuColumn2 = []
    menuColumn3 = []
    menuColumn4 = []
    for item in allStratagems:
        menuColumn1.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=1, default=(item.name in stratIncludeList), disabled=(item.name in banList))])
        
    for item in allWeapons:
        menuColumn2.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=2, default=(item.name in weaponIncludeList), disabled=(item.name in banList))])
        
    for item in allBoosters:
        menuColumn3.append([sg.CBox(item, key=item, enable_events=True, metadata=3, default=(item in boosterToInclude), disabled=(item in banList))])
        
    for item in allArmorPassives:
        menuColumn4.append([sg.CBox(item, key=item, enable_events=True, metadata=4, default=(item in armorPassiveToInclude), disabled=(item in banList))])
    
    menuLayout = [  [ sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn1, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(245, 300), key='menuColumn1')]]),
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn2, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(235, 300), key='menuColumn2')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn3, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(230, 300), key='menuColumn3')]]),
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn4, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(160, 300), key='menuColumn4')]]) ]  ]
    pos = list(win.current_location())
    pos[0] -= 300
    pos[1] += 85
    pos = tuple(pos)
    return sg.Window('Include', menuLayout, modal=True, location=pos)

#GUI event loop

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    #Checkbox events
    if isinstance(event, int):
        if event < 4:
            lockedInStrats.clear()
            for i in range(4):
                if frame1[i][0].get():
                    lockedInStrats.append([i, findNamedTuple(frame1[i][1].get(), allStratagems)])
                    
        elif event < 7:
            lockedInWeapons.clear()
            for i in range(3):
                if frame2[i][0].get():
                    lockedInWeapons.append(findNamedTuple(frame2[i][1].get(), allWeapons))
            
        elif event == 7:
            lockedInBooster = frame3[0][1].get() if frame3[0][0].get() else ''
            
        elif event == 8:
            lockedInArmorPassive = frame4[0][1].get() if frame4[0][0].get() else ''
                
    #Button events
    if event == 'Random Stratagems' or event == 'Generate All':
        generateStratagemLoadout()
        updateDisplay()
        for i in range(4):
            if frame1[i][1].get().strip() not in stratIncludeList:
                window[i].update(disabled=False)
            else:
                window[i].update(disabled=True)
    
    if event == 'Random Weapons' or event == 'Generate All':
        generateWeaponLoadout()
        updateDisplay()
        for i in range(4, 7):
            if frame2[i-4][1].get() not in weaponIncludeList:
                window[i].update(disabled=False)
            else:
                window[i].update(disabled=True)
    
    if event == 'Random Booster' or event == 'Generate All':
        generateBoosterLoadout()
        updateDisplay()
        if boosterLoadout != boosterToInclude:
            window[7].update(disabled=False)
        else:
            window[7].update(disabled=True)
            
    if event == 'Random Armor Passive' or event == 'Generate All':
        generateArmorPassiveLoadout()
        updateDisplay()
        if armorPassiveLoadout != armorPassiveToInclude:
            window[8].update(disabled=False)
        else:
            window[8].update(disabled=True)
            
    if event == 'Clear':
        stratLoadout = [None, None, None, None]
        weaponLoadout = [None, None, None]
        boosterLoadout = ''
        armorPassiveLoadout = ''
        
        lockedInStrats.clear()
        lockedInWeapons.clear()
        lockedInBooster = ''
        lockedInArmorPassive = ''
        
        for i in range(9):
            window[i].update(False, disabled=True)
        
        updateDisplay()
    
    #Popup windows
    if event == 'Exclude':
        menuWindow = makeExcludeMenu(window)
        while True:
            event2, values2 = menuWindow.read()
            if event2 == sg.WIN_CLOSED:
                menuWindow.close()
                break
            
            if event2:
                if event2 == 'Clear':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 1 and item.get():
                            banList.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear0':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 2 and item.get():
                            banList.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear1':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 3 and item.get():
                            banList.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear2':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 4 and item.get():
                            banList.remove(item.key)
                            item.update(False)
                elif (menuWindow[event2].get()):
                    banList.append(event2)
                else:
                    banList.remove(event2)
            
    if event == 'Include':
        menuWindow = makeIncludeMenu(window)
        while True:
            event2, values2 = menuWindow.read()
            if event2 == sg.WIN_CLOSED:
                menuWindow.close()
                break
            
            if event2:
                
                #Clear buttons
                if event2 == 'Clear':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 1 and item.get():
                            stratIncludeList.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear0':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 2 and item.get():
                            weaponIncludeList.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear1':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 3 and item.get():
                            boosterToInclude = ''
                            item.update(False)
                elif event2 == 'Clear2':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 4 and item.get():
                            armorPassiveToInclude = ''
                            item.update(False)
                
                #Stratagem checkboxes
                elif menuWindow[event2].metadata == 1:
                    if menuWindow[event2].get():
                        stratIncludeList.append(event2.strip())
                        tempStrat = findNamedTuple(event2, allStratagems)
                        if tempStrat.isSupportWeapon:
                            for strat in allStratagems:
                                if strat.isSupportWeapon and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    stratIncludeList.remove(strat.name)
                        if tempStrat.isBackpack:
                            for strat in allStratagems:
                                if strat.isBackpack and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    stratIncludeList.remove(strat.name)
                        if tempStrat.isEagle:
                            for strat in allStratagems:
                                if strat.isEagle and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    stratIncludeList.remove(strat.name)
                        if tempStrat.isVehicle:
                            for strat in allStratagems:
                                if strat.isVehicle and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    stratIncludeList.remove(strat.name)
                    else:
                        stratIncludeList.remove(event2)
                
                #Weapon checkboxes
                elif menuWindow[event2].metadata == 2:
                    if menuWindow[event2].get():
                        weaponIncludeList.append(event2.strip())
                        tempWeapon = findNamedTuple(event2, allWeapons)
                        for weapon in allWeapons:
                            if weapon.weaponType == tempWeapon.weaponType and weapon.name != event2 and menuWindow[weapon.name].get():
                                menuWindow[weapon.name].update(False)
                                weaponIncludeList.remove(weapon.name)
                    else:
                        weaponIncludeList.remove(event2)
                        
                #Booster checkboxes
                elif menuWindow[event2].metadata == 3:
                    if menuWindow[event2].get():
                        boosterToInclude = event2.strip()
                        for booster in allBoosters:
                            if booster != event2 and menuWindow[booster].get():
                                menuWindow[booster].update(False)
                 
                #Armor Passive checkboxes
                elif menuWindow[event2].metadata == 4:
                    if menuWindow[event2].get():
                        armorPassiveToInclude = event2.strip()
                        for armorPassive in allArmorPassives:
                            if armorPassive != event2 and menuWindow[armorPassive].get():
                                menuWindow[armorPassive].update(False)
                            
window.close()

writeListToFile(banList, 'Ban List.csv')
writeListToFile(stratIncludeList, 'Stratagem Include List.csv')
writeListToFile(weaponIncludeList, 'Weapon Include List.csv')

with open('Booster Include.csv', 'w') as file:
    file.write(boosterToInclude)
    
with open('Armor Passive Include.csv', 'w') as file:
    file.write(armorPassiveToInclude)
        
    
    
    
    
    
    
        