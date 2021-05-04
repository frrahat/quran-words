import json
import os
import sys
from copy import deepcopy

if __name__ == '__main__':
    parent_dir_path = os.path.abspath(os.path.dirname(__file__))

    input_file_path = os.path.join(parent_dir_path, 'input.json')
    output_file_path = os.path.join(parent_dir_path, '_output.json')

    sys.path.insert(1, '/'.join(__file__.split('/')[:-3]))

    from server.db_quran_arabic import db_quran_arabic, QuranArabic

    data = json.load(open(input_file_path, encoding='utf8'))
    data_new = deepcopy(data)

    for item in data_new:
        examples = item['examples']
        populated_examples = []
        for example in examples:
            sura_num, ayah_num = map(int, example.strip().split(':'))
            verse_arabic = db_quran_arabic.session.query(QuranArabic).filter(
                QuranArabic.sura_num == sura_num,
                QuranArabic.ayah_num == ayah_num
            ).first()

            populated_examples.append(verse_arabic.text)

        item['examples_populated'] = populated_examples

    # format input.json
    json.dump(data, open(input_file_path, 'w', encoding='utf8'),
              ensure_ascii=False, indent=4)

    json.dump(data_new, open(output_file_path, 'w', encoding='utf8'),
              ensure_ascii=False, indent=4)
