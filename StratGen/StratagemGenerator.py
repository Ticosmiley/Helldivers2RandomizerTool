import PySimpleGUI as sg
import random

class Stratagem:
    def __init__(self, name, isBackpack, isSupportWeapon, isOneHandedShield, isEagle):
        self.name = name
        self.isBackpack = isBackpack
        self.isSupportWeapon = isSupportWeapon
        self.isOneHandedShield = isOneHandedShield
        self.isEagle = isEagle
        
    def __str__(self):
        return self.name
    
    def getName(self):
        return self.name
#end class

class Weapon:
    def __init__(self, name, weaponType, isOneHanded):
        self.name = name
        self.weaponType = weaponType
        self.isOneHanded = isOneHanded
        
    def __str__(self):
        return self.name
#end class

stratagemList = []

file = open('Stratagem List.csv', 'r')

#Read file for stratagem info
for line in file:
    tempLineArray = line.split()
    stratagemName = ''
    
    #Get stratagem name from line in file
    for tempString in tempLineArray:
        if not tempString.isnumeric():
            if stratagemName == '':
                stratagemName = tempString
            else:
                stratagemName = stratagemName + ' ' + tempString
        else:
            break
    #end for loop
    
    #Get other stratagem info from line
    stratagemIsBackpack = bool(int(tempLineArray[len(tempLineArray) - 4]))
    stratagemIsSupportWeapon = bool(int(tempLineArray[len(tempLineArray) - 3]))
    stratagemIsOneHandedShield = bool(int(tempLineArray[len(tempLineArray) - 2]))
    stratagemIsEagle = bool(int(tempLineArray[len(tempLineArray) - 1]))
    
    #Create stratagem object and add to list
    tempStratagem = Stratagem(stratagemName, stratagemIsBackpack, stratagemIsSupportWeapon, stratagemIsOneHandedShield, stratagemIsEagle)
    stratagemList.append(tempStratagem)
    
#end file read
file.close()

weaponList = []

file = open('Weapon List.csv', 'r')

#Read file for weapon info
for line in file:
    tempLineArray = line.split()
    weaponName = ''
    weaponIsPrimary = False
    weaponIsSecondary = False
    weaponIsThrowable = False
    weaponIsOneHanded = False
    
    #Get weapon name from line in file
    for tempString in tempLineArray:
        if not tempString.isnumeric():
            if tempString == '*':
                weaponIsOneHanded = True
            elif weaponName == '':
                weaponName = tempString
            else:
                weaponName = weaponName + ' ' + tempString
        else:
            break
    #end for loop
    
    #Get weapon type from line
    weaponType = int(tempLineArray[len(tempLineArray) - 1])
        
        #Create weapon object and add to list
    tempWeapon = Weapon(weaponName, weaponType, weaponIsOneHanded)
    weaponList.append(tempWeapon)
    
#end file read
file.close()


boosterList = []

file = open('Booster List.csv')

#Read file for booster info
for line in file:
    boosterList.append(line.replace('\n', ''))

#end file read
file.close()


apList = []

file = open('Armor Passive List.csv')

#Read file for armor passive  info
for line in file:
    apList.append(line.replace('\n', ''))

#end file read
file.close()


#Random stratagem logic
def generateStrats(l, ban, include, checkList=None):
    stratList = []
    hasSW = False
    hasBP = False
    hasE = False
    
    if include:
        for item in include:
            for strat in l:
                if strat.name == item:
                    stratList.append(strat)
                    if strat.isSupportWeapon:
                        hasSW = True
                    elif strat.isBackpack:
                        hasBP = True
                    elif strat.isEagle:
                        hasE = True
    
    while len(stratList) < 4:
        tempStrat = l[random.randint(0, len(l) - 1)]
        #is the stratagem already in the loadoat?
        if tempStrat in stratList or tempStrat.name in ban:
            pass
        
        #is the stratagem a support weapon?
        elif tempStrat.isSupportWeapon:
            
            #is there already a support weapon in the loadoat?
            if not hasSW:
                
                #is the stratagem also a backpack?
                if tempStrat.isBackpack:
                    
                    #is there already a backpack in the loadoat?
                    if not hasBP:
                        hasSW = True
                        hasBP = True
                        stratList.append(tempStrat)
                    
                #stratagem is not a backpack
                else:
                    hasSW = True
                    stratList.append(tempStrat)
                    
        #is the stratagem a backpack?
        elif tempStrat.isBackpack:
            if not hasBP:
                hasBP = True
                stratList.append(tempStrat)
                
        #is the stratagem an eagle?
        elif tempStrat.isEagle:
            if not hasE:
                hasE = True
                stratList.append(tempStrat)
                
        #all other stratagems
        else:
            stratList.append(tempStrat)
    #end while loop
    return stratList
