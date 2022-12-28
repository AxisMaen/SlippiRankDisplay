from tkinter import *
import Scraper
import json

### Features to support ###

# tkinter UI that shows rank and elo (looks like slippi user profile, could show set record too)
# bar at the time with dropdown to access settings
# app can be fullscreened (top bar removed), exit full screen with escape
# settings menu allows changing slippi code and sound that plays when ranking up/down
# optional: some sort of indication when an update happens (elo "scrolls" up/down, green or red flash for win or loss, etc.)

#create fonts and colors
headerFont = ("Roboto", 28)
subHeaderFont = ("Roboto", 20)
bgColor = "#23252c"
textColor = "#e9eaea"
winColor = "#2ecc40"
lossColor = "#ff4d00"

#default settings
defaultSettings = {
    "code": "AXIS#944",
    "victoryAudioPath": "victoryAudio.mp3",
    "defeatAudioPath": "defeatAudio.mp3"
}

def openSettings():
    top = Toplevel(root)
    top.geometry("750x250")
    top.title("Settings")
    top.config(bg=bgColor)
    top.grid_columnconfigure((0,2), weight=1)
    top.focus_set()
    top.grab_set()
    
    #gets settings from file (or uses default)
    settings = loadSettings()
    
    ### create widgets and populate them with loaded settings ###
    codeLabel = Label(top, text="Slippi Code")
    victoryAudioLabel = Label(top, text="Victory Audio")
    defeatAudioLabel = Label(top, text="Defeat Audio")

    codeEntry = Entry(top, width=10, exportselection=0)
    codeEntry.insert(0, settings["code"]) #prefill value
    victoryAudioEntry = Entry(top, width=60, exportselection=0)
    victoryAudioEntry.insert(0, settings["victoryAudioPath"]) #prefill value
    defeatAudioEntry = Entry(top, width=60, exportselection=0)
    defeatAudioEntry.insert(0, settings["defeatAudioPath"]) #prefill value

    okButton = Button(top, text="OK", command=lambda: saveSettings(top, codeEntry, victoryAudioEntry, defeatAudioEntry))

    #place widgets
    codeLabel.grid(row=0, column=0)
    victoryAudioLabel.grid(row=1, column=0)
    defeatAudioLabel.grid(row=2, column=0)
    codeEntry.grid(row=0, column=1)
    victoryAudioEntry.grid(row=1, column=1)
    defeatAudioEntry.grid(row=2, column=1)
    okButton.grid(row=3, column=1)

def saveSettings(top, codeEntry, victoryAudioEntry, defeatAudioEntry):

    refreshNeeded = False #if the code has changed, we need to refresh

    #format new settings
    settings = {
        "code": codeEntry.get().upper().strip(), 
        "victoryAudioPath": victoryAudioEntry.get().strip(), 
        "defeatAudioPath": defeatAudioEntry.get().strip()
    }

    #get old settings
    with open("settings.json", "r") as file:
        oldSettings = json.load(file)
        if(settings["code"] != oldSettings["code"]):
            refreshNeeded = True

    #save settings to file
    with open("settings.json", "w") as file:
        json.dump(settings, file)

    #refresh main window if needed
    if(refreshNeeded):
        refreshMainWindow()

    #close settings window
    top.destroy()


#loads the settings in the settings file, uses default is no settings file found
def loadSettings():
    #default settings
    settings = defaultSettings

    #Open the settings from the file
    #If this fails, the default settings will be used
    try:
        with open("settings.json", "r") as file:
            settings = json.load(file)
    except:
        pass
    
    return settings
    

def refreshMainWindow():
    #load settings
    settings = loadSettings()
    code = settings["code"]

    #parse data from response
    response = Scraper.sendQuery(code)["data"]

    #if the code does not exist, use default settings and try again
    if(not response["getConnectCode"]):
        code = defaultSettings["code"]
        response = Scraper.sendQuery(code)["data"]

    displayName = response["getConnectCode"]["user"]["displayName"]
    rating = response["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingOrdinal"]
    winCount = str(response["getConnectCode"]["user"]["rankedNetplayProfile"]["wins"])
    lossCount = str(response["getConnectCode"]["user"]["rankedNetplayProfile"]["losses"])

    if(winCount == "None"):
        winCount = 0
    if(lossCount == "None"):
        lossCount = 0   

    #clears old widgets
    widgets = root.winfo_children()

    for widget in widgets:
        if(widget.winfo_children()):
            widgets.extend(widget.winfo_children())
    
    #does not clear menu bar, as that does not need to be refreshed
    for widget in widgets:
       if(widget.widgetName != "menu"):
            widget.destroy()

    #create widgets to display the data
    displayNameLabel = Label(root, text=displayName, font=headerFont, fg=textColor, bg=bgColor)
    codeLabel = Label(root, text=code, font=subHeaderFont, fg=textColor, bg=bgColor)
    #rankImage = Image //TODO
    #rankLabel = Label(root, text = rank) //TODO
    ratingLabel = Label(root, text=rating, font=subHeaderFont, fg=textColor, bg=bgColor)
    #seperate winCount, /, and lossCount for different colors
    winLabel = Label(root, text=winCount, font=subHeaderFont, fg=winColor, bg=bgColor) 
    slashLabel = Label(root, text=" / ", font=subHeaderFont, fg=textColor, bg=bgColor)
    lossLabel = Label(root, text=lossCount, font=subHeaderFont, fg=lossColor, bg=bgColor) 

    #place widgets
    displayNameLabel.grid(row=1, column=0, columnspan=3)
    codeLabel.grid(row=2, column=0, columnspan=3)
    #rankImage.grid(row=, column=) //TODO
    #rankLabel.grid(row=, column=) //TODO
    ratingLabel.grid(row=3, column=0, columnspan=3)
    winLabel.grid(row=4, column=0, sticky="e")
    slashLabel.grid(row=4, column=1)
    lossLabel.grid(row=4, column=2, sticky="w")

    #refresh the window every hour
    root.after(3600000, refreshMainWindow)

##### START OF MAIN WINDOW INIT #####

root = Tk()

#create menu bar
menuBar = Menu(root)
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command( #add settings button
    label="Settings",
    command=openSettings
)
fileMenu.add_command( #add exit button
    label="Exit",
    command=root.destroy,
)
menuBar.add_cascade( #add file dropdown to menu bar
    label="File",
    menu=fileMenu,
    underline=0
)

#configure window
root.title("Slippi Ranked Display")
root.geometry("750x250")
root.config(menu=menuBar, bg=bgColor)
root.grid_columnconfigure((0,2), weight=1)

#build initial window
refreshMainWindow()

root.mainloop()