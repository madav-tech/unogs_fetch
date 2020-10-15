import requests
import xml.etree.ElementTree as T

r = requests.get("http://unogs.com/search/?country_andorunique=or&start_year=1900&end_year=2020&end_rating=10&genrelist=&audiosubtitle_andor=or&countrylist=336")
with open("response.html", 'w') as response_file:
    response_file.write(r.text)

tree = T.parse("response.html")