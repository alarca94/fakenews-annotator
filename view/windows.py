import os
import re

import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Annotator for linguists")

        self.row_id = 0
        self.new_row_id = 0
        self.data = None
        self.new_data = None
        self.save_filename = ''
        self.delimiter = '||'
        self.columns = ['SourceType', 'Title', 'Content', 'Indicator', 'OriginId', 'Label']

        # -------------- SETTING THE TOOLBAR -------------- #
        toolbar = QtWidgets.QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        toolbar.addSeparator()

        self.status = QtWidgets.QStatusBar(self)
        self.default_styleSheet = self.status.styleSheet()
        self.setStatusBar(self.status)

        button_action = QtWidgets.QAction(QtGui.QIcon('./assets/address-book-open.png'), 'Open File', self)
        button_action.triggered.connect(self.open_file)
        toolbar.addAction(button_action)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        font = button_action.font()
        font.setPointSize(15)
        button_action.setFont(font)
        # .setFontStyleHint(QtGui.QFont.Times)

        # -------------- SETTING THE LAYOUTS -------------- #
        gen_layout = QtWidgets.QVBoxLayout()
        upper_layout = QtWidgets.QHBoxLayout()
        bottom_layout = QtWidgets.QHBoxLayout()
        self.grid_layout = QtWidgets.QGridLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.grid_layout2 = QtWidgets.QGridLayout()
        gen_layout.setAlignment(Qt.AlignCenter)
        upper_layout.setAlignment(Qt.AlignCenter)
        bottom_layout.setAlignment(Qt.AlignCenter)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        self.grid_layout2.setAlignment(Qt.AlignCenter)

        min_cbox_width = 150
        type_box = QtWidgets.QComboBox()
        type_box.addItems(['Newspaper', 'Twitter', 'Facebook', 'Other'])
        type_box.setMinimumWidth(min_cbox_width)

        default_size = (700, 100)

        title_text = QtWidgets.QTextEdit()
        title_text.setPlaceholderText('Enter the title of the article (if any)')
        title_text.setMinimumSize(default_size[0], default_size[1])

        content_text = QtWidgets.QTextEdit()
        content_text.setPlaceholderText('Enter the content of the article')
        content_text.setMinimumSize(default_size[0], default_size[1])

        question_ind = QtWidgets.QTextEdit()
        question_ind.setPlaceholderText('Enter the question indicator (if any)')
        question_ind.setMinimumSize(default_size[0], default_size[1])

        label_box = QtWidgets.QComboBox()
        label_box.addItems(['True', 'Partially True', 'Partially False', 'False'])
        label_box.setMinimumWidth(min_cbox_width)

        form = {'Source Type': type_box, 'Title': title_text, 'Context': content_text,
                'Question Indicator': question_ind, 'label': label_box}

        for text, field in form.items():
            self.form_layout.addRow(QtWidgets.QLabel(text), field)

        self.form_layout.setLabelAlignment(Qt.AlignLeft)

        label = QtWidgets.QLabel('Question')
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('background-color:#90D8FE;color:#000000;font-weight: bold;')
        label2 = QtWidgets.QLabel('Answer')
        label2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet('background-color:#90D8FE;color:#000000;font-weight: bold;')
        label3 = QtWidgets.QLabel()
        label3.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label3.setAlignment(Qt.AlignJustify)
        label3.setWordWrap(True)
        label4 = QtWidgets.QLabel()
        label4.setTextInteractionFlags(Qt.TextSelectableByMouse)
        label4.setAlignment(Qt.AlignJustify)
        label4.setWordWrap(True)

        links = QtWidgets.QTextBrowser()
        links.setAcceptRichText(True)
        links.setOpenExternalLinks(True)
        # links.setStyleSheet('background-color:#90D8FE;color:#000000;')
        links.setFixedHeight(100)

        self.grid_layout.addWidget(label, 0, 0)
        self.grid_layout.addWidget(label2, 0, 1)
        self.grid_layout.addWidget(label3, 1, 0)
        self.grid_layout.addWidget(label4, 1, 1)
        self.grid_layout.addWidget(links, 2, 0, 1, 2)

        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)
        self.grid_layout.setRowStretch(0, 1)
        self.grid_layout.setRowStretch(1, 1)
        self.grid_layout.setSpacing(10)

        prev_button = QtWidgets.QPushButton('<<')
        prev_button.clicked.connect(self.get_prev_instance)
        prev_button.setEnabled(False)
        next_button = QtWidgets.QPushButton('>>')
        next_button.clicked.connect(self.get_next_instance)
        next_button.setEnabled(False)
        save_button = QtWidgets.QPushButton('Save')
        save_button.clicked.connect(self.save_instance)
        save_button.setMinimumWidth(100)
        save_button.setEnabled(False)
        remove_button = QtWidgets.QPushButton('Remove')
        remove_button.clicked.connect(self.remove_instance)
        remove_button.setMinimumWidth(100)
        remove_button.setEnabled(False)

        self.grid_layout2.addWidget(prev_button, 0, 0)
        self.grid_layout2.addWidget(next_button, 0, 1)
        self.grid_layout2.addWidget(save_button, 2, 0)
        self.grid_layout2.addWidget(remove_button, 2, 1)

        upper_layout.addLayout(self.grid_layout)
        bottom_layout.addLayout(self.form_layout, 75)
        bottom_layout.addLayout(self.grid_layout2, 25)

        gen_layout.addLayout(upper_layout, 25)
        gen_layout.addLayout(bottom_layout, 75)

        widget = QtWidgets.QWidget()
        widget.setLayout(gen_layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    def get_prev_instance(self):
        if self.row_id == 0:
            self.set_style('error')
            self.status.showMessage('There is no previous row', 5000)
        else:
            self.row_id -= 1
            self.update_screen_record()
            self.clean_form_layout()

    def update_screen_record(self):
        self.grid_layout.itemAt(2).widget().setText(self.data.question.iloc[self.row_id])
        self.grid_layout.itemAt(3).widget().setText(self.data.answer.iloc[self.row_id])
        if not pd.isna(self.data.links.iloc[self.row_id]):
            self.grid_layout.itemAt(4).widget().setHtml(self.process_links_field(self.data.links.iloc[self.row_id]))
        else:
            self.grid_layout.itemAt(4).widget().setText('')

    def clean_form_layout(self):
        for i in range(1, self.form_layout.count(), 2):
            if type(self.form_layout.itemAt(i).widget()) == QtWidgets.QComboBox:
                self.form_layout.itemAt(i).widget().setCurrentIndex(0)
            elif type(self.form_layout.itemAt(i).widget()) == QtWidgets.QTextEdit:
                self.form_layout.itemAt(i).widget().setText('')

    def get_next_instance(self):
        if self.row_id == (self.data.shape[0]-1):
            self.set_style('error')
            self.status.showMessage('This is the last record in the file', 5000)
        else:
            self.row_id += 1
            self.update_screen_record()
            self.clean_form_layout()

    def save_instance(self):
        if self.save_filename == '':
            self.save_file_dialog()

            if self.save_filename != '':
                if '.' not in self.save_filename:
                    self.save_filename += '.csv'

                if not os.path.isfile(self.save_filename):
                    with open(self.save_filename, 'a') as f:
                        f.write(self.delimiter.join(self.columns) + '\n')

        if self.save_filename != '':
            record = [self.form_layout.itemAt(1).widget().currentText(),
                      self.form_layout.itemAt(3).widget().toPlainText(),
                      self.form_layout.itemAt(5).widget().toPlainText(),
                      self.form_layout.itemAt(7).widget().toPlainText(),
                      self.data.iloc[self.row_id].id,
                      self.form_layout.itemAt(9).widget().currentText()]

            self.clean_form_layout()

            with open(self.save_filename, 'a') as f:
                f.write(self.delimiter.join(record) + '\n')

            self.set_style('success')
            self.status.showMessage('Successfully saved record!', 4000)

            self.grid_layout2.itemAt(3).widget().setEnabled(True)

    def remove_instance(self):
        with open(self.save_filename, "a+", encoding="utf-8") as file:
            file.seek(0, os.SEEK_END)
            pos = file.tell() - 1

            while pos > 0 and file.read(1) != "\n":
                pos -= 1
                file.seek(pos, os.SEEK_SET)

            if pos > 0:
                file.seek(pos, os.SEEK_SET)
                file.truncate()

            file.write('\n')

        self.grid_layout2.itemAt(3).widget().setEnabled(False)

        self.set_style('success')
        self.status.showMessage('Successfully removed the last record!', 4000)

    def set_style(self, style):
        if style == 'error':
            self.status.setStyleSheet(
                "QStatusBar{color:red;font-weight:bold;}")
        elif style == 'success':
            self.status.setStyleSheet(
                "QStatusBar{color:green;font-weight:bold;}")
        elif style == 'default':
            self.status.setStyleSheet(self.default_styleSheet)

    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                            "All Files (*);;Python Files (*.py)", options=options)
        if filename:
            if filename.endswith('csv'):
                self.data = pd.read_csv(filename, delimiter='\t')
                self.update_screen_record()

                self.grid_layout2.itemAt(0).widget().setEnabled(True)
                self.grid_layout2.itemAt(1).widget().setEnabled(True)
                self.grid_layout2.itemAt(2).widget().setEnabled(True)
            else:
                self.set_style('error')
                self.status.showMessage('Selected File does not have the correct format (.csv file)', 5000)

    def save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        options |= QtWidgets.QFileDialog.DontConfirmOverwrite
        self.save_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                                      "All Files (*);;Text Files (*.txt)",
                                                                      options=options)

    @staticmethod
    def process_links_field(text):
        new_text = re.sub(r' (\[LINK: \d\])', r'\n\1', text)
        new_text = re.sub(r'(\[LINK: \d\])( => )(.*)(\n)?', r'<a href="\3">\1</a>\2\3<br/>', new_text)
        return new_text