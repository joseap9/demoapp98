import xmltodict
import pandas as pd

def xml_to_dict(xml_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        return xmltodict.parse(xml_content)

def dict_to_dataframe(xml_dict):
    # Obtener los registros
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