import asyncio

import requests
from bs4 import BeautifulSoup as bs
from tortoise import Tortoise

from app.core.database import TORTOISE_ORM
from app.models.wise_word_model import WiseWord


async def scraping_wise_word(start_page: int, final_page: int) -> None:
    try:
        # 세션 연결
        await Tortoise.init(config=TORTOISE_ORM)

        for i in range(start_page, final_page + 1):
            try:
                url = f"https://saramro.com/quotes?page={i}"

                res = requests.get(url=url)
                res.raise_for_status()

                # 첫번째 table 태그의 tr 태그 내용을 전부 가져옴(table2, 리스트 상태)
                # 필요한 부분만 슬라이싱(table3)
                html = bs(res.content, "lxml")
                table1 = html.find("table")
                table2 = table1.find_all("tr")
                table3 = table2[2::2]

                # 명언과 저자를 분리. 만일 저자가 없을 시 무시하도록 처리
                for td in table3:
                    td_list = list(td.stripped_strings)
                    if len(td_list) < 2:
                        continue
                    wise_word = td_list[0]
                    author = td_list[1][2:]
                    await WiseWord.create(content=wise_word, author=author)
                print(f"{i}페이지 저장 완료")
                await asyncio.sleep(2)

            # 한 페이지가 실패하면 다음 페이지부터 재시도
            except requests.RequestException as e:
                print(f"{i}페이지 요청 실패: {e}")
                continue

    finally:
        await Tortoise.close_connections()
        print("커넥션 종료")


asyncio.run(scraping_wise_word(1, 1013))
