#22 Oct 2023 17:21 - Version 4

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import csv

#Load page-----------------------------------------------------------------------------

# Set up Chromium options for headless mode
print("--Opening page...")

options = Options()
options.add_argument("--headless")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)#

# Navigate to website
# Xbox Store Japan - All Console Games - FILTERS: Xbox One, Xbox Series X|S, Price: from 500JPY to 6000JPY
driver.get("https://www.xbox.com/ja-JP/games/all-games/console?PlayWith=XboxSeriesX%7CS%2CXboxOne&Price=500To1000%2C1000To2000%2C2000To6000")

print("--Waiting to load...")

# Wait for the page to load
driver.implicitly_wait(5)  # Wait 5 seconds

print("#Done")

#Initialize next page function, CSV---------------------------------------------------------

# Define a function to click the button
def load_more():
    load_more_button = driver.find_element(By.XPATH, "//button[@aria-label='もっと表示する']")
    if load_more_button:
        load_more_button.click()
        return True
    else:
        return False

print("--Opening CSV...")

#Get title to resume from (Delete or move csv out of directory to avoid resume)
try:
    with open("catalog.csv", "r") as file:
        reader = csv.reader(file)
        last_row = None

        for row in reader:
            last_row = row  # Update last_row with the current row till cursor reaches end

        last_scraped_game = last_row[0]
        
except FileNotFoundError:
    last_scraped_game = None

#print(last_scraped_game) #debug

#Initialize CSV file if not resuming
if last_scraped_game is None:
    with open('catalog.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Game','Boxart','URL','IARC'])

with open('catalog.csv', 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    print("#Done")

#Extract and process game item data page by page-----------------------------------------------------

    # Initialize item count
    item_count = 0

    if last_scraped_game is not None:
        print("Resuming...")

    age_ratings = {
        "https://store-images.s-microsoft.com/image/global.39347.image.1ab912d3-d93c-4b3a-9b9f-511c8b8fef73.318bd350-ab48-4aae-aa58-cd0e8cb1559c" : "18",
        "https://store-images.s-microsoft.com/image/global.23519.image.809064e2-5b97-451f-bd04-e3cbd042ddcc.ce30c715-a977-48f0-9929-0dee0e170626" : "16",
        "https://store-images.s-microsoft.com/image/global.32925.image.f2c0ad38-c096-4e05-a76f-5c72d9258eaa.ecc5c21f-6a74-416a-98c1-99967316380b" : "12"
    }

    # Extract data from each new items
    while True:
        print("--Loading page...", end=" ")
        
        def check_itemsLoaded(driver):
            # Get the page source (HTML)
            page_source = driver.page_source
            global item_count

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')

            items = soup.find_all('li', {'role': 'none'})

            return len(items) > item_count, items
        
        # Find new items in game list after waiting to load them
        game_items = WebDriverWait(driver,15).until(check_itemsLoaded)[1]

        print("Done")
        print("--Extracting page items...", end=" ")

        game_items = game_items[item_count-len(game_items):]
        item_count += len(game_items)

        print("Done")

        # Remove games included in subscriptions
        # Iterate through the game items in reverse order to safely remove items
        for game_item in reversed(game_items):
            badges_div = game_item.find('div', {'class': 'ProductCard-module__badges___IHEn9'})
            if badges_div:
                game_items.remove(game_item)

        print("##Page items cleaned")


        if last_scraped_game is None:
            print("Found:", end=" ")

        # Iterate through the game items
        for game_item in game_items:
            #print(game_item) #debug
            
            #Get title
            anchor = game_item.find('a', {'class': 'commonStyles-module__basicButton___go-bX'})
            game_title = anchor['title']

            # Resume check block
            if last_scraped_game is not None:
                if game_title == last_scraped_game:
                    last_scraped_game = None
                    print("#Resumed")
                continue
            
            #Extract url for game's page
            game_url = anchor['href']

            # Open a new tab
            driver.execute_script("window.open('', '_blank');")
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[1])
            # Navigate to the game's URL
            driver.get(game_url)

            # Wait for the game's page to load
            driver.implicitly_wait(5)  # Wait for 5 seconds

            '''# Wait for the age rating image element to be present
            age_rating_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'EsrbRating-module__ratingImage___sMISX'))
            )'''

            # Get the page source for the game's page
            game_page_source = driver.page_source

            # Close the new tab
            driver.close()
            # Switch back to the main tab
            driver.switch_to.window(driver.window_handles[0])

            # Parse the HTML content using BeautifulSoup
            game_soup = BeautifulSoup(game_page_source, 'html.parser')

            # Extract age rating image url
            age_rating_image = game_soup.find('img', class_='EsrbRating-module__ratingImage___sMISX')
            age_rating_url = age_rating_image['src']

    #Output extracted data to CSV---------------------------------------------

            if age_rating_url in age_ratings:

                #Get corresponding age rating
                iarc=age_ratings[age_rating_url]

                #Get boxart url
                boxart_element = game_item.find('img', {'class': 'ProductCard-module__boxArt___-2vQY'})
                boxart_url = boxart_element['src'] if boxart_element is not None else ''

                csv_writer.writerow([game_title,boxart_url,game_url,iarc])

                print("*", end=" ")

        print("\n")

        if not load_more(): # Load more items
            break

        time.sleep(4)  # Wait to load items

# Close the browser
driver.quit()