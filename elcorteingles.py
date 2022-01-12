### LLIBRERIES
import requests
from json import loads, dumps
from bs4 import BeautifulSoup

from monitor import Monitor

class Elcorteingles(Monitor):
    def __init__(self, interval):
        super().__init__(interval)

        #urls a les que accedim
        self.stock_api = "https://www.elcorteingles.es/api/stock"
        self.url_consoles = "https://www.elcorteingles.es/videojuegos/ps5/consolas/"

        #headers necessaris per al correcte funcionament
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0",
            'Accept': "*/*",
            'Accept-Language': "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            'DNT': "1",
            'Connection': "keep-alive",
            'Cache-Control': "max-age=0",
            'TE': "Trailers"
        }

        self.productes = {}
        self.__buscar_skus()
        #print(dumps(self.productes, indent=4))
        #print(self.sku_string)

    def __buscar_skus(self):
        '''Buscar en la pagina https://www.elcorteingles.es/videojuegos/ps5/consolas/ quins packs de consola ps5 hi ha actualment i en guardem en l'array self.productes un json amb la id, url, nom i stock actual'''

        response = requests.request("GET", self.url_consoles, headers=self.headers)
        print(f"{response.status_code} {self.url_consoles}")

        #seleccionem els spans on es troba un json amb les dades que necessitem
        soup = BeautifulSoup(response.text, 'lxml')
        spans = soup.findAll('span', {'class':'dataholder', 'data-scope':'product'})
        
        for span in spans:
            j = loads(span['data-json'])
            self.productes[j["id"]] = {
                "url": f"https://www.elcorteingles.es/videojuegos/{j['code_a']}/",
                "name": j["name"],
                "stock": True if j["status"] != "temporary_unavailable" else False
            }

        #string amb totes les skus dels productes que anirà a la consulta del stock    
        self.sku_string = ','.join(self.productes.keys())

    def comprovar_stock(self):
        '''Actualitze la informació sobre la disponibilitat dels productes trobats \n
            -Hi ha stock dels productes que apareixen en el array ADD \n
            -Si no hi ha apartat ADD no hi ha stock de cap producte
        '''
        querystring = {"skus": self.sku_string}

        response = requests.request("GET", self.stock_api, headers=self.headers, params=querystring)
        print(f"{response.status_code} {self.stock_api}")

        resp_json = loads(response.text)
        

        #busquem si els productes tenen stock
        if "ADD" in resp_json.keys():
            for id in resp_json['ADD']:
                self.productes[id]['stock'] = True
    




if __name__ == "__main__":
    s = Elcorteingles(30)
    s.monitorejar()
