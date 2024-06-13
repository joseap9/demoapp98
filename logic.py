import pandas as pd
import xml.etree.ElementTree as ET

def parse_xml_to_dataframe(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    records = []

    ns = {'ns1': 'https://support.bridgerinsight.lexisnexis.com/downloads/xsd/5.0/ResultsExport.xsd'}

    for record in root.findall(".//ns1:ResultRecord", namespaces=ns):
        record_data = {
            "Id": record.find(".//ns1:Id", namespaces=ns).text if record.find(".//ns1:Id", namespaces=ns) is not None else "",
            "EntityType": record.find(".//ns1:InputEntity/ns1:EntityType", namespaces=ns).text if record.find(".//ns1:InputEntity/ns1:EntityType", namespaces=ns) is not None else "",
            "Full": record.find(".//ns1:InputEntity/ns1:Name/ns1:Full", namespaces=ns).text if record.find(".//ns1:InputEntity/ns1:Name/ns1:Full", namespaces=ns) is not None else "",
            "IdNumber": record.find(".//ns1:IdNumber", namespaces=ns).text if record.find(".//ns1:IdNumber", namespaces=ns) is not None else "",
            "Status": record.find(".//ns1:Status", namespaces=ns).text if record.find(".//ns1:Status", namespaces=ns) is not None else "",
            "AlertState": record.find(".//ns1:AlertState", namespaces=ns).text if record.find(".//ns1:AlertState", namespaces=ns) is not None else "",
            "Action": record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Action", namespaces=ns).text if record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Action", namespaces=ns) is not None else "",
            "Note": record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Note", namespaces=ns).text if record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Note", namespaces=ns) is not None else "",
            "Origin": record.find(".//ns1:Origin", namespaces=ns).text if record.find(".//ns1:Origin", namespaces=ns) is not None else ""
        }
        records.append(record_data)

    df = pd.DataFrame(records, columns=columns)
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
    df = parse_xml_to_dataframe(file_path)
    df_final = filter_and_merge_dfs(df)
    print(df_final.head())  # Imprimir las primeras filas del DataFrame para verificar
    print(f"Total de registros: {len(df_final)}")
