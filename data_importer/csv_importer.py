# -*- coding: utf-8 -*-
from datetime import datetime
import re
import os


class CSVImporter:
    csv_dir = 'data'
    future_re = re.compile(r'.\d{4}.csv\Z')
    option_re = re.compile(r'.\d{4}-.-\d+.csv\Z')

    @staticmethod
    def import_data(base_dir=None):
        if not base_dir:
            base_dir = CSVImporter.csv_dir
        for filename in os.listdir(base_dir):
            if CSVImporter.future_re.match(filename):
                with open(os.path.join(base_dir, filename)) as f:
                    rows = f.readlines()
                    start_time = datetime.strptime(rows[1].split(',')[0], "%Y/%m/%d %H:%M")
                    for row in rows[1:-3]:
                        pass

            elif CSVImporter.option_re.match(filename):
                print('option '+filename)
            else:
                print('error')

