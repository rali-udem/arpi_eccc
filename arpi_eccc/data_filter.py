import json
import sys

TEMP_WHITELIST = ['High', 'high', 'Low', 'low', 'minus', 'Minus', 'Temperature', 'Temperatures', 'temperature',
                  'temperatures']
TEMP_BLACKLIST = ['Wind', 'wind', 'Winds', 'winds', 'UV', 'uv']


def get_sentence_temperature(bulletin: dict, period: str):
    kept_tokens = []
    for all_tokens in bulletin['en']['tok'][period]:
        keep_sentence = False
        for word in all_tokens:
            if word in TEMP_BLACKLIST:
                keep_sentence = False
                break
            else:
                if word in TEMP_WHITELIST:
                    keep_sentence = True
        if keep_sentence:
            kept_tokens.extend(all_tokens)
    return kept_tokens


def filter_fields(bulletin: dict, fields_to_keep: set):
    bulletin_fields = set(bulletin.keys())
    bulletin_fields.difference_update(fields_to_keep)
    for cur_field in bulletin_fields:
        del bulletin[cur_field]


def main():
    if len(sys.argv) != 4:
        print("Usage: prog input.jsonl output.jsonl field1,field2,...", file=sys.stderr)
        print("Filters input JSONL by field. Only temp supported as of now.", file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    fields = sys.argv[3].split(',')

    assert fields == ['temp'], "Only temp field supported as of now."
    fields.extend(['id', 'en', 'fr', 'names-en', 'names-fr'])

    all_fields = set(fields)

    with open(input_filename, 'rt', encoding='utf-8') as fin, open(output_filename, 'wt', encoding='utf-8') as fout:
        for line in fin:
            bulletin = json.loads(line)
            filter_fields(bulletin, all_fields)

            for lang in ['en', 'fr']:
                for period in bulletin['en']['tok'].keys():
                    bulletin[lang]['tok'][period] = get_sentence_temperature(bulletin, period)

            json.dump(bulletin, fout, ensure_ascii=False)
            fout.write('\n')


if __name__ == '__main__':
    main()
