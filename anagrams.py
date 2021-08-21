from typing import Dict, Iterator


class Dictionary:
    """
    Inspired by <https://stackoverflow.com/a/1924561/9621945>
    """
    path: str
    end: bool
    parent: 'Dictionary'
    children: Dict[str, 'Dictionary']

    def __init__(self, path: str = '', end=False, parent=None):
        self.path = path
        self.end = end
        self.parent = parent
        self.children = {}

    @staticmethod
    def format(word: str):
        return "".join(c for c in word.lower().strip() if c.isalpha())

    @staticmethod
    def remove_first_char(word: str, char: str):
        remainder = [c for c in word]
        remainder.remove(char)
        return "".join(remainder)

    def get_root(self):
        return self.parent.get_root() if self.parent else self

    def ingest_all(self, words: Iterator[str]):
        for w in words:
            self.ingest(w)

    def ingest(self, word: str):
        if word:
            word = self.format(word)
            child = self.children.get(word[0], Dictionary(path=self.path + word[0], parent=self))
            child.ingest(word[1:])
            self.children[word[0]] = child
        else:
            self.end = True

    def anagrams(self, subject: str):
        subject = self.format(subject)
        if self.end and not subject:
            # Base case 1: Perfect match
            yield self.path
        elif self.end:
            # Base case 2: Hit end of path but still more string
            for anagram in self.get_root().anagrams(subject):
                yield f'{self.path} {anagram}'

        # Keep recursing deeper
        for c in set(subject):
            if c in self.children:
                yield from self.children[c].anagrams(self.remove_first_char(subject, c))


def load_dictionary():
    dictionary = Dictionary()
    with open('words.txt', 'r') as f:
        # Obtained <https://raw.githubusercontent.com/paolino/anagrams/master/words.txt>
        dictionary.ingest_all(f.readlines())
    return dictionary


def main():
    dictionary = load_dictionary()
    for anagram in dictionary.anagrams('Liam Peck'):
        print(f'- {anagram}')


if __name__ == '__main__':
    main()
