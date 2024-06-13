from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel
from logic import parse_xml_to_dataframe

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML to DataFrame")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Seleccione un archivo XML:")
        self.layout.addWidget(self.label)

        self.button = QPushButton("Seleccionar archivo")
        self.button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo XML", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_name:
            df = parse_xml_to_dataframe(file_name)
            self.result_label.setText(f"Archivo cargado con éxito. {len(df)} registros encontrados.")
            print(df)  # Para visualizar el DataFrame en la consola
