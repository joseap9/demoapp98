from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import pandas as pd
from logic import xml_to_dict, parse_dict_to_dataframe, filter_and_merge_dfs

class PandasModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame()):
        QAbstractTableModel.__init__(self)
        self._df = df

    def rowCount(self, parent=None):
        return len(self._df)

    def columnCount(self, parent=None):
        return self._df.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._df.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._df.columns[col]
        return None

    def setDataFrame(self, df):
        self._df = df
        self.layoutChanged.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML to DataFrame")
        self.setGeometry(100, 100, 800, 600)

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

        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.df_final = pd.DataFrame()
        self.model = PandasModel(self.df_final)
        self.table_view.setModel(self.model)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo XML", "", "XML Files (*.xml);;All Files (*)", options=options)
        if file_name:
            self.process_file(file_name)

    def process_file(self, file_path):
        self.label_status.setText("Procesando...")
        xml_dict = xml_to_dict(file_path)
        df = parse_dict_to_dataframe(xml_dict)

        # Crear el DataFrame final aplicando el filtro y merge
        self.df_final = filter_and_merge_dfs(df)

        # Actualizar el modelo del TableView con los primeros 15 registros
        self.model.setDataFrame(self.df_final.head(15))
        
        self.label_status.setText("Proceso completo. Registros encontrados: {}".format(len(self.df_final)))
        self.button_save.setEnabled(True)  # Habilitar el botón de guardar

    def save_file_dialog(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Guardar archivo como", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if save_path:
            self.df_final.to_excel(save_path, index=False)
            self.label_status.setText("Archivo guardado exitosamente en: {}".format(save_path))

