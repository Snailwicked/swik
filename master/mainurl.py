from utils.spiderutils.xpathtexts import xPathTexts
from utils.baseutils.headers import headers
from urllib.parse import urljoin


class mainUrl(xPathTexts):
    def __init__(self):
        super(mainUrl, self).__init__()


    def getUrls(self,url,X_path,headers):
        data = set()
        for item in self.get_contents(url,X_path,headers):
            url = urljoin(url, item)
            if "http" in url:
                data.add(url)
        return list(data)

if __name__ == "__main__":
    url = "http://finance.ifeng.com/"
    X_path = "//a//@href"
    mainurl = mainUrl()
    for url in mainurl.getUrls(url,X_path,headers):
        print(url)