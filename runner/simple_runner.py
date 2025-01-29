from collections import deque
import json
import requests
from utils.utils import Item


class SimpleRunner:

    def __init__(self, parser, sink, logger, seed_urls, session, max_tries=5):
        self._parser = parser
        self._sink = sink
        self._logger = logger
        self._seed_urls = seed_urls
        self._max_tries = max_tries
        self._seen = set()
        self._to_process = deque()
        self._to_process.extend(Item(url) for url in seed_urls)
        self._seen.update(seed_urls)
        self._session = session


    def _filter(self, urls):
        to_return = (url for url in urls if url not in self._seen)
        return to_return


    async def _process(self, item):
        async with self._session.request(method='get', url=item.url, ssl=False) as resp:
            resp.raise_for_status()
            content = await resp.content.read()
            result, next_urls = self._parser.parse(content, item.url)
            return result, next_urls


    async def _write(self, item, result, error):
        self._logger.info(f'Writing for {item.url}, error={error}')

        data = {'error': str(error), 'result': result, 'url': item.url}
        data_json = json.dumps(data, ensure_ascii=False) + '\n'
        await self._sink.write(data_json)


    async def run(self):
        while self._to_process:
            item = self._to_process.popleft()
            result = None
            next_urls = []
            try:
                result, next_urls = await self._process(item)
            except Exception as e:
                self._logger.exception('Failed to process: ')
                item.tries += 1
                if item.tries > self._max_tries:
                    await self._write(item, result, e)
                else:
                    self._to_process.append(item)
            if result:
                await self._write(item, result, None)

            for elem in self._filter(next_urls):
                self._to_process.append(Item(elem))
                self._seen.add(elem)