#end function


#Random weapon logic
def generateWeapons(wl, sl, ban, include):
    loadout = []
    hasP = False
    hasS = False
    hasT = False
    needsOHP = False
    
    for item in sl:
        if item.isOneHandedShield:
            needsOHP = True
    #end for loop
    
    if include:
        for item in include:
            for weap in wl:
                if weap.name == item:
                    loadout.append(weap)
                    if weap.weaponType == 0:
                        hasP = True
                    elif weap.weaponType == 1:
                        hasS = True
                    else:
                        hasT = True
    
    while len(loadout) < 3:        
        tempWeapon = wl[random.randint(0, len(wl) - 1)]
        
        #Is the weapon already in the loadout?
        if tempWeapon in loadout or tempWeapon.name in ban:
            pass
        
        #Is the weapon a primary?
        elif tempWeapon.weaponType == 0 and not hasP:
            if needsOHP:
                if tempWeapon.isOneHanded:
                    hasP = True
                    loadout.append(tempWeapon)
            else:
                hasP = True
                loadout.append(tempWeapon)
         
        #Is the weapon a secondary?
        elif tempWeapon.weaponType == 1 and not hasS:
            hasS = True
            loadout.append(tempWeapon)
            
        #Is the weapon a throwable?
        elif tempWeapon.weaponType == 2 and not hasT:
            hasT = True
            loadout.append(tempWeapon)
    #end while loop
    
    loadout = sorted(loadout, key=lambda weapon : weapon.weaponType)
    
    return loadout
#end function

def generateBooster(ban, include):
    if include:
        for item in boosterList:
            if item in include:
                return item
    while True:
        tempBooster = boosterList[random.randint(0, len(boosterList) - 1)]
        if tempBooster in ban:
            pass
        else:
            return tempBooster
            
def generateArmorPassive(ban, include):
    if include:
        for item in apList:
            if item in include:
                return item
    while True:
        tempAP = apList[random.randint(0, len(apList) - 1)]
        if tempAP in ban:
            pass
        else:
            return tempAP

#DO GUI THINGS

#Main Window
frame1 = [   [sg.CBox('', key=0, disabled=True), sg.Text("", key="Line1a")],
             [sg.CBox('', key=1, disabled=True), sg.Text("", key="Line2a")],
             [sg.CBox('', key=2, disabled=True), sg.Text("", key="Line3a")],
             [sg.CBox('', key=3, disabled=True), sg.Text("", key="Line4a")],
             [sg.Button('Random Stratagems')]  ]
           
frame2 = [   [sg.CBox('', key=4, disabled=True), sg.Text("", key="Line1b")],
             [sg.CBox('', key=5, disabled=True), sg.Text("", key="Line2b")],
             [sg.CBox('', key=6, disabled=True), sg.Text("", key="Line3b")],
             [sg.Button('Random Weapons')]  ]
             
frame3 = [   [sg.CBox('', key=7, disabled=True), sg.Text("", key="Line1c")],
             [sg.Button('Random Booster')]  ]
             
frame4 = [   [sg.CBox('', key=8, disabled=True), sg.Text("", key="Line3c")],
             [sg.Button('Random Armor Passive')]  ]

column1 = [  [sg.Frame("Stratagems", frame1, expand_x=True, title_color='light blue')],
             [sg.Frame('Weapons', frame2, expand_x=True, title_color='light blue')],
             [sg.Frame('Booster', frame3, expand_x=True, title_color='light blue')],
             [sg.Frame('Armor Passive', frame4, expand_x=True, title_color='light blue')]  ]

layout = [  [sg.Column(column1, expand_x=True)],
            [sg.Button('Generate All', pad=(6, 5)), sg.Button('Clear', pad=(6, 5)), sg.Button('Exclude', pad=(6, 5)), sg.Button('Include', pad=(6, 5))]  ]

window = sg.Window('Stratagem Generator 2000', layout)

banFile = open('Ban List.csv')
includeFile = open('Include List.csv')

#Popup window function helpers
bannedItems = []
includedItems = []

for line in banFile:
    bannedItems.append(line.replace('\n', ''))
    
for line in includeFile:
    includedItems.append(line.replace('\n', ''))
    
