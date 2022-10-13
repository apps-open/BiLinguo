from window.interface.statistic_interface import Ui_Dialog
from PyQt5 import QtWidgets
import webbrowser

class Statistic(QtWidgets.QDialog):
    def __init__(self, database):
        super(Statistic, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.export_button.clicked.connect(self.write_report)
        self.db = database
        self.main()

    def write_report(self):
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
        with open(f"/home/nemo/Places/Projects/Python/Vocabulary/report_{self.db.current_table}.html", "w") as file:
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
            <tr><td id="header_param">Tests:</td><td id="value">{self.tests}</td></tr>
            <tr><td id="header_param">Average accuracy:</td><td id="value">{self.avg_accuracy}%</td></tr>
            <tr><td id="header_param">Total points:</td><td id="value">{self.pts}</td></tr>
            <tr><td id="header_param">Total words:</td><td id="value">{self.total_words}</td></tr>
            <tr><td id="header_param">Learned words:</td><td id="value">{self.learned_words}/{self.total_words}</td></tr>
        </table>
    </body>
<html>""")
        webbrowser.open(f"/home/nemo/Places/Projects/Python/Vocabulary/report_{self.db.current_table}.html")

    def main(self):
        data = self.db.fetchall(f"SELECT * FROM \"{self.db.current_table}_statistic\"")
        self.tests = data[len(data)-1][1] + 1
        self.pts = data[len(data)-1][2]
        self.avg_accuracy = data[len(data)-1][4]
        self.total_words = data[len(data)-1][5]
        self.learned_words = data[len(data)-1][6]
        self.ui.tests_label.setText(f"{self.tests}")
        self.ui.avg_accuracy_label.setText(f"{self.avg_accuracy}%")
        self.ui.total_pts_label.setText(f"{self.pts}")
        self.ui.total_words_label.setText(f"{self.total_words}")
        self.ui.learned_words_label.setText(f"{self.learned_words}/{self.total_words}")