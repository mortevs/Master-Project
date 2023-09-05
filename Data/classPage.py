from bs4 import BeautifulSoup as soup
import requests
class Page:
    __url = "https://url.spec.whatwg.org/"
    __html = requests.get(__url).content
    __PageContent = soup(__html, "html.parser")
    def __init__(self, url):
        self.__url=url 
        self.__html=requests.get(url).content
        self.__PageContent = soup(self.__html, "html.parser")
    def getPageContent(self):
        return self.__PageContent