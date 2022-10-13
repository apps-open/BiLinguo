from PyQt5 import QtWidgets


class QTableWidgetDisabledItem(QtWidgets.QItemDelegate):
    """
    Create a readOnly QTableWidgetItem
    """
    def __init__(self, parent):

        QtWidgets.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        item = QtWidgets.QLineEdit(parent)
        item.setReadOnly(True)
        #item.setEnabled(False)
        return item

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(index.model().data(index))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())