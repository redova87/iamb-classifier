import re

class SpellingSyllabifier:
    """
    If a token is not in the dictionary,
    Syllabify a word based only on its spelling
    """

    VOWELS = "aeiouy"
    DUMMY_STRESSED = "AH1"
    DUMMY_UNSTRESSED = "AH0"
    REGEX = {
        "QU": r'qu',
        "ION": r'[st]{1}ions?$',
        "AE": r'ae',
        "DOUBLE": r'([eiouy])\1',  # no double a
        "OU": r'ou',
        "EY": r'ey\W?',
        "IES": r'ies?$',
        "YV": r'y[aeiou]',
        "EA": r'ea',
        "ED": r'[^aeiou]ed$',
    }

    def __init__(self, token):
        self.token = token
        self.syllable_count = 0
        self.modified_word = ''
        self.tentative_phonemes = [[]]

        self.main()

    
    def get_syllable_count(self):
        word = self.check_special_cases()
        syllables = [w for w in word if w in self.VOWELS]
        self.syllable_count = len(syllables)
        print(self.syllable_count)

    def find_multiple(self, regex, word, rev=False):
        res = re.finditer(regex, word)
        indicies = [m.start() + 1 for m in res]
        indicies = indicies[::-1] if rev else indicies
        for idx in indicies:
            word = word[:idx] + word[idx + 1:]
        return word

    def find_single(self, letter, word):
        idx = word.rindex(letter)
        word = word[:idx] + word[idx + 1:]
        return word


    def check_special_cases(self, word=None):
        word = word if word else self.token

        if re.search(self.REGEX["QU"], word):
            word = self.find_multiple(self.REGEX["QU"], word)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["ION"], word)  and len(word) > 4:
            word = self.find_single("i", word)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["AE"], word):
            word = self.find_multiple(self.REGEX["AE"], word, rev=True)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["DOUBLE"], word):
            word = self.find_multiple(self.REGEX["DOUBLE"], word)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["OU"], word):
            word = self.find_multiple(self.REGEX["OU"], word)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["EY"], word):
            word = self.find_multiple(self.REGEX["EY"], word)
            return self.check_special_cases(word)

        elif re.search(r'ies?$', word):
            word = self.find_single("e", word)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["YV"], word):
            word = self.find_multiple(self.REGEX["YV"], word)
            return self.check_special_cases(word)

        elif re.search(self.REGEX["EA"], word):
            word = self.find_multiple(self.REGEX["EA"], word)
            return self.check_special_cases(word)

        elif re.search(r'[^aeiou]ed$', word)  and len(word) >= 4:
            word = self.find_single("e", word)
            return self.check_special_cases(word)


        # print("^^^^^^^^^^^", word)
        self.modified_word = word
        return self.modified_word

    
    def simple_stressor(self):
        count = self.syllable_count
        if count == 1:
            return [[self.DUMMY_STRESSED]]
        else:
            return [[self.DUMMY_STRESSED if i == self.syllable_count - 2 else self.DUMMY_UNSTRESSED for i in range(self.syllable_count) ]]


    #TODO
    def complicated_stressor(self):
        pass


    def create_phoneme_repr(self):
        self.tentative_phonemes = self.simple_stressor()


    def main(self):
        self.get_syllable_count()
        self.create_phoneme_repr()



if __name__ == "__main__":
    from pprint import pprint

    words = ["quality", "inspections", "aeneidae", "look", "question", "thought", "thou", "linsey-woolsey", "pixie", "pixies", "yea", "treat", "galilaean", "harbingered", "yeoman"]

    res = []
    for word in words:
        ss = SpellingSyllabifier(word)
        res.append([word, ss.modified_word, ss.syllable_count])
    pprint(res)