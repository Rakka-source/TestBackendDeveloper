import glob
import os
import platform
import json
from pathlib import Path
from zipfile import ZipFile

class CONVERTIRARCHIVOS:

    def __init__(self,ruta) -> None:
        self.pathJson="{0}/downloadList.json".format(ruta)
        self.ruta=ruta
        self.sistOperativo=platform.system()
        with open(self.pathJson,'r') as file:
            self.listDownload = json.load(file)
            print(self.listDownload)

    def obtener_ultimo(self):
        self.list_file = glob.glob(self.ruta+"/*.zip")
        print("aca: {0}".format(self.list_file))
        if self.list_file:
            self.zip = max(self.list_file, key=os.path.getctime)
            self.add_list_download(self.zip)
            return (False)
        else:
            self.zip=""
            return (True)

    def list_download(self):
        return self.listDownload 
    
    def add_list_download(self,lastFile):
        self.listDownload["zip"].append(lastFile)
        with open(self.pathJson,'w') as file:
            json.dump(self.listDownload,file)
    
    def add_correlative_download(self):
        lastCorrelative=self.listDownload["correlativo"]
        print(lastCorrelative)
        self.listDownload["correlativo"].append(self.listDownload["correlativo"][-1]+1)
        with open(self.pathJson,'w') as file:
            json.dump(self.listDownload,file)

    def extract_zip(self):

        path = Path(self.ruta+"/"+str(self.listDownload["correlativo"][-1]))
        path.mkdir(parents=True,exist_ok=True)
        with ZipFile(self.zip,'r')as zip:
            zip.extractall(path)
        self.add_correlative_download()

