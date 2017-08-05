from bs4 import BeautifulSoup
import requests


class YandexSearch:
    def search(self, q):
        search_response = requests.get('https://yandex.ru/search/?text={q}'.format(q=q))
        bs = BeautifulSoup(search_response.text, 'html.parser')
        results = bs.find_all(class_='serp-item')
        parsed_results = []
        for snippet in results:
            parsed_snippet = self.parse_snippet(snippet, q)
            if parsed_snippet is not None and type(parsed_snippet) == dict:
                parsed_results.append(parsed_snippet)
        return parsed_results

    @staticmethod
    def parse_snippet(snippet, query=None):
        links_class = 'organic__url'
        link = snippet.find(class_=links_class)
        if link is None:
            return None
        uri = link.attrs.get('href')

        description_class = 'text-container'
        description = snippet.find(class_=description_class)
        if description is not None:
            description = description.text
        return {'uri': uri, 'title': link.text, 'description': description, 'query': query}


