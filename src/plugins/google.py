import logging
import re
import requests
import google

"""
TODO: 
    1. Внедрить ограничение по "Only some hosts"
    2. Вынести логику парсинга в отдельные сущности
    3. Разбить плагин на модули и внедрить интерфейсы
"""


class QueryVariator:
    def __init__(self):
        self._fields = [
            'firstname',
            'lastname',
            'birthday'
        ]

        self._info = {}

    def _ask_info(self, field):
        for field in self._fields:
            self.info[field] = input('Type "{field_name}"'.format(field_name=field))


class GoogleSearch:
    def search(self, q, limit=10):
        results = google.search(q, stop=limit)
        current_tick = 0
        prepared_results = []
        for uri in results:
            prepared_results.append(self._mining_data(uri=uri))
            current_tick += 1
            if current_tick == limit:
                break
        logging.debug('Search results processing is ready')
        return prepared_results

    def _mining_data(self, uri):
        text = requests.get(uri).text

        return {
            "title": self.get_page_title(text),
            "uri": uri,
            "meta": self.get_page_meta(text)
        }

    @staticmethod
    def get_page_title(text):
        title_re = re.compile('<title>.*?</title>')

        titles = title_re.findall(text)
        if len(titles) > 0:
            return titles[0]\
                .replace('<title>', '')\
                .replace('</title>', '')
        return None

    @staticmethod
    def get_page_meta(text):
        meta_re = re.compile(
            '<meta.*?>'
        )
        found_meta = meta_re.findall(text)
        processed_found_meta = {}
        if len(found_meta) > 0:
            for raw_meta in found_meta:
                try:
                    name = re.findall('name=".*?"', raw_meta)[0].replace('name="', '')[:-1]
                    content = re.findall('content=".*?"', raw_meta)[0].replace('content="', '')[:-1]
                    processed_found_meta[name] = content
                except Exception:
                    continue
            return processed_found_meta
        return None


if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.DEBUG)
    q = os.sys.argv[1]
    try:
        limit = int(os.sys.argv[2])
    except IndexError:
        limit = 10

    gs = GoogleSearch()
    for row in gs.search(q, limit):
        print("@"*50)
        print("@"*50)
        print(row)
