import requests
import json
import time

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

    return r.json()



def get_country_data(nfid):

    r = requests.get("http://unogs.com/api/title/countries", params = {"netflixid": nfid})
    # time.sleep(0.1)
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
    for item in results:
        print(f"\rtitle: {item['title']}", flush = True)
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
                    missing[item["title"]][country["country"]] = c_season_list
    
    return missing



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
        gen = input("No genres found, please enter a new genre query: ")
        genre_json = get_genres(gen)
        genre_list = [element["text"] for element in genre_json]

    for genre in genre_list:
        print(genre)

    gen = input("Please pick one of the genres from the list above: ")
    while gen.lower() not in [genre.lower() for genre in genre_list]:
        gen = input("Genre not in list, please pick again: ")
    print(gen) #### DOESN'T DO ANYTHING RIGHT NOW



def main():
    pick_genre()

if __name__ == "__main__":
    main()