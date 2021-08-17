import json
import sys

from arpi_eccc.utils import get_nb_tokens, pretty_print_bulletin


def main():
    """A quick demo"""
    if len(sys.argv) != 2:
        print("Usage: prog input.jsonl", file=sys.stderr)
        sys.exit(1)

    input_filename = sys.argv[1]

    # read the bulletins and count wordss
    print(f"Reading all bulletins in {input_filename}", file=sys.stderr, flush=True)

    nb_bulletins = 0
    nb_toks_english = 0
    nb_toks_french = 0
    with open(input_filename, 'rt', encoding='utf-8') as fin:
        for cur_line in fin:
            bulletin = json.loads(cur_line)
            nb_bulletins += 1
            nb_toks_english += get_nb_tokens(bulletin, 'en')
            nb_toks_french += get_nb_tokens(bulletin, 'fr')

    print(f"Read {nb_bulletins} bulletins. {nb_toks_english} English tokens, {nb_toks_french} French tokens.",
          file=sys.stderr)
    print("\n\n", file=sys.stderr)

    # show a sample bulletin
    with open(input_filename, 'rt', encoding='utf-8') as fin:
        cur_line = next(fin)
        bulletin = json.loads(cur_line)
        pretty_print_bulletin(bulletin, sys.stderr)

    # try and evaluate a sample (dummy) generation system for English







if __name__ == '__main__':
    main()
