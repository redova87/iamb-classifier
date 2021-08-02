from itertools import product
from pprint import pprint



class IambicLine():

    #TODO: to manage state, create an object {0: unmodified, 1: promote_secondary...}
    #       and increment a counter for every is_valid_IP check, instead of current switches

    BASE_PATTERN = (0,1,0,1,0,1,0,1,0,1)
    WORD_STRESS_PATTERNS = {
        2: ( [0,1], [1,0] ),
        3: {
            (0,0,1): [1,0,1],
            (0,1,0): [0,1,0],
            (1,0,0): [1,0,1]
        },
        4: {
            (0,0,0,1): [0,1,0,1],
            (0,0,1,0): [1,0,1,0],
            (0,1,0,0): [0,1,0,1],
            (1,0,0,0): [1,0,1,0],
            (2,0,1,0): [1,0,1,0]  # TODO TEMPORARY
        },
        5: { #TODO: systematize
            (0,1,0,2,0): [0,1,0,1,0],
            (0,1,0,1,0): [0,1,0,1,0],
            (0,0,0,1,0): [0,1,0,1,0],
            (0,1,0,0,0): [0,1,0,1,0]
        }
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.formatted_list_of_realized_stress_patterns = []
        self.unique_dict_of_realized_stress_patterns = {}
        self.is_valid_pattern = False
        self.valid_pattern = None
        self.current_state = 0

        self.main()


    def get_original_stress_patterns_per_token(self):
        return [(t.stress_patterns, t.token) for t in self.tokens]


    def get_possible_stress_patterns_per_token(self, original_stress_patterns_per_token):
        """
        returns: List[Tuples(Lists)]
        """
        return list(product(*[pair[0] for pair in original_stress_patterns_per_token]))


    def create_formatted_list_of_realized_stress_patterns(self, stress_patterns_per_token):
        """
        accepts: List[Tuples(Lists)]
        produces: 
            -adds on to self.formatted_list_of_realized_stress_patterns -- List[Dictionaries]
            -adds unique values to unique_dict_of_realized_stress_patterns -- Dict{Tuple: List[Tuples(Lists)]}
        """
        formatted_list_of_realized_stress_patterns = []
        for pattern in stress_patterns_per_token:
            f = tuple( syllable for word in pattern for syllable in word)
            line = {
                "formatted": f,
                "original": pattern
            }
            formatted_list_of_realized_stress_patterns.append(line) 
        self.formatted_list_of_realized_stress_patterns.extend(formatted_list_of_realized_stress_patterns)
        self.create_unique_dict_of_realized_stress_patterns()


    def create_unique_dict_of_realized_stress_patterns(self):
        for entry in self.formatted_list_of_realized_stress_patterns:
            if self.unique_dict_of_realized_stress_patterns.get(entry["formatted"]):
                if entry["original"] not in self.unique_dict_of_realized_stress_patterns[entry["formatted"]]:
                    self.unique_dict_of_realized_stress_patterns[entry["formatted"]].append(entry["original"])
            else:
                self.unique_dict_of_realized_stress_patterns[entry["formatted"]] = [entry["original"]]





    def is_valid_IP(self):
        if self.BASE_PATTERN in self.unique_dict_of_realized_stress_patterns:
            return True
        else:
            return self.fit_to_IP()


    def fit_to_IP(self):
        """
        After the initial check:
            1. Promote secondary Stresses
            2. Demote compound stresses
            3. Demote monosyllabic stresses
            4. Promote polysyllabic zero stresses
        """
        phases = {
            1: self.promote_secondary_stresses,
            2: self.demote_compound_stress,
            3: self.demote_monosyllable_stress,
            4: self.promote_polysyllabic_zero_stresses,
            5: self.alter_primary_stresses
        }
        try:
            if phases[self.current_state]():
                return True
            else:
                return False
        except KeyError:
            print("Ran out of transformations")
            return False



    def promote_secondary_stresses(self):
        """
        Works on a List[Tuples(Lists)]
        Creates a new List[Tuples(Lists)]
        """
        new_combinations = [] # List[Tuples(Lists)]
        for line in self.get_baseline_before_alteration():
            reconstituted_line = []
            for w in line:
                reconstituted_line.append([1 if s == 2 and len(w) > 2 else s for s in w])
            new_combinations.append(tuple(reconstituted_line))

        return self.check_validity_and_continue(new_combinations)

    @staticmethod
    def create_demoted_compound_variations(word):
        word_stress_variations = []
        for i,syllable in enumerate(word):
            if syllable == 1:
                word_copy = [*word]
                word_copy[i] = 0
                word_stress_variations.append(word_copy)
                continue
        return word_stress_variations


    def demote_compound_stress(self):
        new_combinations = []
        primary_count = 0
        for line in self.get_baseline_before_alteration():
            for word in line:
                for syllable in word:
                    if syllable == 1:
                        primary_count += 1
                    if primary_count > 1:
                        word_stress_variations = self.create_demoted_compound_variations(word)
                        idx_word_in_line = line.index(word)
                        for word_stress_variation in word_stress_variations:
                            line_copy = [w for w in line]
                            line_copy[idx_word_in_line] = word_stress_variation
                            line_copy = tuple(line_copy)
                            new_combinations.append(line_copy)
                primary_count = 0
            new_combinations.append(line)

        return self.check_validity_and_continue(new_combinations)


    def demote_monosyllable_stress(self):
        """
        Works on a List[Tuples(Lists)]
        Creates a new List[Tuples(Lists)]
        """
        new_combinations = []
        i = 0
        for line in self.get_baseline_before_alteration():
            reconstituted_line = []
            for w in line:
                reconstituted_line.append([0 if s == 1 and len(w) == 1 and i % 2 == 0 else s for s in w])
                i = i + len(w)
            new_combinations.append(tuple(reconstituted_line))
            i = 0

        return self.check_validity_and_continue(new_combinations)


    #helper
    def get_polysyllabic_stress_possibilities(self, word):
        try:
            multi_stressed = self.WORD_STRESS_PATTERNS[len(word)][tuple(word)]
            return multi_stressed
        except:
            print("*" * 80, "polysyllabic pattern not found:", word)

    def promote_polysyllabic_zero_stresses(self):
        """
        check if the word requires two stresses
        """
        new_combinations = []
        i = 0
        for line in self.get_baseline_before_alteration():
            reconstituted_line = []
            for word in line:
                if len(word) == 3 and i % 2 == 1:
                    pass
                    print("three letter word needs two syllables")
                    # print(word)
                elif len(word) > 3:
                    multi_stressed = self.get_polysyllabic_stress_possibilities(word)
                    reconstituted_line.append(multi_stressed)
                else:
                    reconstituted_line.append(word)
                i = i + len(word)
            new_combinations.append(tuple(reconstituted_line))
            i = 0

        return self.check_validity_and_continue(new_combinations)


    def alter_primary_stresses(self):
        new_combinations = []
        for line in self.get_baseline_before_alteration():
            for i,word in enumerate(line):
                if len(word) > 1:
                    for variant in self.WORD_STRESS_PATTERNS[len(word)]:
                        line_copy = [*line]
                        line_copy[i] = variant
                        new_combinations.append(tuple(line_copy))

        return self.check_validity_and_continue(new_combinations)


    def get_baseline_before_alteration(self):
        return (l for line in self.unique_dict_of_realized_stress_patterns.values() for l in line)

    def check_validity_and_continue(self, new_combinations):
        self.create_formatted_list_of_realized_stress_patterns(new_combinations)
        self.current_state += 1
        self.is_valid_pattern = self.is_valid_IP()
        return self.is_valid_pattern


    def main(self):
        original_stress_patterns_per_token = self.get_original_stress_patterns_per_token()
        possible_stress_patterns_per_token = self.get_possible_stress_patterns_per_token(original_stress_patterns_per_token)
        self.is_valid_pattrn = self.check_validity_and_continue(possible_stress_patterns_per_token)
        # print(self.is_valid_pattern)
        