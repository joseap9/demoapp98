import pandas as pd
import xml.etree.ElementTree as ET

def extract_records_from_xml(file_path, action_type):
    tree = ET.parse(file_path)
    root = tree.getroot()

    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    records = []

    ns = {'ns1': 'https://support.bridgerinsight.lexisnexis.com/downloads/xsd/5.0/ResultsExport.xsd'}

    for record in root.findall(".//ns1:ResultRecord", namespaces=ns):
        audit_records = record.findall(".//ns1:AuditRecords/ns1:AuditRecord", namespaces=ns)
        for audit_record in audit_records:
            action = audit_record.find("ns1:Action", namespaces=ns)
            if action is not None and action.text == action_type:
                record_data = {
                    "Id": record.find(".//ns1:Id", namespaces=ns).text if record.find(".//ns1:Id", namespaces=ns) is not None else "",
                    "EntityType": record.find(".//ns1:InputEntity/ns1:EntityType", namespaces=ns).text if record.find(".//ns1:InputEntity/ns1:EntityType", namespaces=ns) is not None else "",
                    "Full": record.find(".//ns1:InputEntity/ns1:Name/ns1:Full", namespaces=ns).text if record.find(".//ns1:InputEntity/ns1:Name/ns1:Full", namespaces=ns) is not None else "",
                    "IdNumber": record.find(".//ns1:IdNumber", namespaces=ns).text if record.find(".//ns1:IdNumber", namespaces=ns) is not None else "",
                    "Status": record.find(".//ns1:Status", namespaces=ns).text if record.find(".//ns1:Status", namespaces=ns) is not None else "",
                    "AlertState": record.find(".//ns1:AlertState", namespaces=ns).text if record.find(".//ns1:AlertState", namespaces=ns) is not None else "",
                    "Action": action.text,
                    "Note": audit_record.find("ns1:Note", namespaces=ns).text if audit_record.find("ns1:Note", namespaces=ns) is not None else "",
                    "Origin": record.find(".//ns1:Origin", namespaces=ns).text if record.find(".//ns1:Origin", namespaces=ns) is not None else ""
                }
                records.append(record_data)

    df = pd.DataFrame(records, columns=columns)
    return df

def create_final_dataframe(df_record_created, df_new_note):
    df_final = df_record_created.copy()
    df_final['Note 2'] = df_final['Id'].map(df_new_note.set_index('Id')['Note'])
    
    def determine_process(row):
        if 'SRS' in row['Note']:
            return 'Retail On Going'
        elif 'ASTRA' in row['Note']:
            return 'Commercial On Going'
        elif 'ORCL' in row['Note']:
            return 'Vendor'
        elif 'WebServices' in row['Origin']:
            return 'Retail On Boarding'
        return ''
    
    df_final['process'] = df_final.apply(lambda row: determine_process(row), axis=1)
    df_final = df_final[df_final['Origin'].str.contains('RealTime') == False]
    
    return df_final

# Ejemplo de uso
if __name__ == "__main__":
    file_path = 'ruta_al_archivo.xml'
    df_record_created = extract_records_from_xml(file_path, 'RecordCreated')
    df_new_note = extract_records_from_xml(file_path, 'NewNote')

    # Crear el DataFrame final
    df_final = create_final_dataframe(df_record_created, df_new_note)
    print(df_final.head())  # Imprimir las primeras filas del DataFrame para verificar
    print(f"Total de registros: {len(df_final)}")
