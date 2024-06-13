import json
import pandas as pd
import xmltodict

def xml_to_json(xml_file_path):
    # Abre y lee el archivo XML
    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        xml_content = xml_file.read()
    
    # Convierte el contenido XML a un diccionario
    xml_dict = xmltodict.parse(xml_content)
    
    # Convierte el diccionario a formato JSON
    json_content = json.dumps(xml_dict, indent=4)
    
    return json.loads(json_content)

def parse_json_to_dataframe(json_data):
    # Extrae los registros del JSON
    records = json_data['ResultRecords']['ResultRecord']
    
    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    data = {column: [] for column in columns}
    
    for record in records:
        data['Id'].append(record.get('Id', ''))
        input_entity = record.get('InputEntity', {})
        data['EntityType'].append(input_entity.get('EntityType', ''))
        name = input_entity.get('Name', {})
        data['Full'].append(name.get('Full', ''))
        data['IdNumber'].append(record.get('IdNumber', ''))
        data['Status'].append(record.get('Status', ''))
        data['AlertState'].append(record.get('AlertState', ''))
        
        audit_records = record.get('AuditRecords', {}).get('AuditRecord', [])
        if isinstance(audit_records, dict):
            audit_records = [audit_records]
        for audit_record in audit_records:
            data['Action'].append(audit_record.get('Action', ''))
            data['Note'].append(audit_record.get('Note', ''))
        
        data['Origin'].append(record.get('Origin', ''))
    
    df = pd.DataFrame(data)
    return df

def filter_and_merge_dfs(df):
    # DataFrame con Action = 'RecordCreated'
    df_record_created = df[df['Action'] == 'RecordCreated'].copy()

    # DataFrame con Action = 'NewNote'
    df_new_note = df[df['Action'] == 'NewNote'].copy()

    # Merge de df_record_created con Note de df_new_note basado en Id
    df_final = df_record_created.copy()
    df_final['Note 2'] = df_final['Id'].map(df_new_note.set_index('Id')['Note'])

    # Agregar columna 'process' basada en 'Note' y 'Origin'
    df_final['process'] = df_final.apply(lambda row: (
        'Retail On Going' if 'SRS' in row['Note'] else
        'Commercial On Going' if 'ASTRA' in row['Note'] else
        'Vendor' if 'ORCL' in row['Note'] else
        'Retail On Boarding' if 'WebServices' in row['Origin'] else
        ''
    ), axis=1)

    # Eliminar filas donde 'Origin' contiene 'RealTime'
    df_final = df_final[~df_final['Origin'].str.contains('RealTime', na=False)]

    return df_final

if __name__ == "__main__":
    file_path = 'ruta_al_archivo.xml'
    json_data = xml_to_json(file_path)
    df = parse_json_to_dataframe(json_data)
    df_final = filter_and_merge_dfs(df)
    print(df_final.head())  # Imprimir las primeras filas del DataFrame para verificar
    print(f"Total de registros: {len(df_final)}")
