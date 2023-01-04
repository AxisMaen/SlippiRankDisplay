import tkinter as tk
import os
import datetime
import json
import scraper
import cache
import graph

### Features to support ###

# tkinter UI that shows rank and elo (looks like slippi user profile, could show set record too)
# bar at the top with dropdown to access settings
# app can be fullscreened (top bar removed), exit full screen with escape //TODO
# settings menu allows changing slippi code and sound that plays when ranking up/down (sound //TODO)
# optional: some sort of indication when an update happens
# (elo "scrolls" up/down, green or red flash for win or loss, etc.) //TODO

SETTINGSFILENAME = "files/settings.json"

#list of after function IDs that tracks any scheduled window refreshes
after_ids = []

#create fonts and colors
HEADERFONT = ("Roboto", 28)
SUBHEADERFONT = ("Roboto", 20)
BGCOLOR = "#23252c"
TEXTCOLOR = "#e9eaea"
WINCOLOR = "#2ecc40"
LOSSCOLOR = "#ff4d00"

#default settings
DEFAULTSETTINGS = {
    "code": "AXIS#944",
    "victoryAudioPath": "victoryAudio.mp3",
    "defeatAudioPath": "defeatAudio.mp3"
}

def open_settings():
    '''
    Opens the settings window
    '''
    top = tk.Toplevel(root)
    top.geometry("750x250")
    top.title("Settings")
    top.config(bg=BGCOLOR)
    top.grid_columnconfigure((0,2), weight=1)
    top.focus_set()
    top.grab_set()

    #gets settings from file (or uses default)
    settings = load_settings()

    ### create widgets and populate them with loaded settings ###
    code_label = tk.Label(top, text="Slippi Code")
    victory_audio_label = tk.Label(top, text="Victory Audio")
    defeat_audio_label = tk.Label(top, text="Defeat Audio")

    code_entry = tk.Entry(top, width=10, exportselection=0)
    code_entry.insert(0, settings["code"]) #prefill value
    victory_audio_entry = tk.Entry(top, width=60, exportselection=0)
    victory_audio_entry.insert(0, settings["victoryAudioPath"]) #prefill value
    defeat_audio_entry = tk.Entry(top, width=60, exportselection=0)
    defeat_audio_entry.insert(0, settings["defeatAudioPath"]) #prefill value

    ok_button = tk.Button(top, text="OK",
        command=lambda: save_settings(top, code_entry, victory_audio_entry, defeat_audio_entry))

    #place widgets
    code_label.grid(row=0, column=0)
    victory_audio_label.grid(row=1, column=0)
    defeat_audio_label.grid(row=2, column=0)
    code_entry.grid(row=0, column=1)
    victory_audio_entry.grid(row=1, column=1)
    defeat_audio_entry.grid(row=2, column=1)
    ok_button.grid(row=3, column=1)

def save_settings(top, code_entry, victory_audio_entry, defeat_audio_entry):
    '''
    Save settings to a file when the OK button is pressed on the settings window
    '''
    #if the code has changed, we need to refresh
    refresh_needed = False

    #format new settings
    settings = {
        "code": code_entry.get().upper().strip(),
        "victoryAudioPath": victory_audio_entry.get().strip(),
        "defeatAudioPath": defeat_audio_entry.get().strip()
    }

    #get old settings, if file not found make new file
    try:
        with open(SETTINGSFILENAME, "r", encoding='UTF8') as file:
            old_settings = json.load(file)

        #if code has changed a refresh might be needed
        if settings["code"] != old_settings["code"]:
            refresh_needed = True
    except: #pylint: disable=bare-except
        refresh_needed = True

    #save settings to file
    os.makedirs(os.path.dirname(SETTINGSFILENAME), exist_ok=True)
    with open(SETTINGSFILENAME, "w", encoding='UTF8') as file:
        json.dump(settings, file)

    #refresh main window if needed
    if refresh_needed:
        refresh_main_window()

    #close settings window
    top.destroy()


#loads the settings in the settings file, uses default if no settings file found
def load_settings():
    '''
    Gets settings from a file
    '''
    #default settings
    settings = DEFAULTSETTINGS

    #Open the settings from the file
    #If this fails, the default settings will be used
    try:
        with open(SETTINGSFILENAME, "r", encoding='UTF8') as file:
            settings = json.load(file)
    except: #pylint: disable=bare-except
        pass

    return settings

