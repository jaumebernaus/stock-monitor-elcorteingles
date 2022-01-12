from time import sleep
import webbrowser
from beepy import beep

class Monitor():
    def __init__(self, interval):
        self.interval = interval

    def monitorejar(self):
        '''Funció que busca periodicament (segons el interval configurat) si hi ha stock.'''
        ids = self.productes.keys()
        while True:
            #fem una copia de productes avans de comprovar 
            productes_antic = self.productes

            #actualitzem al informació del stock
            self.comprovar_stock()

            #iterem entre els productes que hi ha
            for id in ids:
                #canvi d'stock
                if productes_antic[id]['stock'] != self.productes[id]['stock']:
                    #està en stock
                    if self.productes[id]['stock'] == True:
                        webbrowser.open_new_tab(self.productes[id]['url'])
                        beep(sound='ping')
                        print(f"{self.productes[id]['url']} en stock")
                    #stock esgotat
                    else:
                        print(f"{self.productes[id]['url']} agotat")
                        

            sleep(self.interval)
