import warnings
with warnings.catch_warnings():
    # It is difficult to install python-Levenshtein. fuzzywuzzy is slower without it and throws a warning
    # python-Levenshtein installation was unsuccessful in the dev environment
    warnings.simplefilter('ignore')
    from fuzzywuzzy import fuzz, process


class Fuzzy:

    @staticmethod
    def match_best_then_shortest(input_string, possible_matches, scorer=fuzz.UWRatio, user_data=False):
        hits = sorted(process.extract(input_string, possible_matches, scorer=scorer, limit=10),
                      key=lambda x: (x[1] * -1, len(x[0])))
        # results from process.extract come back as the matched string and the score
        # Scores are multiplied by -1 to order highest to lowest

        if not user_data:
            return hits[0], [match_tuple for match_tuple in hits[1:] if match_tuple[1] == hits[0][1]]
        else:
            return hits[0], [match_tuple for match_tuple in hits[1:] if match_tuple[1]]
