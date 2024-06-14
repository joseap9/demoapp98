import pandas as pd
import xml.etree.ElementTree as ET

# Función para parsear el XML y extraer los valores de la etiqueta "Full"
def parse_xml_to_dataframe(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Espacios de nombres del XML (debes ajustarlos si es necesario)
    ns = {
        'ns': 'https://support.bridgerinsight.lexisnexis.com/downloads/xsd/5.0/ResultsExport.xsd',
        'i': 'http://www.w3.org/2001/XMLSchema-instance'
    }

    # Lista para almacenar los valores extraídos
    full_values = []

    # Iterar sobre todos los elementos que contienen la etiqueta "Full"
    for elem in root.findall('.//ns:resultrecord', ns):
        full_tag = elem.find('.//ns:Full', ns)
        if full_tag is not None:
            full_values.append(full_tag.text)
        else:
            full_values.append(None)

    # Crear un DataFrame con los valores extraídos
    df = pd.DataFrame(full_values, columns=['Full'])
    
    return df