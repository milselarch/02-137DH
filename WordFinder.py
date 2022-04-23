import re
import pandas as pd


class WordFinder(object):
    def __init__(
        self, load_path='datasets/republican_comments.csv'
    ):
        self.df = pd.read_csv(load_path)

    def filter_by_word(self, word):
        match_template = f'\\s(?i){word}\\s'
        matches = self.df[
            self.df['comment'].str.contains(match_template)
        ]
        return matches

    def show_occurrences(self, word, span=40):
        match_df = self.filter_by_word(word)
        pattern = re.compile(f'\\s(?i){word}\\s')

        for k in range(len(match_df)):
            comment = match_df.iloc[k]['comment']
            match = pattern.search(comment)
            start, end = match.span()
            sub_comment = comment[start-span:end+span]

            print(f'comment [{k}]')
            print(sub_comment)


if __name__ == '__main__':
    finder = WordFinder()
    finder.show_occurrences('free', 50)