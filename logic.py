import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml_to_dataframe(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    records = []

    namespace = {'ns1': 'https://support.bridgerinsight.lexisnexis.com/downloads/xsd/5.0/ResultsExport.xsd'}
    
    for record in root.findall(".//ns1:ResultRecord", namespaces=namespace):
        record_data = {}
        record_data["Id"] = record.findtext(".//ns1:Id", default="", namespaces=namespace)
        record_data["EntityType"] = record.findtext(".//ns1:InputEntity/ns1:EntityType", default="", namespaces=namespace)
        record_data["Full"] = record.findtext(".//ns1:InputEntity/ns1:Name/ns1:Full", default="", namespaces=namespace)
        record_data["IdNumber"] = record.findtext(".//ns1:IdNumber", default="", namespaces=namespace)
        record_data["Status"] = record.findtext(".//ns1:Status", default="", namespaces=namespace)
        record_data["AlertState"] = record.findtext(".//ns1:AlertState", default="", namespaces=namespace)
        record_data["Action"] = record.findtext(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Action", default="", namespaces=namespace)
        record_data["Note"] = record.findtext(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Note", default="", namespaces=namespace)
        record_data["Origin"] = record.findtext(".//ns1:Origin", default="", namespaces=namespace)

        print(f"Processed record: {record_data}")  # Mensaje de depuración
        records.append(record_data)

    df = pd.DataFrame(records, columns=columns)
    return df