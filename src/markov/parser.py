from pydtmc import MarkovChain


def parse_markov_payload(payload: dict):

    for key in payload:
        if "_to_" in key:
            pass