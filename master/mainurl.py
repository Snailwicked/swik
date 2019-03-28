from utils.spiderutils.xpathtexts import xPathTexts
from utils.baseutils.headers import headers
from urllib.parse import urljoin


class mainUrl(xPathTexts):
    def __init__(self):
        super(mainUrl, self).__init__()


    def getUrls(self,url,html,X_path):
        data = set()
        for item in self.get_contents(html=html,X_path=X_path):
            url = urljoin(url, item)
            if "http" in url:
                data.add(url)
        return list(data)

if __name__ == "__main__":
    url = "http://finance.ifeng.com/"
    X_path = "//a//@href"
    import requests
    html = requests.get(url).text
    mainurl = mainUrl()
    for url in mainurl.getUrls(url,html ,X_path):
        print(url)