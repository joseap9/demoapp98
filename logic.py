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