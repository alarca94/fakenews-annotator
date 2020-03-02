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
        self.delimiter = '|'
        self.columns = ['SourceType', 'SourceField', 'Title', 'Subtitle', 'Content', 'Indicator', 'OriginId', 'Label']

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
        max_cbox_width = 300
        type_box = QtWidgets.QComboBox()
        type_box.addItems(['Newspaper', 'Blog/Magazine', 'Twitter', 'Facebook', 'Other'])
        type_box.setMinimumWidth(min_cbox_width)
        type_box.setMaximumWidth(max_cbox_width)

        origin = QtWidgets.QComboBox()
        origin.addItems(['Links Question', 'Links Answer', 'Question', 'Answer'])
        origin.setMinimumWidth(min_cbox_width)
        origin.setMaximumWidth(max_cbox_width)

        default_size = (600, 100)

        title_text = QtWidgets.QTextEdit()
        title_text.setPlaceholderText('Enter the title of the article (if any)')
        title_text.setMinimumSize(default_size[0], default_size[1])
        title_text.setAcceptRichText(False)

        subtitle_text = QtWidgets.QTextEdit()
        subtitle_text.setPlaceholderText('Enter the subtitle of the article (if any)')
        subtitle_text.setMinimumSize(default_size[0], default_size[1])
        subtitle_text.setAcceptRichText(False)

        content_text = QtWidgets.QTextEdit()
        content_text.setPlaceholderText('Enter the content of the article')
        content_text.setMinimumSize(default_size[0], default_size[1])
        content_text.setAcceptRichText(False)

        question_ind = QtWidgets.QTextEdit()
        question_ind.setPlaceholderText('Enter the question indicator (if any)')
        question_ind.setMinimumSize(default_size[0], default_size[1])
        question_ind.setAcceptRichText(False)

        label_box = QtWidgets.QComboBox()
        label_box.addItems(['True', 'Indefinite', 'False'])
        label_box.setMinimumWidth(min_cbox_width)
        label_box.setMaximumWidth(max_cbox_width)

        form = {'Source Type': type_box, 'Source Field': origin, 'Title': title_text, 'Subtitle': subtitle_text, 'Content': content_text,
                'Question Indicator': question_ind, 'Label': label_box}
        self.form_dict = {key: i for i, key in enumerate(form.keys())}

        for text, field in form.items():
            self.form_layout.addRow(QtWidgets.QLabel(text), field)

        self.form_layout.setLabelAlignment(Qt.AlignLeft)

        qa_height = 50
        label = QtWidgets.QLabel('Question')
        label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label.setAlignment(Qt.AlignCenter)
        label.setFixedHeight(qa_height)
        label.setStyleSheet('background-color:#90D8FE;color:#000000;font-weight: bold;')
        label2 = QtWidgets.QLabel('Answer')
        label2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label2.setAlignment(Qt.AlignCenter)
        label2.setFixedHeight(qa_height)
        label2.setStyleSheet('background-color:#90D8FE;color:#000000;font-weight: bold;')
        label3 = QtWidgets.QTextBrowser()
        label3.setAcceptRichText(True)
        label3.setOpenExternalLinks(True)
        label3.setReadOnly(True)
        label4 = QtWidgets.QTextEdit()
        label4.setReadOnly(True)
        label4.setAcceptRichText(False)

        links = QtWidgets.QTextBrowser()
        links.setAcceptRichText(True)
        links.setOpenExternalLinks(True)
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

        prev_button = QtWidgets.QPushButton('<<', shortcut=Qt.Key_Left)
        prev_button.clicked.connect(self.get_prev_instance)
        prev_button.setEnabled(False)
        next_button = QtWidgets.QPushButton('>>', shortcut=Qt.Key_Right)
        next_button.clicked.connect(self.get_next_instance)
        next_button.setEnabled(False)
        save_button = QtWidgets.QPushButton('Save', shortcut=QtGui.QKeySequence.Save)
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

        gen_layout.addLayout(upper_layout, 50)
        gen_layout.addLayout(bottom_layout, 50)

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

        print(self.row_id)

    def update_screen_record(self):
        if not pd.isna(self.data.links.iloc[self.row_id]):
            self.grid_layout.itemAt(4).widget().setHtml(self.process_links_field(self.data.links.iloc[self.row_id]))

            if not pd.isna(self.data.iloc[self.row_id].evidences):
                n_evidences = len(re.findall(r'([lL]ink ?(\d)|\[LINK: ?\d\])', self.data.iloc[self.row_id].evidences))
                if n_evidences > len(re.findall(r'([lL]ink ?(\d)|\[LINK: ?\d\])',
                                                self.grid_layout.itemAt(4).widget().toPlainText())):
                    self.set_style('warning')
                    self.status.showMessage('Check number of links in the original record and report possible errors',
                                            5000)
        else:
            # If answer has links that have not been added to the table links field...
            if not pd.isna(self.data.evidences.iloc[self.row_id]) \
                    and not pd.isna(self.data.answer.iloc[self.row_id]) \
                    and re.findall(r'link ?(\d)', self.data.iloc[self.row_id].answer.lower()):
                self.data.answer.iloc[self.row_id] = re.sub(r'[lL]ink ?(\d):?', r'[LINK: \1]',
                                                            self.data.answer.iloc[self.row_id])
                self.data.links.iloc[self.row_id] = re.sub(r'[lL]ink ?(\d):?', r'[LINK: \1] =>',
                                                           self.data.evidences.iloc[self.row_id])
                self.update_screen_record()

                return
            else:
                self.grid_layout.itemAt(4).widget().setText('')

        if not pd.isna(self.data.question.iloc[self.row_id]):
            question = re.sub('(https://dl.airtable)([^\s]*)', r'<a href="\1\2">[MEDIA_FILE]</a>',
                              self.data.question.iloc[self.row_id])
            self.grid_layout.itemAt(2).widget().setHtml(question)
        elif not pd.isna(self.data.mediaAttached.iloc[self.row_id]):
            self.grid_layout.itemAt(2).widget().setHtml('<a href="' + self.data.mediaAttached.iloc[self.row_id] +
                                                        '">[MEDIA_FILE]</a>')
        else:
            self.grid_layout.itemAt(2).widget().setText('')

        if not pd.isna(self.data.answer.iloc[self.row_id]):
            self.grid_layout.itemAt(3).widget().setText(self.data.answer.iloc[self.row_id])
        else:
            self.grid_layout.itemAt(3).widget().setText('')

    def clean_form_layout(self):
        for i in range(1, self.form_layout.count(), 2):
            if type(self.form_layout.itemAt(i).widget()) == QtWidgets.QComboBox:
                self.form_layout.itemAt(i).widget().setCurrentIndex(0)
            elif type(self.form_layout.itemAt(i).widget()) == QtWidgets.QTextEdit:
                self.form_layout.itemAt(i).widget().setText('')

    def get_next_instance(self):
        if self.row_id == (self.data.shape[0] - 1):
            self.set_style('error')
            self.status.showMessage('This is the last record in the file', 5000)
        else:
            self.row_id += 1
            self.update_screen_record()
            self.clean_form_layout()

        print(self.row_id)

    def save_instance(self):
        if self.save_filename == '':
            self.save_file_dialog()

            if self.save_filename != '':
                if '.' not in self.save_filename:
                    self.save_filename += '.csv'

                if not os.path.isfile(self.save_filename):
                    with open(self.save_filename, 'a') as f:
                        f.write(self.delimiter.join(self.columns) + '\n')

                self.saved_data = pd.read_csv(self.save_filename, sep=self.delimiter)

        if self.save_filename != '':
            record = [self.form_layout.itemAt(self.form_dict['Source Type'] * 2 + 1).widget().currentText(),
                      self.form_layout.itemAt(self.form_dict['Source Field'] * 2 + 1).widget().currentText(),
                      self.form_layout.itemAt(self.form_dict['Title'] * 2 + 1).widget().toPlainText(),
                      self.form_layout.itemAt(self.form_dict['Subtitle'] * 2 + 1).widget().toPlainText(),
                      self.form_layout.itemAt(self.form_dict['Content'] * 2 + 1).widget().toPlainText(),
                      self.form_layout.itemAt(self.form_dict['Question Indicator'] * 2 + 1).widget().toPlainText(),
                      self.data.iloc[self.row_id].id,
                      self.form_layout.itemAt(self.form_dict['Label'] * 2 + 1).widget().currentText()]

            self.clean_form_layout()
            self.saved_data = self.saved_data.append(pd.Series(record, index=self.columns), ignore_index=True)

            with open(self.save_filename, 'a', newline='\n', encoding='utf-8', errors='ignore') as f:
                self.saved_data.tail(1).to_csv(f, sep=self.delimiter, index=False, header=False)

            self.set_style('success')
            self.status.showMessage('Successfully saved record!', 4000)

            self.grid_layout2.itemAt(3).widget().setEnabled(True)

    def remove_instance(self):
        matches = 0
        requires_quotes = False
        last_field = False
        with open(self.save_filename, "a+", encoding="utf-8", errors='ignore') as file:
            file.seek(0, os.SEEK_END)
            pos = file.tell()

            prev_char = ''
            curr_char = file.read(1)
            while pos > 0 and (not last_field or curr_char != '\n'):
                pos -= 1

                if curr_char == self.delimiter:
                    if requires_quotes and prev_char == '"':
                        matches += 1
                        requires_quotes = False
                    elif not requires_quotes:
                        matches += 1

                    if matches == self.saved_data.shape[1] - 1:
                        last_field = True

                elif curr_char == '"' and prev_char == self.delimiter:
                    requires_quotes = True

                file.seek(pos, os.SEEK_SET)

                prev_char = curr_char
                curr_char = file.read(1)

            if pos > 0:
                pos += 1
                file.seek(pos, os.SEEK_SET)
                file.truncate()

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
        elif style == 'warning':
            self.status.setStyleSheet(
                "QStatusBar{color:yellow;font-weight:bold;}")
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
        new_text = text.replace('//: ', '//').replace('com.', 'com')
        new_text = re.sub(r' (\[LINK: \d\])', r'\n\1', new_text)
        new_text = re.sub(r'(\[LINK: \d\])( => )(.*)(\n)?',
                          r'<a href="\3"><font color="#3085FF">\1</font></a>\2\3<br/>', new_text)
        return new_text
