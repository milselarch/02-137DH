import re
import numpy as np
import torch

from WordFinder import WordFinder
from datetime import datetime

from transformers import BertTokenizer, BertModel
from tqdm import tqdm


class Extractor(WordFinder):
    def __init__(self, *args, **kwargs):
        super(Extractor, self).__init__(*args, **kwargs)
        # we use second last BERT layer output as our embeddings
        self.embeddings_layer = -2

        self.device = None
        self.tokenizer = None
        self.model = None

    def load_model(self):
        if self.device is not None:
            return False

        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu"
        )
        self.tokenizer = BertTokenizer.from_pretrained(
            'bert-base-uncased'
        )
        self.model = BertModel.from_pretrained(
            'bert-base-uncased',
            output_hidden_states=True
            # Whether the model returns all hidden-states.
        ).to(self.device)

    def word_embedding(self, word):
        # gets the embedding for a single word without context
        return self.load_embeddings(word, word)[0]

    def load_embeddings(self, sentence, word):
        assert '.' not in sentence
        self.load_model()

        wrapped_comment = f"[CLS] {sentence} [SEP]"
        tokenized_text = self.tokenizer.tokenize(wrapped_comment)
        print(tokenized_text)

        np_tokenized_text = np.array(tokenized_text)
        word_token_indexes = np.where(np_tokenized_text == word)[0]

        segments_ids = [1] * len(tokenized_text)
        segments_tensor = torch.tensor([segments_ids]).to(self.device)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(
            tokenized_text
        )

        tokens_tensor = torch.tensor([indexed_tokens])
        tokens_tensor = tokens_tensor.to(self.device)
        outputs = self.model(tokens_tensor, segments_tensor)
        hidden_states = outputs[2]

        token_embeddings = torch.stack(hidden_states, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        token_embeddings = token_embeddings.permute(1, 0, 2)
        # dimensions now are [tokens, layers, 768]
        # word embedding is a length-768 vector

        word_embeddings = []
        for word_token_index in word_token_indexes:
            # print('WORD IDX', word_token_index, word_token_indexes)
            word_embedding = token_embeddings[
                             word_token_index, self.embeddings_layer, :
                             ]

            word_embedding = torch.flatten(word_embedding)
            np_embedding = word_embedding.cpu().detach().numpy()
            word_embeddings.append(np_embedding)

        return word_embeddings

    def get_embeddings(self, word):
        self.load_model()

        df = self.filter_by_word(word)
        pattern = self.get_search_regex(word)
        all_embeddings, all_indexes = [], []
        all_comment_ids = []

        pbar = tqdm(range(len(df)))

        for k in pbar:
            row = df.iloc[k]
            comment = row['comment']
            comment_id = row['comment_id']
            pbar.set_description(comment_id)

            # replace trailing dots like .. or ...
            comment = re.sub('\\.{2,}', '', comment)
            # replace all whitespace with spaces
            comment = re.sub('\\s+', ' ', comment)
            sentences = []

            for match in re.finditer(pattern, comment):
                word_indexes = match.span()

                start, end = word_indexes
                sentence = self.extract_sentence(comment, start, end)
                sentence = sentence.strip().lower()
                # word_count = sentence.count(word)

                if sentence not in sentences:
                    sentences.append(sentence)

            for sentence in sentences:
                print('sentence =', sentence)
                embeddings = self.load_embeddings(sentence, word)
                num_words = len(embeddings)
                all_comment_ids.extend([comment_id] * num_words)
                all_embeddings.extend(embeddings)

        return all_embeddings, all_comment_ids

    def extract_embeddings(
            self, word, export_dir='extractions', export=True
    ):
        stamp = self.make_stamp()
        embeddings, comment_ids = self.get_embeddings(word)
        export_path = f'{export_dir}/extract-{stamp}.npy'

        if export:
            np.save(export_path, {
                'filepath': self.load_path,
                'embeddings': embeddings,
                'comment_ids': comment_ids,
                'target_word': word,
                'stamp': stamp
            })

            print(f'exported embeddings to {export_path}')


if __name__ == '__main__':
    extractor = Extractor()
    test_sentence = 'This is a test sentence, ' \
                    'and this is a test of my resolve as well'

    word_vectors = extractor.load_embeddings(test_sentence, 'test')
    print(len(word_vectors), word_vectors[0].shape)
