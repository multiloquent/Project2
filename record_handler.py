import csv
from pathlib import Path
from soundcloud_scraper import *


def start_record() -> None:
    """
    Checks for new_tracks_record.csv. If it does not exist it is created. Returns None.
    """
    file_path = Path('new_tracks_record')
    if not file_path.exists():
        with open('new_tracks_record', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Artist', 'URL', 'New'])
        print('new_tracks_record.csv created')
    else:
        print('new_tracks_record.csv found')


def update_record(artist, url) -> None:
    """
    Passes parameters artists and url to determine if user input should be added to new_tracks_record.csv
    Returns None.
    """
    duplicate = False
    with open('new_tracks_record', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if url in row:
                duplicate = True
                print('URL in dataset')
                break
    if duplicate is False:
        try:
            with open('new_tracks_record', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([artist, url, len(soundcloud_scrape(url))])
        except TypeError:
            with open('new_tracks_record', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([artist, url, 0])


def table_list() -> list:
    """
    Creates list of tuples created to populate table in gui.py. Returns a list.
    """
    tuple_list = []
    with open('new_tracks_record', mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        try:
            for row in csv_reader:
                tuple_list.append((row[0], row[1], row[2]))
        except IndexError:
            print('Check csv file for blank spaces')
        return tuple_list


def clear_track_memory() -> None:
    """
    Clears found_tracks.txt and new_tracks_record.csv. Returns None.
    """
    clear_found_tracks()
    with open('new_tracks_record', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Artist', 'URL', 'New'])
