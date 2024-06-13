from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel
import pandas as pd
from logic import parse_xml_to_dataframe, filter_and_merge_dfs

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
        df = parse_xml_to_dataframe(file_path)

        # Crear el DataFrame final aplicando el filtro y merge
        self.df_final = filter_and_merge_dfs(df)
        
        # Agregar columna 'process' basada en 'Note' y 'Origin'
        self.df_final['process'] = self.df_final.apply(lambda row: (
            'Retail On Going' if 'SRS' in row['Note'] else
            'Commercial On Going' if 'ASTRA' in row['Note'] else
            'Vendor' if 'ORCL' in row['Note'] else
            'Retail On Boarding' if 'WebServices' in row['Origin'] else
            ''
        ), axis=1)
        
        # Eliminar filas donde 'Origin' contiene 'RealTime'
        self.df_final = self.df_final[~self.df_final['Origin'].str.contains('RealTime', na=False)]

        self.label_status.setText("Proceso completo. Registros encontrados: {}".format(len(self.df_final)))
        self.button_save.setEnabled(True)  # Habilitar el botón de guardar

    def save_file_dialog(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if save_path:
            self.df_final.to_excel(save_path, index=False)
            self.label_status.setText("Archivo guardado exitosamente en: {}".format(save_path))

