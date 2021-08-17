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
            print(period_name + ': ' + '     '.join([' '.join(x) for x in sentences]), file=stm)
        print('-' * 120, file=stm)

    for field_name in ['accum', 'avert', 'ciel', 'climat_temp', 'indice_uv', 'pcpn', 'prob', 'rosee', 'temp', 'vents', 'visib']:
        if field_name in bulletin:
            print(field_name, file=stm)
            print('-' * 120, file=stm)
            pprint.pprint(bulletin[field_name], stream=stm)
            print('-' * 120, file=stm)


def dummy_nlg_english(bulletin: dict) -> dict:
    """
    A NLG system should return a dict with the same structure as that in the field bulletin['en' or 'fr']['tok'], i.e.
    the same periods (e.g. today) with the corresponding text, as list of sentences. Each sentence is a list of strings.

    :param bulletin: The input bulleting.
    :return: The NLG dict, for English here.
    """

    # we need to have the same periods as in the input
    result = bulletin['en']['tok']
    #result = {period_name: [] for period_name in bulletin['en']['tok'].keys()}

    # we provide dummy results
    for period_name, sentence_list in result.items():
        sentence_list.append(['Mainly', 'cloudy', '.'])  # first sentence for this period
        sentence_list.append(['Wind', 'up', 'to', '15', 'km/h', '.'])  # second sentence for this period

    return result
