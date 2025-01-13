import csv
import datetime as dt
from collections import defaultdict

from scrapy.exceptions import DropItem

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT, RESULTS_DIR


class PepParsePipeline:
    def open_spider(self, spider):
        self.pep_status_counts = defaultdict(int)

    def process_item(self, item, spider):
        pep_status = item.get('status')
        if pep_status is None:
            raise DropItem(f'Неизвестный статус pep - {item}')
        self.pep_status_counts[pep_status] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / RESULTS_DIR
        results_dir.mkdir(exist_ok=True)

        results = [('Статус', 'Количество')]
        status_count_pairs = list(self.pep_status_counts.items())
        results.extend(status_count_pairs)
        results.append(('Total', sum(self.pep_status_counts.values())))
        now_format_time = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_format_time}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(results)
