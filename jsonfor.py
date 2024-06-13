import os
import xmltodict
import json

def xml_to_json(xml_file_path):
    # Obtiene la ruta a la carpeta de Descargas del usuario
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Construye la ruta completa para el archivo JSON de salida
    json_file_path = os.path.join(downloads_path, 'archivo.json')
    
    # Abre y lee el archivo XML
    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        xml_content = xml_file.read()
    
    # Convierte el contenido XML a un diccionario
    xml_dict = xmltodict.parse(xml_content)
    
    # Convierte el diccionario a formato JSON
    json_content = json.dumps(xml_dict, indent=4)
    
    # Guarda el contenido JSON en un archivo
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_content)

    print(f"El archivo XML ha sido convertido a JSON y guardado en {json_file_path}")

# Ejemplo de uso
xml_file_path = r'C:\ruta\a\tu\archivo.xml'  # Usa la ruta completa a tu archivo XML
xml_to_json(xml_file_path)
