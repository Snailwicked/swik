import requests
from lxml import etree
cookies = {'tgc': 'TGT-NjUwNjEyODg5Ng==-1583907716-gz-D0994C8D1C18B524BD402E6C227EDE8E-1', 'SUB': '_2A25zbPMuDeRhGeBL61QQ8ibEwjqIHXVQGGPmrDV_PUNbm9AfLUjSkW9NR0wDx0iXKgLvgyohS0onfJ9wKcwvVncT', 'ALC': 'ac%3D2%26bt%3D1583907717%26cv%3D5.0%26et%3D1615443717%26ic%3D-1267822545%26login_time%3D1583907715%26scf%3D%26uid%3D6506128896%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D883278dd60296d6bbecbdd92581a438a', 'SCF': 'AnGJUCfT8ULMc41y6y7TURtwcJH2a3ETu26hUcrJhVWFMhFSVbsn_Ug2W33BoG-8DY5qZ9MeOsaBU2Mj_ovrVSo.', 'LT': '1583907717', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5oh1C84Ps40UIv7gEFX-Aw5NHD95QcSK5ceKzR1h.cWs4DqcjTqJpf9PSk1KepSh2t', 'sso_info': 'v02m6alo5qztaKbh5WlnLW8uYyzhLSMkpm1mpaQvY2jlLCNo4SyjoOguY2gwMA=', 'login': '866e230c83d469a8ac6b9ebaf4f0b3f2', 'ALF': '1615443717'}


headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Sec-Fetch-Dest': 'document',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Referer': 'https://s.weibo.com/weibo/%25E5%258D%259A%25E5%25BD%25A9?topnav=1&wvr=6&b=1&page=3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


def get_info_list(page):
    for page in range(1,page+1):
        params = (
            ('topnav', '1'),
            ('wvr', '6'),
            ('b', '1'),
            ('page', '{}'.format(page)),
        )
        print(params)

        response = requests.get('https://s.weibo.com/weibo/%25E5%258D%259A%25E5%25BD%25A9', headers=headers, params=params, cookies=cookies)
        html = etree.HTML(response.text)
        print(response.text)
        for item in html.xpath("//div[@class='content']"):
            print(etree.tostring(item))

if __name__ == '__main__':
    get_info_list(1)