import pandas as pd 
from pathlib import Path

def separate_by_region(nameFile,path,listDownload):
    pathstr=path+"/"+str(listDownload["correlativo"][-1])
    pathDire = Path(path+"/"+str(listDownload["correlativo"][-1]))
    pathFil=Path(path+"/"+str(listDownload["correlativo"][-1])+"/"+nameFile)
    df = pd.read_csv(pathFil,index_col=0, encoding='latin-1')
    
    listaRegiones=df["REGION"].unique().tolist()
    for item in listaRegiones:
        print(item)
        tablaToCSV=df[df["REGION"]==item]
        namfile=Path(path+"/"+str(listDownload["correlativo"][-1])+"/{0}.csv".format(item.lower()))
        tablaToCSV.to_csv(namfile) 
    print(listaRegiones)




if __name__=="__main__":
    separate_by_region("pcm_donaciones.csv","C:/Users/Mhord/Documents/GitHub/TestBackendDeveloper/download",{"correlativo":[0,1,2]})
