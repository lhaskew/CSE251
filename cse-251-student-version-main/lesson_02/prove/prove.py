"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: <Add name here>

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}

Outline of API calls to server

1) Use TOP_API_URL to get the dictionary above
2) Add "6" to the end of the films endpoint to get film 6 details
3) Use as many threads possible to get the names of film 6 data (people, starships, ...)
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0
lock = threading.Lock()


class Request_Thread(threading.Thread):

    def __init__(self, url):
        # Call the Thread class's init function
        super().__init__()
        self.url = url
        self.response = {}
        self.status_code = {}

    def run(self):
        global call_count
        response = requests.get(self.url)
        with lock:
            call_count += 1
        self.status_code = response.status_code
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('RESPONSE = ', response.status_code)


def get_film_details(film_url):
    response = requests.get(film_url)
    global call_count
    with lock:
        call_count += 1
    if response.status_code == 200:
        return response.json()
    return None


def get_resource_names(urls):
    threads = [Request_Thread(url) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return sorted([thread.response['name'] for thread in threads if thread.response])


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # Retrieve Top API urls
    response = requests.get(TOP_API_URL)
    global call_count
    with lock:
        call_count += 1

    if response.status_code != 200:
        log.write('Failed to retrieve top API URL')
        return

    api_urls = response.json()

    # Retrieve Details on film 6
    film_url = api_urls['films'] + '6'
    film_details = get_film_details(film_url)
    if not film_details:
        log.write('Failed to retrieve film 6 details')
        return

    # Get URLs for each resource category
    people_urls = film_details['characters']
    starships_urls = film_details['starships']
    vehicles_urls = film_details['vehicles']
    species_urls = film_details['species']
    planets_urls = film_details['planets']

    # Retrieve names using threads
    people_names = get_resource_names(people_urls)
    starships_names = get_resource_names(starships_urls)
    vehicles_names = get_resource_names(vehicles_urls)
    species_names = get_resource_names(species_urls)
    planets_names = get_resource_names(planets_urls)

    # Display results
    log.write("----------------------------------------")
    log.write(f"Title   : {film_details['title']}")
    log.write(f"Director: {film_details['director']}")
    log.write(f"Producer: {film_details['producer']}")
    log.write(f"Released: {film_details['release_date']}\n")

    log.write(f"Characters: {len(people_names)}")
    log.write(", ".join(people_names) + "\n")

    log.write(f"Planets: {len(planets_names)}")
    log.write(", ".join(planets_names) + "\n")

    log.write(f"Starships: {len(starships_names)}")
    log.write(", ".join(starships_names) + "\n")

    log.write(f"Vehicles: {len(vehicles_names)}")
    log.write(", ".join(vehicles_names) + "\n")

    log.write(f"Species: {len(species_names)}")
    log.write(", ".join(species_names) + "\n")

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')


if __name__ == "__main__":
    main()
