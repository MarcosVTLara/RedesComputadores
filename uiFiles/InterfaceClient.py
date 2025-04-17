from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStyledItemDelegate, QStyleOptionButton,
    QStyle, QTableView, QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QRect, QEvent
from client import Ui_MainWindow  # Gerado a partir do client.ui
import sys


# Modelo de dados dinâmico
class TabelaModelo(QAbstractTableModel):
    def __init__(self, dados):
        super().__init__()
        self.dados = dados

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Data"
            elif section == 1:
                return "Ação"
        return super().headerData(section, orientation, role)

    def rowCount(self, parent=None):
        return len(self.dados)

    def columnCount(self, parent=None):
        return 2  # Valor + Botão

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if col == 0:
                return self.dados[row]
        return None

    def flags(self, index):
        return Qt.ItemIsEnabled
    
    def removeLinha(self, linha):
        if 0 <= linha < len(self.dados):
            self.beginRemoveRows(QModelIndex(), linha, linha)
            self.dados.pop(linha)
            self.endRemoveRows()


# Delegate para mostrar botão na coluna 1
class BotaoDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 1:
            botao = QStyleOptionButton()
            botao.rect = option.rect
            botao.text = "Apagar"
            botao.state = QStyle.State_Enabled
            QApplication.style().drawControl(QStyle.CE_PushButton, botao, painter)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and index.column() == 1:
            linha = index.row()
            if hasattr(model, "removeLinha"):
                model.removeLinha(linha)
        return True
    



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Exemplo de dados dinâmicos
        self.dados = ["Item A", "Item B", "Item C", "Item D"]

        # Modelo da tabela
        self.modelo = TabelaModelo(self.dados)

        self.ui.tableView.setModel(self.modelo)
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)


        # Delegate para a coluna de botões
        self.delegate = BotaoDelegate()
        self.ui.tableView.setItemDelegateForColumn(1, self.delegate)

        # Ajustes visuais opcionais
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.setColumnWidth(0, 300)
        self.ui.tableView.setColumnWidth(1, 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
