import requests
import json
import time
import html.parser as HP
import random
import webbrowser as wb


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_json(title_type = ""):
    query = {
            "limit": 1,
            "offset": 0,
            "countrylist": 336, ## Israel code (for some reason)
            "country_andorunique": "or",
            "start_year": 1900,
            "end_year": 2020,
            "end_rating": 10,
            "audiosubtitle_andor": "or",
            "type": title_type
            }
    head =  {
            'Referer': 'http://unogs.com/search/?country_andorunique=or&start_year=1900&end_year=2020&end_rating=10&genrelist=&audiosubtitle_andor=or&countrylist=336',
            'REFERRER': 'http://unogs.com'
            }


    r = requests.get("http://unogs.com/api/search", params = query, headers = head)

    results = r.json()

    query["limit"] = results["total"]

    r = requests.get("http://unogs.com/api/search", params = query, headers = head)

    results = r.json()
    for item in results["results"]:
        item["title"] = HP.unescape(item["title"])
        item["synopsis"] = HP.unescape(item["synopsis"])
    
    return results




def get_country_data(nfid):

    r = requests.get("http://unogs.com/api/title/countries", params = {"netflixid": nfid})
    return r.json()

def get_genres(genre):
    head =  {
            'Referer': 'http://unogs.com',
            'REFERRER': 'http://unogs.com'
            }
    r = requests.get("http://unogs.com/api/select/genre",params = {"q": genre}, headers = head)
    return r.json()

def missing_seasons():
    results = get_json(title_type = "Series")["results"]
    missing = {}
    last_title = ""
    for item in results:
        print(f"title: {item['title']}", end = f"{' ' * (len(last_title) - len(item['title']))}\r")
        last_title = item["title"]
        country_data = get_country_data(item["nfid"])
        
        for country in country_data:
            if country["id"] == 336:
                season_str = country["seasdet"]
                i_season_list = [season[1] for season in season_str.split(',')] ## ['1', '2', ...]
        
        for country in country_data:
            c_season_list = [season[1] for season in country["seasdet"].split(',')] ## ['1', '2', ...]
            for season_number in c_season_list:
                if season_number not in i_season_list:
                    if item["title"] not in missing:
                        missing[item["title"]] = {}
                        print(f"{colors.OKCYAN}\'{item['title']}\' has missing seasons!{colors.ENDC}")
                    missing[item["title"]]["israel"] = i_season_list
                    missing[item["title"]][country["country"]] = c_season_list
    
    return missing

def print_mising_seasons():
    print("Fetching missing seasons (this may take a while)... ")
    missing_json = missing_seasons()
    for title in missing_json:
        print(f"{colors.OKGREEN}For title '{title}'': {colors.ENDC}")
        print(f"{colors.OKBLUE}Seasons available in Israel: {', '.join(missing_json[title]['israel'])}{colors.ENDC}")
        for country in missing_json[title]:
            if country != "israel":
                print(f"Seasons available in {country}: {', '.join(missing_json[title][country])}")


def update_dump():
    results = get_json(title_type = "Series")
    ## Printing full json to file
    with open("title_dump.json", 'w') as f:
        f.write(json.dumps(results, indent = 2))


def pick_genre():
    gen = input("Enter a genre query: ")
    print("Fetching matching genres...")
    genre_json = get_genres(gen)
    genre_list = [element["text"] for element in genre_json]

    while genre_list == []:
        gen = input(f"{colors.WARNING}No genres found, please enter a new genre query: {colors.ENDC}")
        genre_json = get_genres(gen)
        genre_list = [element["text"] for element in genre_json]

    for genre in genre_list:
        print(genre)

    gen = input("Please pick one of the genres from the list above: ")
    while gen.lower() not in [genre.lower() for genre in genre_list]:
        gen = input(f"{colors.WARNING}Genre not in list, please pick again: {colors.ENDC}")
    print(gen) #### DOESN'T DO ANYTHING RIGHT NOW


def get_random_title():
    results = get_json()
    return random.choice(results["results"])


def open_random_title():
    rand_title = get_random_title()
    title = rand_title["title"]
    nfid = rand_title["nfid"]
    for i in range(3, 0, -1):
        print(f"\rYour random title is: '{title}'. Opening in {i} seconds...", end = "")
        time.sleep(1)
    print("")
    wb.open(f"https://www.netflix.com/title/{nfid}")


def main():
    open_random_title()

if __name__ == "__main__":
    main()