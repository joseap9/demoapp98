import xmltodict
import pandas as pd

def xml_to_dict(xml_file_path):
    # Abre y lee el archivo XML
    with open(xml_file_path, 'r', encoding='utf-8') as xml_file:
        xml_content = xml_file.read()
    
    # Convierte el contenido XML a un diccionario
    xml_dict = xmltodict.parse(xml_content)
    
    return xml_dict

def parse_dict_to_dataframe(xml_dict):
    # Extrae los registros del diccionario
    records = xml_dict['ResultRecords']['ResultRecord']
    
    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    data = {column: [] for column in columns}
    
    for record in records:
        id_value = record.get('Id', '')
        input_entity = record.get('InputEntity', {})
        entity_type = input_entity.get('EntityType', '')
        name = input_entity.get('Name', {})
        full_name = name.get('Full', '')
        id_number = record.get('IdNumber', '')
        status = record.get('Status', '')
        alert_state = record.get('AlertState', '')
        origin = record.get('Origin', '')
        
        audit_records = record.get('AuditRecords', {}).get('AuditRecord', [])
        if isinstance(audit_records, dict):
            audit_records = [audit_records]

        if not audit_records:
            data['Id'].append(id_value)
            data['EntityType'].append(entity_type)
            data['Full'].append(full_name)
            data['IdNumber'].append(id_number)
            data['Status'].append(status)
            data['AlertState'].append(alert_state)
            data['Action'].append('')
            data['Note'].append('')
            data['Origin'].append(origin)
        else:
            for audit_record in audit_records:
                data['Id'].append(id_value)
                data['EntityType'].append(entity_type)
                data['Full'].append(full_name)
                data['IdNumber'].append(id_number)
                data['Status'].append(status)
                data['AlertState'].append(alert_state)
                data['Action'].append(audit_record.get('Action', ''))
                data['Note'].append(audit_record.get('Note', ''))
                data['Origin'].append(origin)
    
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