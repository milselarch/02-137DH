import re
import pandas as pd
import argparse


class WordFinder(object):
    def __init__(
        self, load_path='datasets/republican_comments.csv'
    ):
        self.df = pd.read_csv(load_path)

    @staticmethod
    def get_search_regex(word):
        # make sure search word isn't interpreted as part
        # of the regex expression for special chars (/.*+ etc.)
        escaped_word = re.escape(word)
        # match the word only if it has whitespace before it,
        # and it has whitespace after (or it's the last word
        # in the comment). (?i) means search is case-insensitive
        pattern = re.compile(f'\\s(?i){escaped_word}(\\s|$)')
        return pattern

    def filter_by_word(self, word):
        regex = self.get_search_regex(word)
        matches = self.df[
            self.df['comment'].str.contains(regex)
        ]
        return matches

    def show_occurrences(self, word, span=40):
        """
        show the relevant snippets of the target word
        for all comments containing said word
        """
        match_df = self.filter_by_word(word)
        regex = self.get_search_regex(word)
        num_matches = len(match_df)

        for k in range(num_matches):
            comment = match_df.iloc[k]['comment']
            match = regex.search(comment)
            start, end = match.span()
            sub_comment = comment[
                max(start-span, 0):end+span
            ]

            print(f'comment [{k}] {start, end}')
            print(sub_comment)
            # print(comment)

        print('')
        print('-' * 40)
        print(f'{num_matches} matches for [{word}]')
        print(f'span = {span}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter search word.')
    parser.add_argument(
        '--word', action='store', type=str,
        const='free', default='free', nargs='?'
    )
    parser.add_argument(
        '--span', action='store', type=int,
        const=40, default=50, nargs='?'
    )

    finder = WordFinder()
    # finder.show_occurrences('free', 50)
    args = parser.parse_args()
    finder.show_occurrences(args.word, args.span)