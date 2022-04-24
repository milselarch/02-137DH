from WordFinder import WordFinder
from tqdm import tqdm


class Extractor(WordFinder):
    def __init__(self, *args, **kwargs):
        super(Extractor, self).__init__(*args, **kwargs)
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

    def get_embeddings(self, word):
        df = self.filter_by_word(word)

        for k in range(len(df)):
            row = df.iloc[k]
            comment = row['comment']
            
