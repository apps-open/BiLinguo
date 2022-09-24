from window.interface.statistic_interface import Ui_MainWindow
from PyQt5 import QtWidgets
import webbrowser

class Statistic(QtWidgets.QMainWindow):
    def __init__(self, database):
        super(Statistic, self).__init__()
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__ui.export_button.clicked.connect(self.__write_report)
        self.__db = database
        self.__main()

    def __write_report(self):
        stylesheet = """body {
 background: rgb(255,255,255);
background: -moz-linear-gradient(315deg, rgba(255,255,255,1) 0%, rgba(0,212,255,1) 100%);
background: -webkit-linear-gradient(315deg, rgba(255,255,255,1) 0%, rgba(0,212,255,1) 100%);
background: linear-gradient(315deg, rgba(255,255,255,1) 0%, rgba(0,212,255,1) 100%);
            }
            h1 {
                text-align: center;
                font-family: 'Michroma', sans-serif;
                font-size: 100px;
                font-weight: 400;
            }
            #header_param {
                font-family: 'Michroma', sans-serif;
                font-size: 20px;
                font-weight: 400;
            }
            #value {
                font-family: 'Michroma', sans-serif;
                font-size: 20px;
                font-weight: 300;
            }"""
        with open(f"/home/nemo/Places/Projects/Python/Vocabulary/report_{self.__db.current_table}.html", "w") as file:
            file.write(
                f"""<!DOCTYPE html>

<html>
    <head>
        <title>Statistic</title>
        <link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Paytone+One:wght@400&family=Michroma:wght@400&display=swap" rel="stylesheet">
        <style type="text/css">
            {stylesheet}
        </style>
    </head>
    
    <body >
        <div id="header"><h1>Statistic</h1></div>
        <table>
            <tr><td id="header_param">Tests:</td><td id="value">{self.__tests}</td></tr>
            <tr><td id="header_param">Average accuracy:</td><td id="value">{self.__avg_accuracy}%</td></tr>
            <tr><td id="header_param">Total points:</td><td id="value">{self.__pts}</td></tr>
            <tr><td id="header_param">Total words:</td><td id="value">{self.__total_words}</td></tr>
            <tr><td id="header_param">Learned words:</td><td id="value">{self.__learned_words}/{self.__total_words}</td></tr>
        </table>
    </body>
<html>""")
        webbrowser.open(f"/home/nemo/Places/Projects/Python/Vocabulary/report_{self.__db.current_table}.html")

    def __main(self):
        data = self.__db.fetchall(f"SELECT * FROM \"{self.__db.current_table}_statistic\"")
        self.__tests = data[len(data)-1][1] + 1
        self.__pts = data[len(data)-1][2]
        self.__avg_accuracy = data[len(data)-1][4]
        self.__total_words = data[len(data)-1][5]
        self.__learned_words = data[len(data)-1][6]
        self.__ui.tests_label.setText(f"{self.__tests}")
        self.__ui.avg_accuracy_label.setText(f"{self.__avg_accuracy}%")
        self.__ui.total_pts_label.setText(f"{self.__pts}")
        self.__ui.total_words_label.setText(f"{self.__total_words}")
        self.__ui.learned_words_label.setText(f"{self.__learned_words}/{self.__total_words}")