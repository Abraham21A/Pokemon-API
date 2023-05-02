import os
import requests
import json
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import urlopen
import textwrap

while True:
  nombre_pokemon = input("Introduce el nombre de un Pokémon: ")
  url = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon.lower()}"
  respuesta = requests.get(url)

  # Si el código de estado de la respuesta es 404 (no se encontró el Pokémon)
  if respuesta.status_code == 404:
    print(f"No se encontró el Pokémon {nombre_pokemon}. Intenta nuevamente.")
  else:
    # Obtener los datos del Pokémon en formato JSON
    datos_pokemon = respuesta.json()

    # guardar los datos de un Pokémon en un archivo JSON
    nombre_archivo = f"{datos_pokemon['name']}.json"
    if not os.path.exists("pokedex"): # Si la carpeta 'pokedex' no existe
      os.makedirs("pokedex") # Si la carpeta 'pokedex' no existe
    ruta_archivo = os.path.join("pokedex", nombre_archivo)

    # Abrir el archivo JSON en modo escritura
    with open(ruta_archivo, "w") as archivo:
      archivo.write(f"Datos del Pokémon {nombre_pokemon}:\n")
      # Escribir los datos del Pokémon en formato JSON en el archivo
      json.dump(datos_pokemon, archivo, indent=4) 

    # mostrar la información de un Pokémon
    print("Nombre:", datos_pokemon["name"])
    print("Peso:", datos_pokemon["weight"])
    print("Tamaño:", datos_pokemon["height"])
    print("Habilidades:")
    # Obtener una lista de habilidades del Pokémon
    habilidades = [habilidad["ability"]["name"] for habilidad in datos_pokemon["abilities"]]
    # Convertir la lista de habilidades en una cadena formateada
    habilidades_texto = "\n".join(textwrap.wrap(", ".join(habilidades), width=15))
    print(habilidades_texto)
    print("Tipos:", end=" ")
    for tipo in datos_pokemon["types"]:
      print(tipo["type"]["name"], end=", ")
    print("\nMovimientos:", len(datos_pokemon["moves"]))

    # mostrar la imagen y la tabla de un Pokémon
    url_imagen = datos_pokemon["sprites"]["front_default"]
    imagen = Image.open(urlopen(url_imagen))

    # se crea una figura que contiene dos subplots (ax1 y ax2) 
    # utilizando la biblioteca Matplotlib. En este caso, se establece 
    # el número de columnas en 2 y el tamaño de la figura en 10x5.
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))
    ax1.imshow(imagen)
    ax1.axis('off') 

    # se crea una lista de estadísticas del Pokémon 
    # que se utilizará para crear una tabla en el segundo subplot. 
    # La lista contiene información sobre el peso, tamaño, habilidades, 
    # tipos y movimientos del Pokémon.
    estadisticas = [
      ["Peso", str(datos_pokemon["weight"]/10) + " kg"],
      ["Tamaño", str(datos_pokemon["height"]/10) + "m"],
      ["Habilidades", habilidades_texto],
      ["Tipos", ", ".join([tipo["type"]["name"] for tipo in datos_pokemon["types"]])],
      ["Movimientos", str(len(datos_pokemon["moves"]))]
    ]
    
    # se crea una tabla utilizando la biblioteca Matplotlib. 
    # La tabla se basa en la lista de estadísticas del Pokémon.
    tabla = ax2.table(cellText=estadisticas, loc='center')
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(12)
    tabla.scale(1, 4)
    ax2.axis('off')

    # se muestra la figura que contiene los dos subplots, la imagen y la tabla
    plt.show()
    break