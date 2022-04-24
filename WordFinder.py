import re
import pandas as pd
import argparse

from datetime import datetime


class WordFinder(object):
    def __init__(
        self, load_dir='datasets',
        filename='republican_comments.csv'
    ):
        self.load_path = f'{load_dir}/{filename}'
        self.df = pd.read_csv(self.load_path)

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

    @staticmethod
    def extract_sentence(comment, start_index, end_index):
        while start_index > 0:
            if comment[start_index] == '.':
                start_index += 1
                break

            start_index -= 1

        while end_index < len(comment) - 1:
            if comment[end_index] == '.':
                break

            end_index += 1

        return comment[start_index:end_index]

    @staticmethod
    def make_stamp():
        date = datetime.now()
        stamp = date.strftime('%y%m%d-%H%M')
        return stamp

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
        print(f'dataframe = {self.load_path}')
        print(f'span = {span}')


if __name__ == '__main__':
    """
    example command:
    python3 WordFinder.py --word republican --span 100 \
    --df dem-comments-220424-1305.csv
    """
    parser = argparse.ArgumentParser(description='Enter search word.')
    parser.add_argument(
        '--word', action='store', type=str,
        const='free', default='free', nargs='?'
    )
    parser.add_argument(
        '--span', action='store', type=int,
        const=40, default=50, nargs='?'
    )
    parser.add_argument(
        '--dir', action='store', type=str,
        const='datasets', default='datasets', nargs='?'
    )
    default_file = 'republican_comments.csv'
    parser.add_argument(
        '--df', action='store', type=str,
        const=default_file, default=default_file, nargs='?'
    )

    args = parser.parse_args()
    finder = WordFinder(
        load_dir=args.dir, filename=args.df
    )

    # finder.show_occurrences('free', 50)
    finder.show_occurrences(word=args.word, span=args.span)