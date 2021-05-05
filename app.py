import requests
from bs4 import BeautifulSoup
from re import search
from flask import Flask ,jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False



def getNotesAndBooks(title):
    url = f'https://doku.pub/search/{title}?sort=popular'

    header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content,features='lxml')
    articals = soup.find_all('div', class_ ='col-lg-3 col-md-4 col-sm-6 col-6')
    complete_json = []
    for item in articals:
        complete_json.append(
            {
                'name':item.find('h5', class_='card-title').text,
                'uploadDate':item.find('small', class_='text-muted float-left' ).text,
                'imgurl':item.find('img' )['src'],
                'dawnloadurl':"https://doku.pub/download/"+item.find('a' )['href'].rsplit('/', 1)[1],
                # 'documentOpenUrl':BeautifulSoup(requests.get(item.find('a')['href'], headers=header).content,features='lxml').find_all('iframe',id='viewer'),
                'url':item.find('a' )['href'],
            }
        )
    return complete_json
       

    

@app.route('/')
def home_page():
    return "Welcome to https://doku.pub/ unofficial API"

@app.route('/<query>')
def home(query):
    

    return jsonify(getNotesAndBooks(query))



if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
    





