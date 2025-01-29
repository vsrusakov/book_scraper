import logging
import time
import asyncio, aiofiles
from aiohttp import ClientSession

from runner.simple_runner import SimpleRunner
from parser.css_selector_parser import CssSelectorParser


async def main():
    logging.basicConfig(
        format='[%(asctime)s] - %(name)s - %(levelname)s: %(message)s',
        datefmt='%d-%m-%y %H:%M:%S',
        level=logging.INFO,
    )
    logger = logging.getLogger('Runner')
    # главная - https://books.toscrape.com/index.html
    seed_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']
    parser = CssSelectorParser()
    async with aiofiles.open('./result/result.jsonl', 'w', encoding='utf-8') as sink:
        async with ClientSession() as session:
            runner = SimpleRunner(parser, sink, logger, seed_urls, session)
            start = time.perf_counter()
            await runner.run()
            logger.info(f'Elapsed in {(time.perf_counter() - start):.3f} seconds')


if __name__ == '__main__':
    asyncio.run(main())
