from bs4 import BeautifulSoup as soup
import requests
from Data.classPage import Page


def NPDgetFieldURL(fieldName: str) ->str:
    url = "https://factpages.npd.no/nb-no/field/PageView/All"
    html = requests.get(url).content
    page = soup(html, "html.parser")
    fieldList = (page.find_all("a", {"class":"node"}))
    for i in fieldList:
        fName = i.find('div').contents[0]
        if fieldName.upper() == fName:
            url = str(i['href'])
            return url
    else:
        raise Exception("No data avaiable for " + fieldName + " at NPD")

        
        
def getWellURL(fieldPage) -> str:
    content = fieldPage.getPageContent()
    a = (content.find("td", {"class":"a397c"}))
    a = a.select("div a")
    return ((a[0]).attrs["href"])


def getProductionWellURLs(fieldPage) -> list:
    URLList = []
    content = fieldPage.getPageContent()
    a = (content.find_all("td", {"class":"a1494cl"}))
    for el in a:
        el = el.select("div a")
        el = ((el[0]).attrs["href"])
        URLList.append(el)
    return URLList


    


