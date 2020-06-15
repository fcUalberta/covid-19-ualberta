import os
import urllib.request

def download_data():
    """
    Function to download everyday data
    """
    path = r"data1/"
    myProxy = urllib.request.ProxyHandler({'http': '127.0.0.2'})
    openProxy = urllib.request.build_opener(myProxy)
    link = r"https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv"

    urllib.request.urlretrieve(link, os.path.join(path,"data.csv"))
