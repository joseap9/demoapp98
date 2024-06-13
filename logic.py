import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml_to_dataframe(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    records = []

    namespace = {
        'ns': 'https://support.bridgerinsight.lexisnexis.com/downloads/xsd/5.0/ResultsExport.xsd',
        'i': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    # Procesar registros
    for record in root.findall(".//ns:ResultRecord", namespaces=namespace):
        record_data = {}
        record_data["Id"] = record.findtext("ns:Id", default="", namespaces=namespace)
        record_data["EntityType"] = record.findtext("ns:InputEntity/ns:EntityType", default="", namespaces=namespace)
        record_data["Full"] = record.findtext(".//ns:Name/ns:Full", default="", namespaces=namespace)
        record_data["IdNumber"] = record.findtext("ns:IdNumber", default="", namespaces=namespace)
        record_data["Status"] = record.findtext("ns:Status", default="", namespaces=namespace)
        record_data["AlertState"] = record.findtext("ns:AlertState", default="", namespaces=namespace)
        record_data["Action"] = record.findtext("ns:AuditRecords/ns:AuditRecord/ns:Action", default="", namespaces=namespace)
        record_data["Note"] = record.findtext("ns:AuditRecords/ns:AuditRecord/ns:Note", default="", namespaces=namespace)
        record_data["Origin"] = record.findtext("ns:Origin", default="", namespaces=namespace)

        records.append(record_data)
        print(f"Processed record: {record_data}")

    df = pd.DataFrame(records, columns=columns)
    return df
