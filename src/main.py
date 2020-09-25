import re
import requests
from bs4 import BeautifulSoup



def get_code(url):
    res = requests.get(url)
    code = res.text

    return code

def find_api_url(github_url):
    exclusions = ['https://', 'github.com/', 'github.com']
    url_data = re.sub('|'.join(exclusions), '', github_url)

    url_data = url_data.split(sep='/')

    file = {"user": url_data[0], "repo": url_data[1], "branch": url_data[3], "file_path": '/'.join(url_data[4:])}

    api_url = f"https://raw.githubusercontent.com/{file['user']}/{file['repo']}/{file['branch']}/{file['file_path']}"
    return api_url

if __name__ == '__main__':
    url = "https://github.com/keshprad/Algorithms/blob/master/BellmanFordShortestPath/bellman_ford.py"
    api_url = find_api_url(url)
    code = get_code(api_url)
    print(code)
    print(api_url)
