import sys
from PyQt5.QtWidgets import (
    QApplication
)
from PyQt5.QtGui import QIcon
import os
from MainWindow import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Delta Parser Timeline") 
    app.setApplicationDisplayName("DPT")  
    app.setOrganizationName("DeltaResearch")

    # Imposta l'icona dell'applicazione
    icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icon.icns')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())