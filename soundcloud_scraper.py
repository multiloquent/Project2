import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Function to clear previously stored tracks
def clear_found_tracks():
    with open("found_tracks.txt", "w") as file:
        file.write("")


# Function to scrape SoundCloud page for user's uploaded tracks using Selenium
def scrape_soundcloud_tracks_selenium(artist_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(artist_url)

    try:
        # Wait for the tracks button to load
        tracks_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.g-tabs-link[href$='/tracks']")))
        tracks_button.click()

        # Wait for the tracks to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "soundTitle__title")))

        # Find elements containing the links to the user's uploaded tracks
        track_links = driver.find_elements(By.CLASS_NAME, "soundTitle__title")

        # Extract the track titles and URLs from the filtered links
        tracks = []
        for link in track_links:
            track_title = link.text
            track_url = link.get_attribute("href")
            if artist_url in track_url:
                tracks.append({'title': track_title, 'url': track_url})

        return tracks
    finally:
        # Close the WebDriver
        driver.quit()


# Function to scrape SoundCloud for new tracks
def get_new_tracks(artist_url):
    # Load previously found track URLs from file
    try:
        with open("found_tracks.txt", "r") as file:
            found_tracks = set(file.read().splitlines())
    except FileNotFoundError:
        found_tracks = set()

    # Scrape SoundCloud for new tracks
    new_tracks = scrape_soundcloud_tracks_selenium(artist_url)
    if new_tracks:
        # Filter out tracks already found
        new_tracks = [track for track in new_tracks if track['url'] not in found_tracks]
        
        for track in new_tracks:
            found_tracks.add(track['url'])

        # Save updated found tracks to file
        with open("found_tracks.txt", "w") as file:
            file.write("\n".join(found_tracks))

    return new_tracks


def soundcloud_scrape(profile_url):
    # Scrape uploaded tracks
    print(f"Scraping uploaded tracks from {profile_url}...")
    tracks = get_new_tracks(profile_url)

    if tracks:
        print(f"Uploaded tracks from {profile_url}:")
        for track in tracks:
            print("Title:", track['title'])
            print("URL:", track['url'])
            print()
    else:
        print("No new tracks found.")

    # delay between scraping each user's profile page
    time.sleep(8)  # Adjust as needed


if __name__ == "__main__":
    # Check if the "--clear" argument is provided in the command line
    if "--clear" in sys.argv:
        # Clear previously stored tracks
        clear_found_tracks()
        print("Previously stored tracks cleared.")

    # List of user profile URLs
    profile_urls = [
        "https://soundcloud.com/andy-pls"
    ]
    for profile_url in profile_urls:
        soundcloud_scrape(profile_url)
