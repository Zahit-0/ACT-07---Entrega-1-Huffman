from tkinter import *
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText


Ventana = Tk()

def Abrir_Archivo():
    archivo = filedialog.askopenfilename()
    with open(archivo) as leer:
        Contenido = leer.read()
        Texto.insert('1.0', Contenido)#Inserta el contenido en el espacio asigando
        Total_letras = {}
        #for para buscar las letras y contarlas
        for Letra in Contenido:
            if Letra in Total_letras:
                Total_letras[Letra] += 1 #si se encuentra una letra y se repite se suma un mas 1 
            else:
                Total_letras[Letra]= 1
        for letra, contar in Total_letras.items():
            Texto.insert('end', f"\nNúmero de '{letra}':{contar}")
            

Texto = ScrolledText(Ventana)
Texto.pack()

Button(Ventana, text="Abrir Archivo", command=Abrir_Archivo).pack()
Button(Ventana, text="Comprimir").pack()#boton pa aplicar la funcion comprimir
Button(Ventana, text="Descomprimir").pack()

Ventana.mainloop()
