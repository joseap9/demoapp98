from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel
import pandas as pd
from logic import extract_records_from_xml, create_final_dataframe

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML to DataFrame")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Seleccione un archivo XML:")
        self.layout.addWidget(self.label)

        self.button_select = QPushButton("Seleccionar archivo")
        self.button_select.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.button_select)

        self.label_status = QLabel("")
        self.layout.addWidget(self.label_status)

        self.button_save = QPushButton("Guardar como Excel")
        self.button_save.clicked.connect(self.save_file_dialog)
        self.button_save.setEnabled(False)  # Deshabilitar hasta que el proceso esté completo
        self.layout.addWidget(self.button_save)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.df_final = pd.DataFrame()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo XML", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_name:
            self.process_file(file_name)

    def process_file(self, file_path):
        self.label_status.setText("Procesando...")
        df_record_created = extract_records_from_xml(file_path, 'RecordCreated')
        df_new_note = extract_records_from_xml(file_path, 'NewNote')

        # Crear el DataFrame final
        self.df_final = create_final_dataframe(df_record_created, df_new_note)
        
        self.label_status.setText("Proceso completo. Registros encontrados: {}".format(len(self.df_final)))
        self.button_save.setEnabled(True)  # Habilitar el botón de guardar

    def save_file_dialog(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if save_path:
            self.df_final.to_excel(save_path, index=False)
            self.label_status.setText("Archivo guardado exitosamente en: {}".format(save_path))

