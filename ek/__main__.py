import requests
from bs4 import BeautifulSoup, builder
import os
import re
import sys

URL_REGEX = r"/index\.php/etlapunk\?survey=[a-z0-9]{40}"

if __name__ == "__main__":
    post_url = "https://httpbin.org/anything"
    session = requests.Session()
    if os.getenv("EK_DEBUG") is not None and os.getenv("EK_DEBUG"):
        with open("urlap.html") as fp:
            soup = BeautifulSoup(fp, "html.parser")
    else:
        if len(sys.argv) != 2:
            raise RuntimeError("Hibás számú paraméter")
        post_url = sys.argv[1]
        response = session.get(url=post_url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")
    survey = None
    for form in forms:
        matches =  re.match(URL_REGEX, form["action"]) 
        if matches is not None:
            survey = form
    if survey is None:
        raise RuntimeError("Nem található az űrlap")
    inputs = survey.find_all(["input", "select"])
    post_data = {
        "ipacomment": "",
        "xxx": []
    }
    for input in inputs:
        if input["name"] == "postsurvey" or input["name"] == "survey" or input["name"] == "week":
            post_data[input["name"]] = input["value"]
        elif input["name"] == "xxx":
            pass
        else:
            post_data[input["name"]] = 10
            post_data["xxx"].append(10)
    response = session.post(post_url, data=post_data)
    if response.status_code != 200:
        print(BeautifulSoup(response.text, "html.parser").prettify())
        raise RuntimeError(f"HTTP hiba; státusz kód: {response.status_code}")
    print(BeautifulSoup(response.text, "html.parser").prettify())
