import os
import win32clipboard
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium import webdriver
from card-stats import CardStats

browser_type = input("Select a browser:\n1.) Chrome\n2.) Firefox\nChoice: ")
while browser_type != "1" and browser_type != "2":
    browser_type = input("Invalid input, try again: ")

if browser_type == "1":
    driver_path = os.getcwd() + "/WebDrivers/chromedriver.exe"
    service = ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
elif browser_type == "2":
    driver_path = os.getcwd() + "/WebDrivers/geckodriver.exe"
    service = FirefoxService(executable_path=driver_path)
    driver = webdriver.Firefox(service=service)


deck_found = False
while not deck_found:
    targ_deck = input("Enter the target deck's name 'Ex: Giratina, Mew Genesect': ")
    limit = float(input("How many of the highest scoring decks should be analyzed?: "))
    while not limit.is_integer() or limit == 0:
        if limit == 0:
            limit = float(input("Please enter a number greater than 0: "))
        else:
            limit = float(input("Invalid input, try again: "))
        targ_deck = targ_deck.capitalize()
    try:
        driver.get("https://play.limitlesstcg.com/decks?game=PTCG")
        deck_anchor = driver.find_element(By.LINK_TEXT, targ_deck)
        deck_found = True
        deck_anchor.click()
    except:
        targ_deck = input("No deck could be located with given name. Please try again: ")

deck_list = []
copied_decks = 0
index = 0
while copied_decks < int(limit):
    decklist_anchors = driver.find_elements(By.XPATH, "//div/table/tbody/tr/td/a/i/parent::*")
    if index >= len(decklist_anchors):
        print("Decks ran out before reaching the given number.")
        break
    decklist_anchors[index].click()
    try:
        # Finds the export button and clicks it to copy decklist to clipboard. Throws and exception if the element can't be found.
        export_button = driver.find_element(By.CLASS_NAME, "export")
        export_button.click()
        win32clipboard.OpenClipboard()
        deck = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        stats_string = driver.find_element(By.CLASS_NAME, "details").getText()
        # stats_string: '# points (W-L-D)'
        # Splits to ['#', 'points', '(W-L-D)']
        points = stats_string.split()[0]
        win_loss = stats_string.split()[2]
        # tuple format: ('decklist', '(W-L-D)')
        deck_tuple = (deck, win_loss)
        deck_list.append(deck_tuple)
        copied_decks += 1
        driver.back()
        index += 1
    except Exception as e:
        # Current decklist is not available or does not have an export button
        driver.back()
        index += 1
driver.close()

card_dict = {}
for deck_stats in deck_list:
    card_list = deck_stats[0]
    # record_string: '#Wins-#Losses-#Draws'
    record_string = (deck_stats[1].replace('(', '')).replace(')', '')
    # wld: ['#Wins', '#Losses', '#Draws']
    wld = record_string.split('-')
    # iterate through wld and convert each string to an integer
    for i in range(len(wld)):
        wld[i] = int(wld[i])
    winrate = float(wins / (wins + losses + draws))
    for card in card_list:
        # ["count", "name", "(set)"]
        card_stats = card.split()
        name = card_stats[1]
        set = (card_stats[2].replace('(', '')).replace(')', '')
        if (card + ' ' + set) not in card_dict.keys():
            new_card = CardStats(name, set)
            count = int(card_stats[0])
            new_card.add_Count(count)
            new_card.add_Count_WR(count, winrate)
