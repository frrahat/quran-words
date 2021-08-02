import json
import os
import sys
from copy import deepcopy

if __name__ == '__main__':
    parent_dir_path = os.path.abspath(os.path.dirname(__file__))

    input_file_path = os.path.join(parent_dir_path, 'input.json')
    # output_file_path = os.path.join(parent_dir_path, '_output.json')

    sys.path.insert(1, '/'.join(__file__.split('/')[:-3]))

    from server.db_quran_arabic import db_quran_arabic, QuranArabic

    data = json.load(open(input_file_path, encoding='utf8'))
    data_new = deepcopy(data)

    t = 0

    for index, item in enumerate(data_new):
        query = db_quran_arabic.session.query(QuranArabic).filter(
            QuranArabic.text.like(f'%{item["arabic"]}%'))
        c = query.count()
        if c == 0:
            print('+++', index, item['arabic'],
                  item['level_num'], item['serial_num'])
            t += 1
        item['match_count'] = c

    # format input.json
    json.dump(data_new, open(input_file_path, 'w', encoding='utf8'),
              ensure_ascii=False, indent=4)

    print('total mismatching words == ', t)
