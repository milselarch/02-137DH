from WordFinder import WordFinder


class Extractor(WordFinder):
    def __init__(self, *args, **kwargs):
        super(Extractor, self).__init__(*args, **kwargs)
        self.tokenizer = None
        self.model = None

    def load_model(self):
        if self.tokenizer is not None:
            return

        self.tokenizer = BertTokenizer.from_pretrained(
            'bert-base-uncased'
        )
