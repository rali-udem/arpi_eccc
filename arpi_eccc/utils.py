import pprint


def get_nb_tokens(bulletin: dict, lang: str) -> int:
    result = 0
    tok_dict = bulletin[lang]['tok']
    for k, sents in tok_dict.items():
        result += sum([len(cur_sent) for cur_sent in sents])
    return result


def pretty_print_bulletin(bulletin: dict, stm):
    print('=' * 120, file=stm)
    print(f"{bulletin['id']} : {' '.join([str(x) for x in bulletin['header']])}", file=stm)
    print('=' * 120, file=stm)

    for lang in ['en', 'fr']:
        print(lang + ' ' + ('-' * 117), file=stm)
        for period_name, sentences in bulletin[lang]['tok'].items():
            print(period_name + ': ' + ' | '.join([' '.join(x) for x in sentences]), file=stm)
        print('-' * 120, file=stm)

    for field_name in ['accum', 'avert', 'ciel', 'climat_temp', 'indice_uv', 'pcpn', 'prob', 'rosee', 'temp', 'vents', 'visib']:
        if field_name in bulletin:
            print(field_name, file=stm)
            print('-' * 120, file=stm)
            pprint.pprint(bulletin[field_name], stream=stm)
            print('-' * 120, file=stm)


def dummy_nlg_english(bulletin: dict) -> dict:
    return {}