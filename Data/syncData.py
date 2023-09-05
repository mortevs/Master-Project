import requests
from bs4 import BeautifulSoup
import time
import numpy as np



def syncData(urls):
    statusList=[]
    purposeList=[]
    contentList=[]
    def my_handler(request, exception):
        print(f"exception thrown by requests: \n{exception}")
        return None
    for link in urls:

        response = requests.get(link, stream = False, timeout=2.0)
        response.close()
        try:
            response.close()
            sp = BeautifulSoup(response.content, 'lxml')
            

            try:
                status = (((sp.find("td", {"class":"a807c r6"})).select("div"))[1]).text
                statusList.append(status)
            except:
                statusList.append("NO DATA")
        except:
            print("An error occured")
    return statusList