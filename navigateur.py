import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar, QAction, QVBoxLayout, 
    QWidget, QTabWidget, QPushButton, QLabel, QDialog, QListWidget, QMenu, QMenuBar, QCheckBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPixmap

class FenetreAPropos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("À propos de NavigBack")
        self.setFixedSize(400, 200)
        
        logo = QLabel(self)
        pixmap = QPixmap("logo.png")  # Assurez-vous d'avoir un fichier "logo.png" dans le répertoire
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        
        version = QLabel("Version 1.0", self)
        version.setAlignment(Qt.AlignCenter)
        
        description = QLabel("© Superea Systems 2024", self)
        description.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(version)
        layout.addWidget(description)
        self.setLayout(layout)

class FenetreHistorique(QDialog):
    def __init__(self, historique, naviguer_vers_url):
        super().__init__()
        self.setWindowTitle("Historique")
        self.setFixedSize(300, 400)
        
        self.historique_liste = QListWidget()
        self.historique_liste.addItems(historique)
        
        self.historique_liste.itemDoubleClicked.connect(
            lambda item: naviguer_vers_url(item.text())
        )
        
        layout = QVBoxLayout()
        layout.addWidget(self.historique_liste)
        self.setLayout(layout)

class FenetreParametres(QDialog):
    def __init__(self, activer_mode_sombre, changer_mode_sombre):
        super().__init__()
        self.setWindowTitle("Paramètres")
        self.setFixedSize(300, 200)
        
        self.checkbox_mode_sombre = QCheckBox("Activer le mode sombre")
        self.checkbox_mode_sombre.setChecked(activer_mode_sombre)
        self.checkbox_mode_sombre.stateChanged.connect(changer_mode_sombre)
        
        layout = QVBoxLayout()
        layout.addWidget(self.checkbox_mode_sombre)
        self.setLayout(layout)

