import xml.etree.ElementTree as ET
from collections import defaultdict

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = defaultdict(set)
    
    def get_namespaces(elem, namespaces):
        for ns in elem.iter():
            if ns.tag[0] == "{":
                uri, tag = ns.tag[1:].split("}")
                namespaces[uri].add(tag)
        return namespaces
    
    namespaces = get_namespaces(root, namespaces)
    
    print("Namespaces found in the XML:")
    for ns, tags in namespaces.items():
        print(f"Namespace: {ns}")
        print("Tags:", ", ".join(tags))
    
    def print_tree(element, indent=""):
        print(f"{indent}Tag: {element.tag}, Attributes: {element.attrib}")
        for child in element:
            print_tree(child, indent + "  ")
    
    print("\nXML Tree Structure:")
    print_tree(root)
    
    return tree, namespaces

def find_element_path(tree, tag_name, namespaces):
    for ns, tags in namespaces.items():
        if tag_name in tags:
            tag_with_ns = f"{{{ns}}}{tag_name}"
            elements = tree.findall(f".//{tag_with_ns}")
            for elem in elements:
                print(f"\nFull path for tag '{tag_name}':")
                print(elem.tag, elem.attrib)
                parent_map = {c: p for p in tree.iter() for c in p}
                path = [elem.tag]
                parent = parent_map.get(elem)
                while parent is not None:
                    path.append(parent.tag)
                    parent = parent_map.get(parent)
                print(" -> ".join(reversed(path)))
            return elements
    print(f"Tag '{tag_name}' not found in the XML.")
    return None

# Ejemplo de uso
file_path = 'tu_archivo.xml'
tree, namespaces = parse_xml(file_path)

# Busca la etiqueta específica que deseas, por ejemplo, 'Full'
elements = find_element_path(tree, 'Full', namespaces)