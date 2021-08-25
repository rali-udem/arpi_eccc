"""
Not the fastest of codes, but builds tensors for meteocode data, considerably simplifying the information.
"""
import json

import numpy as np
import sys

from arpi_eccc.simple_onehot_encoder import SimpleOneHotEncoder
from arpi_eccc.utils import get_time_interval_for_period

# encoder for element 2 for field 'temp'
temp_2_encoder = SimpleOneHotEncoder(['pi', 'min', 'max', 'stationnaire', 'hausse', 'baisse'],
                                     handle_unknown='error')  # or 'ignore' if we want to ignore unknown labels


def meteocode_tensor_for_field(bulletin: dict, for_hour: int, field_name: str, data_point: list) -> list:
    assert field_name == 'temp', "Only temp implemented for now"

    result = None

    if field_name == 'temp':  # 1-dimensional np tensor of size 7
        field_2 = temp_2_encoder.encode(data_point[2])
        result = np.concatenate([field_2, [data_point[3]]])  # we ignore fields 4 and next

    return result


def meteocode_tensors(bulletin: dict, start_hour: int, end_hour: int, field_list: list) -> dict:
    """
    Returns a dict mapping an hour in the range [start_hour, end_hour] to a tensor representing the meteocode
    info a this hour.

    :param bulletin:
    :param start_hour:
    :param end_hour:
    :param field_list: The list of fields read to create the tensor.
    :return: A dict.
    """
    assert end_hour > start_hour, "Invalid time interval"

    result = {}

    for field_name in field_list:
        hour_to_datapoints_map = {}  # for this field only
        for data_point in bulletin[field_name]:
            data_point_start, data_point_end = data_point[0:2]

            for h in range(data_point_start, data_point_end):
                assert h not in hour_to_datapoints_map, "Duplicate value in hour map"
                hour_to_datapoints_map[h] = data_point

        for cur_hour in range(start_hour, end_hour + 1):  # includes last hour
            if cur_hour not in result:
                result[cur_hour] = []

            result[cur_hour].append(meteocode_tensor_for_field(bulletin, cur_hour, field_name,
                                                               hour_to_datapoints_map[cur_hour]))

    # finally, when we are done for each hour, we concatenate the field tensors for each hour
    result[cur_hour] = np.concatenate(result[cur_hour])

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