class NavigateurAvecOnglets(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NavigBack")
        self.setGeometry(100, 100, 800, 600)
        
        self.activer_mode_sombre = False  # Par défaut, le mode sombre est désactivé

        self.onglets = QTabWidget()
        self.onglets.setTabsClosable(True)
        self.onglets.tabCloseRequested.connect(self.fermer_onglet)
        self.onglets.currentChanged.connect(self.changement_onglet)
        self.onglets.setMovable(True)
        self.setCentralWidget(self.onglets)

        self.bouton_plus = QPushButton("+")
        self.bouton_plus.setFixedSize(30, 30)
        self.bouton_plus.clicked.connect(self.ajouter_onglet)
        self.onglets.setCornerWidget(self.bouton_plus, Qt.TopRightCorner)

        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Entrez une URL ou une recherche...")
        self.url_bar.returnPressed.connect(self.naviguer_vers_url)
        self.toolbar.addWidget(self.url_bar)

        # Ajout des icônes dynamiques
        self.bouton_retour = QAction(QIcon("back_dark.png"), "Retour", self)
        self.bouton_retour.triggered.connect(lambda: self.onglets.currentWidget().back())
        self.toolbar.addAction(self.bouton_retour)

        self.bouton_avancer = QAction(QIcon("forward_dark.png"), "Avancer", self)
        self.bouton_avancer.triggered.connect(lambda: self.onglets.currentWidget().forward())
        self.toolbar.addAction(self.bouton_avancer)

        self.bouton_actualiser = QAction(QIcon("refresh_dark.png"), "Actualiser", self)
        self.bouton_actualiser.triggered.connect(lambda: self.onglets.currentWidget().reload())
        self.toolbar.addAction(self.bouton_actualiser)

        self.historique = []

        profile = QWebEngineProfile.defaultProfile()
        profile.clearHttpCache()

        self.ajouter_onglet(url="https://www.google.com/")

        # Menu "Plus"
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        menu_plus = QMenu("Plus", self)
        menu_bar.addMenu(menu_plus)

        # Ajout des actions au menu "Plus"
        action_a_propos = QAction("À propos", self)
        action_a_propos.triggered.connect(self.afficher_a_propos)
        menu_plus.addAction(action_a_propos)

        action_historique = QAction("Historique", self)
        action_historique.triggered.connect(self.afficher_historique)
        menu_plus.addAction(action_historique)

        action_parametres = QAction("Paramètres", self)
        action_parametres.triggered.connect(self.afficher_parametres)
        menu_plus.addAction(action_parametres)

    def afficher_a_propos(self):
        fenetre = FenetreAPropos()
        fenetre.exec_()

    def afficher_historique(self):
        fenetre_historique = FenetreHistorique(self.historique, self.naviguer_vers_url)
        fenetre_historique.exec_()

    def afficher_parametres(self):
        fenetre_parametres = FenetreParametres(self.activer_mode_sombre, self.changer_mode_sombre)
        fenetre_parametres.exec_()

    def changer_mode_sombre(self, etat):
        self.activer_mode_sombre = etat == Qt.Checked
        if self.activer_mode_sombre:
            self.activer_style_sombre()
            self.charger_icones_mode_sombre()
        else:
            self.desactiver_style_sombre()
            self.charger_icones_mode_clair()

    def activer_style_sombre(self):
        style_sombre = """
            QMainWindow {
                background-color: #2e2e2e;
                color: white;
            }
            QTabWidget::pane {
                background: #2e2e2e;
            }
            QTabBar::tab {
                background: #3e3e3e;
                color: white;
            }
            QTabBar::tab:selected {
                background: #5e5e5e;
            }
            QToolBar {
                background: #3e3e3e;
            }
            QLineEdit {
                background: #1e1e1e;
                color: white;
            }
            QListWidget {
                background: #2e2e2e;
                color: white;
            }
        """
        self.setStyleSheet(style_sombre)

    def desactiver_style_sombre(self):
        self.setStyleSheet("")

    def charger_icones_mode_sombre(self):
        self.bouton_retour.setIcon(QIcon("back_light.png"))
        self.bouton_avancer.setIcon(QIcon("forward_light.png"))
        self.bouton_actualiser.setIcon(QIcon("refresh_light.png"))

    def charger_icones_mode_clair(self):
        self.bouton_retour.setIcon(QIcon("back_dark.png"))
        self.bouton_avancer.setIcon(QIcon("forward_dark.png"))
        self.bouton_actualiser.setIcon(QIcon("refresh_dark.png"))

    def ajouter_onglet(self, url=None, titre="Nouvel Onglet"):
        if url is None:
            url = "https://google.com/"

        navigateur = QWebEngineView()
        navigateur.setUrl(QUrl.fromUserInput(str(url)))
        navigateur.urlChanged.connect(self.mettre_a_jour_url_bar)
        navigateur.titleChanged.connect(lambda titre, navigateur=navigateur: self.mettre_a_jour_titre_onglet(navigateur))

        navigateur.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
        navigateur.settings().setAttribute(QWebEngineSettings.PluginsEnabled, False)
        navigateur.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)

        index = self.onglets.addTab(navigateur, titre)
        self.onglets.setCurrentIndex(index)

        # Ajout de l'URL à l'historique
        self.historique.append(url)

    def naviguer_vers_url(self):
        url = self.url_bar.text()
        if "." not in url:
            url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
        self.onglets.currentWidget().setUrl(QUrl.fromUserInput(url))

        # Ajout de l'URL à l'historique
        self.historique.append(url)

    def mettre_a_jour_url_bar(self, url):
        self.url_bar.setText(url.toString())

    def mettre_a_jour_titre_onglet(self, navigateur):
        index = self.onglets.indexOf(navigateur)
        if index != -1:
            self.onglets.setTabText(index, navigateur.title())

    def fermer_onglet(self, index):
        widget = self.onglets.widget(index)
        self.onglets.removeTab(index)
        widget.deleteLater()

    def changement_onglet(self, index):
        navigateur = self.onglets.widget(index)
        if navigateur:
            self.url_bar.setText(navigateur.url().toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = NavigateurAvecOnglets()
    fenetre.show()
    sys.exit(app.exec_())
