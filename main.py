from unicodedata import category, name
from scrapingProcedure.seleniumScraping import DATOSABIERTOSGOB
from manejoCsv.pandasRegion import separate_by_region
import pathlib
import argparse

pathBase=str(pathlib.Path(pathlib.Path(__file__).parent.absolute()))

###Entrega de argumentos ###
##python3.9 main.py -t dataset -c "economia y finanzas" -f "csv"#
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tipo" ,help="Tipo de contenido; Ejemplo : 'Dataset' ")
parser.add_argument("-c", "--category", help="Categoria ; Ejemplo : 'Economia y finanzas'")
parser.add_argument("-f", "--format", help="Formato ; Ejemplo: 'csv'")
parser.add_argument("-n", "--name", help="Capturar todas las alertas activas; Prueba conexión")
parser.add_argument("-s", "--separate", help="separar regiones")
args=parser.parse_args()

if args.tipo and args.category and args.format:
    a=DATOSABIERTOSGOB(pathBase)
    if a.access_dataset_category_finanzas(args.tipo,args.category,args.format):
        a.query_search()
        a.select_and_download()
        pathCSV=a.endProcess()
else:
    sw=0
    cont=0
    while sw==0 and cont<5:
        type_data=str(input("Tipo de contenido; Ejemplo : 'Dataset' : ")).lower()
        category_data=str(input("\n Categoria ; Ejemplo : 'Economia y finanzas' : ")).lower()
        format_data=str(input("\n Formato ; Ejemplo: 'csv' : ")).lower()
        name_data = str(input("\n Nombre Archivo: ")).lower()
        if type_data and category_data and format_data and name_data:
            a=DATOSABIERTOSGOB(pathBase)
            if a.access_dataset_category_finanzas(type_data,category_data,format_data):
                a.query_search()
                a.select_and_download()
                pathCSV=a.endProcess()
                sw=1
            else:
                print("----- Volver a ingresar datos ------")
        else:
            print("Se requiere de todos los campos")
        cont+=1

separate_by_region("pcm_donaciones.csv",str(pathCSV),{"correlativo":[0]})