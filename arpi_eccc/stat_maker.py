"""
A program to make statistics about the bulletins.
"""
import json
import sys


def analyze_list(stat_info: dict, cur_list: list):
    for data_point in cur_list:
        for variable_index, variable_value in enumerate(data_point):
            stat_info[variable_index] = stat_info.get(variable_index, {})
            if type(variable_value) == list:
                original_value = variable_value
                variable_value = 'sublist'  # temporary
                stat_info[variable_index]['sublist_values'] = stat_info[variable_index].get('sublist_values', {})
                analyze_list(stat_info[variable_index]['sublist_values'], [original_value])

            stat_info[variable_index][variable_value] = stat_info[variable_index].get(variable_value, 0) + 1  # freqs

    return len(cur_list)


def analyze_fields(stat_info: dict, json_dict):
    for k, v in json_dict.items():
        if k not in stat_info:
            stat_info[k] = {'nb_bulletins_with_field': 0}
        stat_info[k]['nb_bulletins_with_field'] += 1

        if v:
            if type(v) == dict and k != 'en' and k != 'fr':  # skip stats on text, they are not needed here
                stat_info[k]['descendants'] = stat_info[k].get('descendants', {})
                analyze_fields(stat_info[k]['descendants'], v)
            elif type(v) == list and type(v[0]) == list:
                if k == 'prob':  # this field is a bit tricky
                    assert v[0][0] == 'seuil' and v[0][1] == 0.2, "Invalid prob field, first 2 toks should be seuil 0.2"
                    v = v[0][2:]  # modify v so that stats can be gathered, removing first 2 tokens that are useless

                stat_info[k]['list_statistics'] = stat_info[k].get('list_statistics', {})
                stat_info[k]['nb_data_points'] = stat_info[k].get('nb_data_points', 0)
                nb_data_points = analyze_list(stat_info[k]['list_statistics'], v)
                stat_info[k]['nb_data_points'] += nb_data_points


def analyze(bulletin: dict, analysis: dict):
    analysis['nb_bulletins'] += 1
    analyze_fields(analysis['fields'], bulletin)


def main():
    if len(sys.argv) != 2:
        print("Usage: prog input.jsonl (or - for stdin)", file=sys.stderr)
        print("Prints JSON stats on stdout", file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]
    analysis = {"fields": {}, "nb_bulletins": 0}
    with open(input_filename, 'rt', encoding='utf-8') if input_filename != '-' else sys.stdin as fin:
        for line in fin:
            analyze(json.loads(line), analysis)

    print(json.dumps(analysis, sort_keys=False), file=sys.stdout)


if __name__ == '__main__':
    main()
