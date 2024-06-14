import xmltodict
import pandas as pd

def xml_to_dict(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        return xmltodict.parse(xml_content)

def dict_to_dataframe(xml_dict):
    # Imprimir la estructura del diccionario para depuración
    print("Estructura del diccionario XML:", xml_dict)
    
    # Ajustar las claves según la estructura del diccionario
    result_records = xml_dict.get('resultrecords', {}).get('resultrecord', [])
    
    # Asegurarse de que result_records sea una lista
    if not isinstance(result_records, list):
        result_records = [result_records]
    
    # Crear una lista de diccionarios
    records_list = []
    for record in result_records:
        record_dict = {}
        for key, value in record.items():
            if isinstance(value, dict) and '#text' in value:
                record_dict[key] = value['#text']
            else:
                record_dict[key] = value
        records_list.append(record_dict)
    
    # Convertir la lista de diccionarios en un DataFrame
    df = pd.DataFrame(records_list)
    
    return df

# Ruta al archivo XML
xml_file = 'path_to_your_xml_file.xml'

# Convertir el XML a diccionario
xml_dict = xml_to_dict(xml_file)

# Convertir el diccionario a DataFrame
df = dict_to_dataframe(xml_dict)

# Mostrar el DataFrame
print(df)
