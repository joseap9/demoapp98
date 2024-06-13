import pandas as pd
import xml.etree.ElementTree as ET

def parse_xml_to_dataframe(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    columns = ["Id", "EntityType", "Full", "IdNumber", "Status", "AlertState", "Action", "Note", "Origin"]
    records = []

    ns = {'ns1': 'https://support.bridgerinsight.lexisnexis.com/downloads/xsd/5.0/ResultsExport.xsd'}

    for record in root.findall(".//ns1:ResultRecord", namespaces=ns):
        record_data = {}
        for column in columns:
            record_data[column] = ""

        record_data["Id"] = record.find(".//ns1:Id", namespaces=ns).text if record.find(".//ns1:Id", namespaces=ns) is not None else ""
        record_data["EntityType"] = record.find(".//ns1:InputEntity/ns1:EntityType", namespaces=ns).text if record.find(".//ns1:InputEntity/ns1:EntityType", namespaces=ns) is not None else ""
        record_data["Full"] = record.find(".//ns1:InputEntity/ns1:Name/ns1:Full", namespaces=ns).text if record.find(".//ns1:InputEntity/ns1:Name/ns1:Full", namespaces=ns) is not None else ""
        record_data["IdNumber"] = record.find(".//ns1:IdNumber", namespaces=ns).text if record.find(".//ns1:IdNumber", namespaces=ns) is not None else ""
        record_data["Status"] = record.find(".//ns1:Status", namespaces=ns).text if record.find(".//ns1:Status", namespaces=ns) is not None else ""
        record_data["AlertState"] = record.find(".//ns1:AlertState", namespaces=ns).text if record.find(".//ns1:AlertState", namespaces=ns) is not None else ""
        record_data["Action"] = record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Action", namespaces=ns).text if record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Action", namespaces=ns) is not None else ""
        record_data["Note"] = record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Note", namespaces=ns).text if record.find(".//ns1:AuditRecords/ns1:AuditRecord/ns1:Note", namespaces=ns) is not None else ""
        record_data["Origin"] = record.find(".//ns1:Origin", namespaces=ns).text if record.find(".//ns1:Origin", namespaces=ns) is not None else ""

        records.append(record_data)

    df = pd.DataFrame(records, columns=columns)
    return df