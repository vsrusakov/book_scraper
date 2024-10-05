import logging
import time

from runner.simple_runner import SimpleRunner
from parser.css_selector_parser import CssSelectorParser
from utils.utils import FileSink

def main():
    logging.basicConfig(
        format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
        datefmt='%d-%m-%y %H:%M:%S',
        level='INFO',
    )
    logger = logging.getLogger('Runner')
    # главная - https://books.toscrape.com/index.html
    # seed_urls = ['https://books.toscrape.com/catalogue/category/books/default_15/index.html']
    seed_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']
    parser = CssSelectorParser()
    sink = FileSink('./result/result.jsonl')
    runner = SimpleRunner(parser, sink, logger, seed_urls)
    start = time.time()
    runner.run()
    logger.info(f'Total duration is {(time.time() - start):.3f} sec')


if __name__ == '__main__':
    main()