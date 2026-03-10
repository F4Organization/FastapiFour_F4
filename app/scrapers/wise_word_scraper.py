import requests
from bs4 import BeautifulSoup as bs

url = "https://saramro.com/quotes"

cookies = {
    'PHPSESSID': 'obq66q5khlqo4keav43jto58r5',
    'e1192aefb64683cc97abb83c71057733': 'cXVvdGVz',
    '2a0d2363701f23f8a75028924a3af643': 'MTIxLjE1Ny4xMTUuNTQ%3D',
    '__gads': 'ID=f1eafbf4968618d4:T=1773129457:RT=1773129457:S=ALNI_MbsSslws46VIcASWS3KZif8FWZdAQ',
    '__gpi': 'UID=00001348823fafaf:T=1773129457:RT=1773129457:S=ALNI_MYyLMUyYKSUu9QWtDG5u-SRWzWpqg',
    '__eoi': 'ID=475480a570f89063:T=1773129457:RT=1773129457:S=AA-AfjbwvrT_rhWjPddKR4C0mx5D',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

res = requests.get(url=url, headers=headers, cookies=cookies)
res.raise_for_status()

# 첫번째 table 태그의 tr 태그 내용을 전부 가져옴(table2, 리스트 상태)
# 필요한 부분만 슬라이싱(table3)
html = bs(res.content, 'lxml')
table1 = html.find('table')
table2 = table1.find_all('tr')
table3 = table2[2::2]

# 명언과 저자를 분리. 만일 저자가 없을 시 무시하도록 처리
for td in table3:
    td_list = list(td.stripped_strings)
    if len(td_list) < 2:
        continue
    wise_word = td_list[0]
    author = td_list[1]
    print(wise_word)
    print(author)
    print("-"*20)