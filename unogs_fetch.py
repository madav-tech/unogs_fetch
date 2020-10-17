import requests
from bs4 import BeautifulSoup as BS
import json

def get_json():
    query = {"limit": 1, "offset": 0, "countrylist": 336, "country_andorunique": "or", "start_year": 1900, "end_year": 2020, "end_rating": 10, "audiosubtitle_andor": "or"}
    head =  {
            'Referer': 'http://unogs.com/search/?country_andorunique=or&start_year=1900&end_year=2020&end_rating=10&genrelist=&audiosubtitle_andor=or&countrylist=336',
            'REFERRER': 'http://unogs.com'
            }

    r = requests.get("http://unogs.com/api/search", params = query, headers = head)

    results = r.json()

    query["limit"] = results["total"]

    r = requests.get("http://unogs.com/api/search", params = query, headers = head)

    return r.json()

def main():
    results = get_json()
    ## Printing full json to file
    with open("title_dump.json", 'w') as f:
        f.write(json.dumps(results, indent = 2))

    ## Printing title list to file
    with open("name_list.txt", 'w') as f:
        for entry in results["results"]:
            f.write("title: " + str(entry["title"].encode('ascii','ignore'))[1:] + "\n")


if __name__ == "__main__":
    main()