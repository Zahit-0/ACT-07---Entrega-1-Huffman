###########LIBRERIAS##############
import tkinter as tk
from tkinter import filedialog  #Modulo para explorar y leer archivos
import collections              #Modulo para crear de manera mas dinamica y sencilla la lista de frecuencia

############FUNCIONES#############

class Nodo:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

def Arbol(simbolos, frecuencias):
    cola_prioridad = [Nodo(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
    while len(cola_prioridad) > 1:
        cola_prioridad.sort(key=lambda nodo: nodo.frecuencia)
        izquierda = cola_prioridad.pop(0)
        derecha = cola_prioridad.pop(0)
        nuevo_nodo = Nodo(None, izquierda.frecuencia + derecha.frecuencia)
        nuevo_nodo.izquierda = izquierda
        nuevo_nodo.derecha = derecha
        cola_prioridad.append(nuevo_nodo)
    return cola_prioridad[0]

def Codigos(arbol, codigo_actual="", codigos={}):
    if arbol.caracter:
        codigos[arbol.caracter] = codigo_actual
    else:
        Codigos(arbol.izquierda, codigo_actual + "0", codigos)
        Codigos(arbol.derecha, codigo_actual + "1", codigos)
    return codigos

def Comprimir_texto(texto, codigos_huffman):
    texto_comprimido = ""
    for caracter in texto:
        texto_comprimido += codigos_huffman[caracter]
    return texto_comprimido

def Descomprimir_texto(texto_comprimido, arbol_huffman):
    texto_original = ""
    nodo_actual = arbol_huffman
    for bit in texto_comprimido:
        if bit == "0":
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        if nodo_actual.caracter:
            texto_original += nodo_actual.caracter
            nodo_actual = arbol_huffman
    return texto_original

def Compresion_Archivo(codigos_huffman):
    filePath = filedialog.askopenfilename()
    if filePath:
        file = open(filePath, 'r')
        content = file.read()
        file.close()
        texto_comprimido = Comprimir_texto(content, codigos_huffman)
        Compresion_Archivo = open("Texto Comprimido.bin", "w")
        Compresion_Archivo.write(texto_comprimido)
        Compresion_Archivo.close()

def Descomprimir_Archivo(arbol_huffman):
    filePath = filedialog.askopenfilename()
    if filePath:
        file = open(filePath, 'r')
        texto_comprimido = file.read()
        file.close()
        texto_original = Descomprimir_texto(texto_comprimido, arbol_huffman)
        Descomprimir_Archivo = open("Texto Descomprimido.txt", "w")
        Descomprimir_Archivo.write(texto_original)
        Descomprimir_Archivo.close()
 
def openFile():                                   #Funcion para leer el archivo y leer su frecuencia de caracteres
    global codigos_huffman, arbol_huffman
    filePath = filedialog.askopenfilename()       #Recupera y guarda la ruta del archivo
    if filePath:                                  #Revisa que esta ruta sea de un archivo existente
        file = open(filePath, 'r')                #Abre el archivo y guarda el objeto del mismo
        content = file.read()                     #Se imprime la frecuencia en la listbox de la ventana#
        file.close()                              #Cierra el archivo
        charFreq = collections.Counter(content)   #Counter, se encarga de contar la frecuencia de caracteres del string content
        arbol_huffman = Arbol(None, charFreq)
        codigos_huffman = Codigos(arbol_huffman)
        frequencyListbox.delete(0, tk.END)        #Limpia la listbox de la ventana, en caso de que tenga contenido no deseado

        #Se imprime la frecuencia en la listbox de la ventana
        for char, freq in charFreq.items():
            frequencyListbox.insert(tk.END, f"' {char} ' : {freq}")





#############VENTANA#############

####Ventana principal#####
root = tk.Tk()
root.title("Compresion Huffman")    

###Marco para los botones###
buttonFrame = tk.Frame(root)
buttonFrame.pack(pady=10)
#Boton para examinar archivos
examineButton = tk.Button(buttonFrame, text="Examinar", command=openFile)
examineButton.grid(row=0, column=0, padx=10)
#Boton para mandar a comprimir
compressButton = tk.Button(buttonFrame, text="Comprimir", command=lambda: Compresion_Archivo(codigos_huffman))
compressButton.grid(row=0, column=1, padx=10)
#Boton para descomprimir
decompressButton = tk.Button(buttonFrame, text="Descomprimir", command=lambda: Descomprimir_Archivo(arbol_huffman))
decompressButton.grid(row=0, column=2, padx=10)

###Marco para mostrar las frecuencias al usuario###
frequencyFrame = tk.Frame(root)
frequencyFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
#Etiqueta del marco
frequencyLabel = tk.Label(frequencyFrame, text="Frecuencia de Caracteres:")
frequencyLabel.pack(side=tk.LEFT)
#Caja para mostrar la lista
frequencyListbox = tk.Listbox(frequencyFrame, width=50, height=10)
frequencyListbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
