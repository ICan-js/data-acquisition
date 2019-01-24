import os
import uuid

from data_app.email.tools import GmailSender
from data_app.thread.stream import StreamThread, EmailSenderThread

from PyQt5.uic import loadUiType
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMainWindow, QFileDialog, QMessageBox

from data_app.system_file.utils import clear_files, create_dir, create_zip

form, base = loadUiType('data_app/ui/main.ui')


class Window(base, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.someImage = None
        self.pathToSave = None
        self.progressValue = 0

        self.saveCount = 0
        self.actualLabel = 0
        self.labels = {
            0: {
            'name': 'idade',
            'picture': 'data_app/res/idade.png'
        }, 1: {
            'name': 'telefone',
            'picture': 'data_app/res/telefone.png'
        }, 2: {
            'name': 'desculpa',
            'picture': 'data_app/res/desculpa.png'
        }, 3: {
            'name': 'amigo',
            'picture': 'data_app/res/amigo.png'
        }}

        self.buttonRestart.clicked.connect(self.restartProcess)
        self.buttonCapture.clicked.connect(self.captureProcess)
        self.buttonAbout.clicked.connect(self.showAboutDialog)

        self.labelOrigem.setPixmap(QPixmap(self.labels[self.actualLabel]['picture']))
        self.labelQtd.setText('Quantidade para finalizar este gesto: 20')
        self.labelGestureName.setText('Nome do gesto: {}'.format(self.labels[self.actualLabel]['name']))

        self.progressBar.setValue(0)

    @pyqtSlot(QImage)
    def updateImage(self, image):
        """Slot to update the image in QLabel via StreamThread
        :param image:
        :return:
        """

        self.someImage = image
        self.labelDestino.setPixmap(QPixmap.fromImage(image))

    def startThread(self):
        """Initialize the StreamThread to update the Image in QLabel
        :return:
        """

        th = StreamThread(self)
        th.imageSignal.connect(self.updateImage)
        th.start()

    def startEmailSenderThread(self):
        """Create a sender email thread
        :return:
        """

        sender = GmailSender('Email com resultados', 'Segue os resultados',
                             'mauricioselecto@gmail.com', 'felipe.carlos@fatec.sp.gov.br', '123@abc..')
        th = EmailSenderThread(self)
        th.emailStatusSignal.connect(self.showCoolMessage)

        th.emailSender = sender
        th.filename = '{}/imagens_para_enviar.zip'.format(self.pathToSave)

        th.start()

    def showCoolMessage(self, value):
        """Method to show a cool message to user
        :return:
        """

        title = "=("
        message = "Ops! Tive algum problema para fazer o envio dos resultados! Verifique sua conexão com a internet"
        if value:
            title = "=D"
            message =  "Obrigado por colaborar! Os resultados foram enviados para meu email =D"
        QMessageBox.information(self, title, message)

    def restartProcess(self):
        """Reset all user's progress
        :return:
        """

        clear_files(self.pathToSave)

        self.progressValue = 0
        self.saveCount = 0
        self.actualLabel = 0

        self.progressBar.setValue(0)

        self.labelQtd.setText('Quantidade para finalizar este gesto: 20')
        self.labelOrigem.setPixmap(QPixmap(self.labels[self.actualLabel]['picture']))

    def captureProcess(self):
        """Method to save user's image in QLabel
        :return:
        """

        try:
            tempPath = os.path.join(self.pathToSave, self.labels[self.actualLabel]['name'] + '_tg')
            fileName = str(uuid.uuid4()).split('-')[4]
            fileName = os.path.join(tempPath, '{}.png'.format(fileName))
            self.someImage.save(fileName)

            self.updateActualLabel()
        except BaseException as error:
            QMessageBox.warning('Erro ao tentar salvar os dados!')

    def definePathToSave(self):
        """Method to open a dialog to select the path to save files
        :return:
        """

        self.pathToSave = str(QFileDialog.getExistingDirectory(self, "Diretório para salvar os dados"))
        self.pathToSave = os.path.join(self.pathToSave, 'imagens_para_tg')

        if not os.path.exists(self.pathToSave):
            os.mkdir(self.pathToSave)

    def showWelcomeDialog(self):
        QMessageBox.information(self, "Oiie", "Olá! Bem-vindo ao programa para ajudar na aquisição de dados" + \
                                    " para meu TG. Aqui você fará 80 imagens de 4 gestos diferentes em LIBRAS" + \
                                    "\nSerá bem legal se você puder variar sua posição e rosto na captura das imagens" + \
                                    "\nSelecione o diretório onde os dados serão salvos e bora começar!")

    def showAboutDialog(self):
        QMessageBox.information(self, "Sobre", "Este é o programa criado para a aquisição de 80 exemplos de gestos" + \
                                        " em LIBRAS. Você colaborando ajuda muito com o desenvolvimento do TG =D")

    def updateActualLabel(self):
        """Method to update all information labels for the user
        :return:
        """

        create_dir(os.path.join(self.pathToSave, self.labels[self.actualLabel]['name'] + '_tg'))

        self.saveCount += 1

        self.progressValue += 0.125 * 10
        self.progressBar.setValue(self.progressValue)

        if self.progressValue >= 100.0:
            QMessageBox.information(self, "Fim",
                                    "O processo chegou ao fim! Obrigado por colaborar! Agora vou enviar os dados para meu email. Clique em ok e aguarde a confirmação do processo")
            # ZIP
            create_zip(self.pathToSave)

            # Start email thread
            self.startEmailSenderThread()
        else:
            if self.saveCount == 20:
                self.actualLabel += 1
                self.saveCount = 0

            self.labelQtd.setText('Quantidade para finalizar este gesto: {}'.format(str(20 - self.saveCount)))
            self.labelOrigem.setPixmap(QPixmap(self.labels[self.actualLabel]['picture']))
            self.labelGestureName.setText('Nome do gesto: {}'.format(self.labels[self.actualLabel]['name']))
