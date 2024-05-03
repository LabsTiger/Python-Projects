'''
REMEMBER: THE CODE MAY NOT BE CORRECT IN SOME PARTS(LIKE THE AD DOMAINS LIST) SINCE SOME PARTS
MAY BE OUTDATED OR MAY NOT EVEN EXIST. THANK YOU FOR YOUR UNDERSTANDING. -TIGERLABS
'''
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class AdBlocker(QWebEngineUrlRequestInterceptor):
    def __init__(self):
        super().__init__()

    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if self.is_ad(url):
            info.block(True)

    def is_ad(self, url):
        ad_domains = [
    "ad.doubleclick.net",
    "googlesyndication.com",
    "adservice.google.com",
    "advertising.com",
    "adnxs.com",
    "openx.net",
    "rubiconproject.com",
    "pubmatic.com",
    "criteo.com",
    "taboola.com",
    "outbrain.com",
    "revcontent.com",
    "taboola.com",
    "bidvertiser.com",
    "adblade.com",
    "adroll.com",
    "indexexchange.com",
    "contextweb.com",
    "sharethrough.com",
    "adform.com",
    "conversantmedia.com",
    "sovrn.com",
    "emxdgt.com",
    "spotx.tv",
    "districtm.io",
    "advertising.amazon.com",
    "advertising.microsoft.com",
    "ads.twitter.com",
    "business.linkedin.com",
    "advertising.yahoo.com",
    "advertising.aol.com",
    "advertising.apple.com",
    "advertising.ebay.com",
    "advertising.ibm.com",
    "advertising.salesforce.com",
    "advertising.oracle.com",
    "advertising.sap.com",
    "advertising.adobe.com",
    "advertising.paypal.com",
    "advertising.dropbox.com",
    "advertising.spotify.com",
    "advertising.netflix.com",
    "advertising.uber.com",
    "advertising.airbnb.com",
    "advertising.tesla.com",
    "advertising.etsy.com",
    "advertising.zillow.com",
    "advertising.netflix.com",
    "advertising.snapchat.com",
    "advertising.pinterest.com",
    "advertising.tiktok.com",
    "advertising.github.com",
    "advertising.reddit.com",
    "advertising.quora.com",
    "advertising.stackoverflow.com",
    "advertising.yelp.com",
    "advertising.tripadvisor.com",
    "advertising.hulu.com",
    "advertising.fox.com",
    "advertising.disney.com",
    "advertising.cnn.com",
    "advertising.bbc.com",
    "advertising.nbc.com",
    "advertising.cbs.com",
    "advertising.abc.com",
    "advertising.forbes.com",
    "advertising.nytimes.com",
    "advertising.wsj.com",
    "advertising.theguardian.com",
    "advertising.bloomberg.com",
    "advertising.reuters.com",
    "advertising.apnews.com",
    "advertising.buzzfeed.com",
    "advertising.huffpost.com",
    "advertising.cnbc.com",
    "advertising.buzzfeed.com",
    "advertising.buzzfeednews.com",
    "advertising.buzzfeedtasty.com",
    "advertising.buzzfeedunsolved.com",
    "advertising.npr.org",
    "advertising.bbc.co.uk",
    "advertising.thetimes.co.uk",
    "advertising.telegraph.co.uk",
    "advertising.independent.co.uk",
    "advertising.guardian.co.uk",
    "advertising.dailymail.co.uk",
    "advertising.metro.co.uk",
    "advertising.mirror.co.uk",
    "advertising.thesun.co.uk"
]


        for domain in ad_domains:
            if domain in url:
                return True
        return False


class DownloadManager(QObject):
    def __init__(self):
        super().__init__()
        self.browser = None

    def setBrowser(self, browser):
        self.browser = browser

    def downloadRequested(self, item: QWebEngineDownloadItem):
        save_path, _ = QFileDialog.getSaveFileName(self.browser, "Save File", "", "All Files (*)")
        if save_path:
            item.setPath(save_path)
            item.accept()

        item.finished.connect(lambda: print("Download finished:", item.path()))


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ad_blocker = AdBlocker()
        self.browser = QWebEngineView()
        self.browser.page().profile().setRequestInterceptor(self.ad_blocker)

        self.download_manager = DownloadManager()
        self.download_manager.setBrowser(self.browser)
        self.browser.page().profile().downloadRequested.connect(self.download_manager.downloadRequested)

        self.browser.setUrl(QUrl("http://google.com"))
        self.setCentralWidget(self.browser)

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.setStatusTip("Forward to next page")
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.addSeparator()

        search_bar = QLineEdit()
        search_bar.returnPressed.connect(self.search)
        navbar.addWidget(search_bar)

        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.showMaximized()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def search(self):
        search_term = self.url_bar.text()
        url = "https://www.google.com/search?q={}".format(search_term)
        self.browser.setUrl(QUrl(url))


app = QApplication(sys.argv)
QApplication.setApplicationName("PyBrowse")
window = Browser()
app.exec_()