def refresh_main_window():
    '''
    Populates the main window with all needed widgets
    '''
    print("Refreshing")
    #load settings
    settings = load_settings()
    code = settings["code"]

    #remove any pending refreshes
    for after_id in after_ids:
        root.after_cancel(after_id)

    #checks for code in cache, scrape needed, and code validity
    while True:
        if cache.is_code_in_cache(code):
            if cache.is_update_needed(code):
                print("Valid code, update needed")
                #code in cache and needs updated, scrape and update cache
                response = scraper.send_query(code)

                #if we fail to get a response for any reason, do not proceed
                if not response:
                    return

                response = cache.update_cache(code, response)
                break
            else:
                print("Valid code, update not needed")
                #code exists but does not need update, pull from cache
                response = cache.read_cache()[code]
                break
        else:
            #not in cache, need to scrape
            response = scraper.send_query(code)

            #if we fail to get a response for any reason, do not proceed
            if not response:
                return

            if response["data"]["getConnectCode"]:
                print("Not in cache, updating")

                #if code is valid, update cache
                response = cache.update_cache(code, response)
            else:
                print("Invalid Code, using default settings")
                #if code is invalid, use default settings and try again
                code = DEFAULTSETTINGS["code"]

    display_name = response["data"]["getConnectCode"]["user"]["displayName"]
    rating = response["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingOrdinal"]
    win_count = str(response["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["wins"])
    loss_count = str(response["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["losses"])
    rating_history = response["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingHistory"]

    if win_count == "None":
        win_count = 0
    if loss_count == "None":
        loss_count = 0

    #clears old widgets
    widgets = root.winfo_children()

    #get all widgets
    for widget in widgets:
        if widget.winfo_children():
            widgets.extend(widget.winfo_children())

    #does not clear menu bar, as that does not need to be refreshed
    for widget in widgets:
        if widget.widgetName != "menu":
            widget.destroy()

    #create widgets to display the data
    display_name_label = tk.Label(root, text=display_name, font=HEADERFONT, fg=TEXTCOLOR, bg=BGCOLOR)
    code_label = tk.Label(root, text=code, font=SUBHEADERFONT, fg=TEXTCOLOR, bg=BGCOLOR)
    #rankImage = Image //TODO
    #rankLabel = Label(root, text = rank) //TODO
    rating_label = tk.Label(root, text=rating, font=SUBHEADERFONT, fg=TEXTCOLOR, bg=BGCOLOR)
    #seperate winCount, /, and lossCount for different colors
    win_label = tk.Label(root, text=win_count, font=SUBHEADERFONT, fg=WINCOLOR, bg=BGCOLOR)
    slash_label = tk.Label(root, text=" / ", font=SUBHEADERFONT, fg=TEXTCOLOR, bg=BGCOLOR)
    loss_label = tk.Label(root, text=loss_count, font=SUBHEADERFONT, fg=LOSSCOLOR, bg=BGCOLOR)

    #place widgets
    display_name_label.grid(row=1, column=0, columnspan=3)
    code_label.grid(row=2, column=0, columnspan=3)
    #rankImage.grid(row=, column=) //TODO
    #rankLabel.grid(row=, column=) //TODO
    rating_label.grid(row=3, column=0, columnspan=3)
    win_label.grid(row=4, column=0, sticky="e")
    slash_label.grid(row=4, column=1)
    loss_label.grid(row=4, column=2, sticky="w")

    #create graph
    #graphFrame = Frame(root,)
    canvas = graph.create_graph(root, rating_history)
    canvas.get_tk_widget().grid(row=5, column=0, columnspan=3)

    #get delay from now until midnight
    current_time = datetime.datetime.now()
    tomorrow = current_time + datetime.timedelta(days=1)
    delay = datetime.datetime.combine(tomorrow, datetime.time.min) - current_time

    #set to refresh at midnight
    after_id = root.after(int(delay.total_seconds()*1000), refresh_main_window)

    #add ID in case the refresh should be canceled
    #refreshes are canceled if another one happens before schedule (e.g. switching to another code)
    after_ids.append(after_id)


def on_closing():
    '''
    Actions to perform on tkinter closing
    Closes tkinter root and any open graphs
    '''
    root.destroy()
    graph.close_graphs()

##### START OF MAIN WINDOW INIT #####

root = tk.Tk()

#ensure that both tkinter and graphs are closed when exiting
root.protocol("WM_DELETE_WINDOW", on_closing)

#create menu bar
menuBar = tk.Menu(root)
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command( #add settings button
    label="Settings",
    command=open_settings
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
root.geometry("750x700")
root.config(menu=menuBar, bg=BGCOLOR)
root.grid_columnconfigure((0,2), weight=1)

#build initial window
refresh_main_window()

root.mainloop()