banFile.close()
includeFile.close()

#Exclude Window
def makeExcludeMenu(win):
    menuColumn1 = []
    menuColumn2 = []
    menuColumn3 = []
    menuColumn4 = []
    for item in stratagemList:
        menuColumn1.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=1, default=(item.name in bannedItems))])
        
    for item in weaponList:
        menuColumn2.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=2, default=(item.name in bannedItems))])
        
    for item in boosterList:
        menuColumn3.append([sg.CBox(item, key=item, enable_events=True, metadata=3, default=(item in bannedItems))])
        
    for item in apList:
        menuColumn4.append([sg.CBox(item, key=item, enable_events=True, metadata=4, default=(item in bannedItems))])
    
    
    
    menuLayout = [  [ sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn1, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(200, 300), key='menuColumn1')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn2, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(235, 300), key='menuColumn2')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn3, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(230, 300), key='menuColumn3')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn4, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(160, 300), key='menuColumn4')]]) ]  ] 
    pos = list(win.current_location())
    pos[0] -= 300
    pos[1] += 85
    pos = tuple(pos)
    return sg.Window('Exclude', menuLayout, modal=True, location=pos)
#end function

#Include Window
def makeIncludeMenu(win):
    menuColumn1 = []
    menuColumn2 = []
    menuColumn3 = []
    menuColumn4 = []
    for item in stratagemList:
        menuColumn1.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=1, default=(item.name in includedItems), disabled=(item.name in bannedItems))])
        
    for item in weaponList:
        menuColumn2.append([sg.CBox(item.name, key=item.name, enable_events=True, metadata=2, default=(item.name in includedItems), disabled=(item.name in bannedItems))])
        
    for item in boosterList:
        menuColumn3.append([sg.CBox(item, key=item, enable_events=True, metadata=3, default=(item in includedItems), disabled=(item in bannedItems))])
        
    for item in apList:
        menuColumn4.append([sg.CBox(item, key=item, enable_events=True, metadata=4, default=(item in includedItems), disabled=(item in bannedItems))])
    
    menuLayout = [  [ sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn1, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(200, 300), key='menuColumn1')]]),
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn2, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(235, 300), key='menuColumn2')]]), 
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn3, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(230, 300), key='menuColumn3')]]),
                      sg.Column([[sg.Button('Clear')], [sg.Column(menuColumn4, scrollable=True, vertical_scroll_only=True, vertical_alignment='top', s=(160, 300), key='menuColumn4')]]) ]  ]
    pos = list(win.current_location())
    pos[0] -= 300
    pos[1] += 85
    pos = tuple(pos)
    return sg.Window('Include', menuLayout, modal=True, location=pos)
#end function

