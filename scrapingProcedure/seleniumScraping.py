import platform
from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from re import split
from selenium.webdriver.firefox.options import Options
from pathlib import Path
from filesConvert.fileHandler import CONVERTIRARCHIVOS
import time


class DATOSABIERTOSGOB ():
  
    def __init__(self,ruta):
        ## Declaración de variables iniciales para sistemaWEB
        self.ruta=ruta
        path = Path(ruta)
        path.mkdir(parents=True,exist_ok=True)
        operatingSystem=platform.system()
        self.diccionary_web_scraping()
        if operatingSystem == "Windows":
            self.ruta=ruta+"\\"+"download"
            options = Options()
            options.set_preference("browser.download.dir", self.ruta)
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/pdf,application/zip,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
            options.set_preference("pdfjs.disabled", True)
            # Crear una sesión de Firefox
 
            self.driver = webdriver.Firefox(
                executable_path=r'.\geckodriver.exe',firefox_options=options)
            self.driver.implicitly_wait(30)
            self.driver.maximize_window()
            print("Creación de sesión exitosa, Windows")
        
        elif operatingSystem == "Linux":
            self.ruta=ruta+"/"+"download/"
            options = Options()
            options.set_preference("browser.download.dir", self.ruta)
            options.set_preference("browser.download.folderList", 2)
            options.set_preference("browser.download.manager.showWhenStarting", False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
            options.set_preference("pdfjs.disabled", True)
            # Crear una sesión de Firefox 

            options.headless = True
            self.driver = webdriver.Firefox(
                executable_path='/usr/local/bin/geckodriver',firefox_options=options)
            self.driver.implicitly_wait(30)
            self.driver.maximize_window()
            self.driver.set_window_size(1920, 1080)
            print (self.driver.get_window_size())
            print("Creación de sesión exitosa, Linux")

    def access_web_page(self):
        #Acceder pagina web
        self.driver.get("https://www.datosabiertos.gob.pe/")
        self.driver.implicitly_wait(10)

    def diccionary_web_scraping(self):
        self.dicContentType={
            "recursos":"facetapi-link--198",
            "dataset":"facetapi-link--199",
            "entidades":"facetapi-link--200",
            "harvest source":"facetapi-link--201",
            "pagina":"facetapi-link--202"
            ##You can keep adding
        }
        self.dicCategory={
            "economia y finanzas":"facetapi-link",
            "gobernalidad":"facetapi-link--2",
            "desarrollo social":"facetapi-link--3"
            ## You can keep adding
        }
        self.dicFormat={
            #Important: sequencing is required
            "xlsx":"facetapi-link--8",
            "csv":"facetapi-link--9"
            ##You can keep adding
        }

    def validador_diccionario(self,contentTypeData,category,formatFile):
        print(contentTypeData)
        if contentTypeData in self.dicContentType:
            return True
        else:
            return False


    def access_dataset_category_finanzas(self,contentTypeData,category,formatFile):
        validate=self.validador_diccionario(contentTypeData,category,formatFile)
        if validate:    
            self.access_web_page()
            #Input Squence
            datasetOptionButton=self.driver.find_element_by_id(self.dicContentType[contentTypeData])
            datasetOptionButton.click()
            #---
            economiaFinanzaButton=self.driver.find_element_by_id(self.dicCategory[category])
            print("Ingreso a economia y finanzas")
            economiaFinanzaButton.click()
            self.driver.implicitly_wait(10)

            #Item obscure option, Expand
            formatoCointainer=self.driver.find_element_by_xpath("/html/body/div[3]/div/div/section/div/div/div/div/div[1]/div/div[4]")
            formatoCointainer.click()
            self.driver.implicitly_wait(1)
            #Format open
            csvFormatButton=self.driver.find_element_by_id(self.dicFormat[formatFile])       
            csvFormatButton.click()
            self.driver.implicitly_wait(10)
            return(True)
        else:
            print ("Error en el diccionario, parametros no encontrados")
            return(False)

    def query_search(self):
        searcher=self.driver.find_element_by_id("edit-query")
        searcher.clear()
        searcher.send_keys("donaciones")
        buttonConsultar=self.driver.find_element_by_id("edit-submit-dkan-datasets")
        buttonConsultar.click()
        self.driver.implicitly_wait(10)
    
    def select_and_download(self):
        title="Donaciones COVID-19 - [Ministerio de Economía y Finanzas - MEF]"
        titleButton=self.driver.find_element_by_xpath("//a[@title='{0}']".format(title))
        titleButton.click()
        self.driver.implicitly_wait(10)
        downloadButton=self.driver.find_element_by_xpath("/html/body/div[3]/div/div/section/div/div/div/div/div[2]/div/div/div/article/div/div[3]/div/div/ul/li[3]/div/span/a")
        downloadButton.click()
        itsTheLast=CONVERTIRARCHIVOS(self.ruta)
        while itsTheLast.obtener_ultimo():
            print("no descarga aún")
            time.sleep(5)
        itsTheLast.extract_zip()

    def endProcess(self):
        self.driver.quit()