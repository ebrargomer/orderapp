import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QWidget
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a database connection
        self.conn = sqlite3.connect('database.db')

        # Create a table to store orders
        self.conn.execute('''CREATE TABLE IF NOT EXISTS orders
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             siparis_no INTEGER,
                             musteri_adi TEXT,
                             firma TEXT,
                             urun TEXT
                             tarih TEXT,
                             durum TEXT)''')
        self.conn.commit()

        # Create a table widget to display orders
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Sipariş No', 'Müşteri adı', 'Firma', 'Ürün', 'Durum', 'Sipariş Tarihi'])
        self.table.resize(500, 300)

        # Create line edits and combo boxes for adding and editing orders
        self.siparis_no_edit = QLineEdit(self)
        self.musteri_adi_edit = QLineEdit(self)
        self.firma_edit = QLineEdit(self)
        self.urun_edit = QLineEdit(self)
        self.tarih_edit = QLineEdit(self)
        self.durum_combo = QComboBox(self)
        self.durum_combo.addItems(['Sipariş alındı', 'Sipariş firmaya iletildi', 'Sipariş tamamlandı'])

        # Create buttons for adding and editing orders
        self.add_button = QPushButton('Sipariş Ekle', self)
        self.edit_button = QPushButton('Siparişi Düzenle', self)

        # Connect signals and slots
        self.add_button.clicked.connect(self.add_order)
        self.edit_button.clicked.connect(self.edit_order)

        # Set the layout
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.siparis_no_edit)
        layout.addWidget(self.musteri_adi_edit)
        layout.addWidget(self.firma_edit)
        layout.addWidget(self.urun_edit)
        layout.addWidget(self.tarih_edit)
        layout.addWidget(self.durum_combo)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Update the table with the current orders
        self.update_table()

    def add_order(self):
        # Get the values from the line edits and combo box
        siparis_no = int(self.siparis_no_edit.text())
        musteri_adi = self.musteri_adi_edit.text()
        firma = self.firma_edit.text()
        urun = int(self.urun_edit.text())
        tarih = self.tarih_edit.text()
        durum = self.durum_combo.currentText()

        # Insert the values into the database
        self.conn.execute('INSERT INTO orders (siparis_no, musteri_adi, firma, urun, tarih, durum) VALUES (?,?,?,?,?,?)',
                           (siparis_no, musteri_adi, firma, urun, tarih, durum))
        self.conn.commit()

        # Clear the line edits
        self.siparis_no_edit.clear()
        self.musteri_adi_edit.clear()
        self.date_edit.clear()
        self.firma_edit.clear()
        self.urun_edit.clear()
        self.musteri_adi_edit.clear()
        self.tarih_edit.clear()
        # Update the table with the new order
        self.update_table()

    def edit_order(self):
        # Get the current row from the table
        current_row = self.table.currentRow()

        if current_row != -1:
            # Get the ID of the selected order
            order_id = self.table.item(current_row, 0).text()

            # Get the values from the line edits and combo box
            siparis_no = int(self.siparis_no_edit.text())
            musteri_adi = self.musteri_adi_edit.text()
            firma = self.firma_edit.text()
            urun = int(self.urun_edit.text())
            tarih = self.tarih_edit.text()
            durum = self.durum_combo.currentText()

            # Update the order in the database
            self.conn.execute('UPDATE orders SET siparis_no=?, musteri_adi=?, firma=?, urun=? , tarih=?, durum=? WHERE id=?',
                               (siparis_no, musteri_adi, firma, urun, tarih, durum,order_id))
            self.conn.commit()

            # Clear the line edits
            self.order_number_edit.clear()
            self.customer_name_edit.clear

if __name__ == '__main__':
    # Create a new QApplication instance
    app = QApplication(sys.argv)

    # Create a new MyWindow instance
    window = MyWindow()

    # Show the window
    window.show()

    # Start the event loop
    sys.exit(app.exec_())