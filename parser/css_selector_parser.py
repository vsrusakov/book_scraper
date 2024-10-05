from bs4 import BeautifulSoup
from urllib.parse import urljoin


class CssSelectorParser:

    def parse_book(self, root):
        result = {}

        title_elem = root.select_one('.product_main h1')
        if title_elem:
            title_text = title_elem.text
            result['title'] = title_text.strip()

        description = root.select_one('meta[description]')
        if description:
            description_text = description.attrs['content']
            result['description'] = description_text.strip()

        price_elem = root.select_one('.product_main p.price_color')
        if price_elem:
            result['price'] = price_elem.text.strip()

        return result

    def parse_next(self, root, base_url):
        links = root.select('.product_pod h3 a')
        to_return = []
        for link in links:
            url = link.attrs['href']
            to_return.append(urljoin(base_url, url))
        next_page = root.select_one('li.next a')
        if next_page:
            url = next_page.attrs['href']
            to_return.append(urljoin(base_url, url))
        return to_return

    def parse(self, content, base_url):
        soup = BeautifulSoup(content, features="html.parser")
        element = soup.select_one('article.product_page')
        if element:
            result = self.parse_book(soup)
            return result, []
        next_links = self.parse_next(soup, base_url)
        return None, next_links