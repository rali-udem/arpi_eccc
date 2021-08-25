import json

import numpy as np
import sklearn.preprocessing
import sys

from sklearn.preprocessing import OneHotEncoder

from arpi_eccc.utils import get_time_interval_for_period

# encoder for element 2 for field 'temp'
temp_2_encoder = OneHotEncoder(categories=['pi', 'min', 'max', 'stationnaire', 'hausse', 'baisse'],
                               handle_unknown='error')  # or 'ignore' if we want to ignore unknown labels


def meteocode_tensor_for_field(bulletin: dict, for_hour: int, field_name: str, data_point: list) -> list:
    assert field_name == 'temp', "Only temp implemented for now"

    result = []

    if field_name == 'temp':
        field_2 = temp_2_encoder.transform([data_point[2]])
        # fields 3 and 4 are mere integers
        # fields 5 -> are ignored

    return result


def meteocode_tensors(bulletin: dict, start_hour: int, end_hour: int, field_list: list):
    assert end_hour > start_hour, "Invalid time interval"

    result = {}

    for field_name in field_list:
        hour_to_datapoints_map = {}  # for this field only
        for data_point in bulletin[field_name]:
            data_point_start, data_point_end = data_point[0:2]
            if start_hour < data_point_end and data_point_start < end_hour < data_point_end:  # overlap
                for h in range(data_point_start, data_point_end):
                    assert h not in hour_to_datapoints_map, "Duplicate value in hour map"
                    hour_to_datapoints_map[h] = data_point

        for cur_hour in range(start_hour, end_hour + 1):  # includes last hour
            if cur_hour not in result:
                result[cur_hour] = []
            result[cur_hour].extend(meteocode_tensor_for_field(bulletin, cur_hour, field_name, hour_to_datapoints_map[cur_hour]))

    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: prog input.jsonl", file=sys.stderr)
        print("Demoes encoding.", file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]
    with open(input_filename, 'rt', encoding='utf-8') if input_filename != '-' else sys.stdin as fin:
        for line in fin:
            bulletin = json.loads(line)
            start_hour, end_hour = get_time_interval_for_period(bulletin, 'today')
            tensors = meteocode_tensors(bulletin, start_hour, end_hour, ['temp'])


if __name__ == '__main__':
    main()