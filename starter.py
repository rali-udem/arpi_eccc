import json
import sys

from arpi_eccc.nlg_evaluation import bleu_evaluation
from arpi_eccc.pp_json import pp_json
from arpi_eccc.utils import get_nb_tokens, pretty_print_bulletin, dummy_nlg_english, get_time_interval_for_period


def main():
    """A quick demo to show how to start this project."""
    if len(sys.argv) != 2:
        print("Usage: prog input.jsonl", file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]

    # =============================================================================================
    # read the bulletins and count words
    print(f"Reading all bulletins in {input_filename}", flush=True)

    nb_bulletins = 0
    nb_toks_english = 0
    nb_toks_french = 0
    with open(input_filename, 'rt', encoding='utf-8') as fin:
        for cur_line in fin:
            bulletin = json.loads(cur_line)
            nb_bulletins += 1
            nb_toks_english += get_nb_tokens(bulletin, 'en')
            nb_toks_french += get_nb_tokens(bulletin, 'fr')

    print(f"Read {nb_bulletins} bulletins. {nb_toks_english} English tokens, {nb_toks_french} French tokens.")
    print("\n\n")

    # =============================================================================================
    # show a sample bulletin
    print("A sample bulletin:")
    with open(input_filename, 'rt', encoding='utf-8') as fin:
        cur_line = next(fin)
        sample_bulletin = json.loads(cur_line)
        # pretty_print_bulletin(sample_bulletin, sys.stdout)  # for a non-JSON output
        pp_json(sys.stdout, sample_bulletin, sortkeys=False)

    print('\n\n')

    # =============================================================================================
    # demonstrate what periods correspond to which time intervals in the data
    bulletin_periods = sample_bulletin['en']['tok'].keys()
    print(f"The sample bulletin has the following periods: {bulletin_periods}")
    print(f"These periods correspond to the following time intervals in this bulletin's weather data:")
    for period in bulletin_periods:
        time_interval = get_time_interval_for_period(bulletin, period)
        print(f"Period '{period}' corresponds to time interval [{time_interval[0]}, {time_interval[1]}] (in hours)")

    print('\n\n')

    # =============================================================================================
    # try and evaluate a sample (dummy) generation system for English
    print("Running a dummy natural language generation system on first 1000 bulletins...")
    # first we read a few thousand bulletins...
    bulletins = []
    with open(input_filename, 'rt', encoding='utf-8') as fin:
        for cur_line in fin:
            bulletin = json.loads(cur_line)
            bulletins.append(bulletin)
            if len(bulletins) >= 1000:
                break

    # ...then we run a dummy NLG (natural language generation) system on those bulletins for English...
    print("Evaluating...")
    nlg_results = []  # our NLG results, for English
    reference = []  # the reference, for English
    for bulletin in bulletins:
        nlg_result = dummy_nlg_english(bulletin)  # the nlg_result is a dict with structure identical to bulletin['en']['tok']
        nlg_results.append(nlg_result)
        reference.append(bulletin['en']['tok'])

    # ...now we can evaluate the NLG system using the two lists created above.
    evaluation = bleu_evaluation(nlg_results, reference)
    print(f"Dummy system performance:")
    for period in ['today', 'tonight', 'tomorrow', 'tomorrow_night']:
        print(f"For bulletin period {period}, BLEU score is {evaluation[period]:.3f} on a scale from 0 to 1")
    print()
    print(f"Global score is {evaluation['global']:.3f}")


if __name__ == '__main__':
    main()
