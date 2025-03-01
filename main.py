import json
import os
import logging
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs


subject_of_interest = "django"


def get_urls(filepath):
    # Test the filepath to sure it exists
    if os.path.exists(filepath):
        f = open(filepath, "r")
        urls = json.load(f)
        f.close()
        return urls

    else:
        return ImportError

try:
    urls = get_urls(os.path.join(os.path.dirname(os.path.abspath(__file__)), "urls.json"))
except Exception as e:
    print(f"Erreur lors de l'obtention des urls. Details: {e}")
else:
    data = []
    for subject in urls.keys():
        for url in urls[subject]:
            try:
                res = get(url)
                soup = bs(res.text, 'html.parser')
                course_name = soup.find('h1', class_='ud-heading-xxl clp-lead__title clp-lead__title--small').text
                price = soup.find("meta", {"property": "udemy_com:price"})['content'].replace(',','.')
                devise = "Euro (€)" if "€" in price else "USD ($)"
                price = price.strip(" $US").strip("$") if devise == "USD ($)" else price.strip("€")
                next_topic = subject == subject_of_interest
                dic = {"Name": course_name, "Price": price, "Devise": devise, "Interessé": next_topic}
                data.append(dic)

            except Exception as e:
                print(f"Erreur lors du scrapping du cours: {url}. Details: {e}")


    df = pd.DataFrame(data)

    df.to_csv("courses_tracked_prices.csv", index=False)