stratList = []
weaponLoadout = []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if (event == 'Random Stratagems' or event == 'Generate All'):  
        if stratList:
            checkedStrats = []
            for row in frame1:
                if isinstance(row[0], sg.Checkbox) and row[0].get():
                    checkedStrats.append(row[1].get())
            stratList = generateStrats(stratagemList, bannedItems, includedItems)
            stratNames = {x.name for x in stratList}
            checkSet = set(checkedStrats)
            while checkSet in stratNames:
                stratList = generateStrats(stratagemList, bannedItems, includedItems)
        else:
            stratList = generateStrats(stratagemList, bannedItems, includedItems)
        
        if not window[0].get():
            window["Line1a"].update(stratList[0].name)
            if stratList[0].name in includedItems:
                window[0].update(disabled=True)
            else:
                window[0].update(disabled=False)
        if not window[1].get():
            window["Line2a"].update(stratList[1].name)
            if stratList[1].name in includedItems:
                window[1].update(disabled=True)
            else:
                window[1].update(disabled=False)
        if not window[2].get():
            window["Line3a"].update(stratList[2].name)
            if stratList[2].name in includedItems:
                window[2].update(disabled=True)
            else:
                window[2].update(disabled=False)
        if not window[3].get(): 
            window["Line4a"].update(stratList[3].name)
            if stratList[3].name in includedItems:
                window[3].update(disabled=True)
            else:
                window[3].update(disabled=False)
        
    if (event == 'Random Weapons' or event == 'Generate All'):
        weaponLoadout = generateWeapons(weaponList, stratList, bannedItems, includedItems)
        if not window[4].get():
            window["Line1b"].update(weaponLoadout[0].name)
            if weaponLoadout[0].name in includedItems:
                window[4].update(disabled=True)
            else:
                window[4].update(disabled=False)
        if not window[5].get():
            window["Line2b"].update(weaponLoadout[1].name)
            if weaponLoadout[1].name in includedItems:
                window[5].update(disabled=True)
            else:
                window[5].update(disabled=False)
        if not window[6].get():
            window["Line3b"].update(weaponLoadout[2].name)
            if weaponLoadout[2].name in includedItems:
                window[6].update(disabled=True)
            else:
                window[6].update(disabled=False)
        
    if (event == 'Random Booster' or event == 'Generate All'):
        if not window[7].get():
            window["Line1c"].update(generateBooster(bannedItems, includedItems))
            if window['Line1c'].get() in includedItems:
                window[7].update(disabled=True)
            else:
                window[7].update(disabled=False)
        
    if (event == 'Random Armor Passive' or event == 'Generate All'):
        if not window[8].get():
            window["Line3c"].update(generateArmorPassive(bannedItems, includedItems))
            if window['Line3c'].get() in includedItems:
                window[8].update(disabled=True)
            else:
                window[8].update(disabled=False)
        
    if (event == 'Exclude'):
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
                            bannedItems.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear0':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 2 and item.get():
                            bannedItems.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear1':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 3 and item.get():
                            bannedItems.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear2':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 4 and item.get():
                            bannedItems.remove(item.key)
                            item.update(False)
                elif (menuWindow[event2].get()):
                    bannedItems.append(event2)
                else:
                    bannedItems.remove(event2)
                    
    if (event == 'Include'):
        menuWindow = makeIncludeMenu(window)
        while True:
            event2, values2 = menuWindow.read()
            if event2 == sg.WIN_CLOSED:
                menuWindow.close()
                break
            
            if event2:
                if event2 == 'Clear':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 1 and item.get():
                            includedItems.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear0':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 2 and item.get():
                            includedItems.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear1':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 3 and item.get():
                            includedItems.remove(item.key)
                            item.update(False)
                elif event2 == 'Clear2':
                    for item in menuWindow.element_list():
                        if isinstance(item, sg.CBox) and item.metadata == 4 and item.get():
                            includedItems.remove(item.key)
                            item.update(False)
                elif (menuWindow[event2].get()):
                    includedItems.append(event2)
                    
                    #Handle disabling stratagem cboxes
                    if menuWindow[event2].metadata == 1:
                        tempStrat = None
                        for strat in stratagemList:
                            if strat.name == event2:
                                tempStrat = strat
                        if tempStrat.isSupportWeapon:
                            for strat in stratagemList:
                                if strat.isSupportWeapon and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    includedItems.remove(strat.name)
                        if tempStrat.isBackpack:
                            for strat in stratagemList:
                                if strat.isBackpack and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    includedItems.remove(strat.name)
                        if tempStrat.isEagle:
                            for strat in stratagemList:
                                if strat.isEagle and strat.name != event2 and menuWindow[strat.name].get():
                                    menuWindow[strat.name].update(False)
                                    includedItems.remove(strat.name)
                    
                    #Handle disabling weapon cboxes
                    if menuWindow[event2].metadata == 2:
                        tempWeapType = 0
                        for weap in weaponList:
                            if weap.name == event2:
                                tempWeapType = weap.weaponType
                        for weap in weaponList:
                            if weap.weaponType == tempWeapType and weap.name != event2 and menuWindow[weap.name].get():
                                menuWindow[weap.name].update(False)
                                includedItems.remove(weap.name)
                                
                    #Handle disabling booster cboxes
                    if menuWindow[event2].metadata == 3:
                        for item in boosterList:
                            if item != event2 and menuWindow[item].get():
                                menuWindow[item].update(False)
                                includedItems.remove(item)
                                
                    #Handle disabling armor passive cboxes
                    if menuWindow[event2].metadata == 4:
                        for item in apList:
                            if item != event2 and menuWindow[item].get():
                                menuWindow[item].update(False)
                                includedItems.remove(item)
                                
                else:
                    includedItems.remove(event2)
                                
    if (event == 'Clear'):
        for element in window.element_list():
            if isinstance(element, sg.Text):
                element.update("")
        for i in range (0,9):
            window[i].update(disabled=True)

window.close()

banFile = open('Ban List.csv', 'w')
for item in bannedItems:
    banFile.write(item + '\n')
    
includeFile = open('Include List.csv', 'w')
for item in includedItems:
    includeFile.write(item + '\n')
    
banFile.close()
includeFile.close()
