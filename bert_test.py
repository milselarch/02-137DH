import torch
import pandas as pd

from transformers import BertTokenizer, BertModel

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
df = pd.read_csv('datasets/republican_comments.csv')

print('dataframe head:')
print(df.head())

comment1 = df.loc[0]['comment']
print('comment[0]', comment1)
wrapped_comment = f"[CLS] {comment1} [SEP]"
tokenized_text = tokenizer.tokenize(wrapped_comment)
print(tokenized_text, len(tokenized_text))

indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
print('token indexes')
for tup in zip(tokenized_text, indexed_tokens):
    print('{:<12} {:>6,}'.format(tup[0], tup[1]))

segments_ids = [1] * len(tokenized_text)
tokens_tensor = torch.tensor([indexed_tokens]).to(device)
segments_tensors = torch.tensor([segments_ids]).to(device)

model = BertModel.from_pretrained(
    'bert-base-uncased',
    output_hidden_states=True,
    # Whether the model returns all hidden-states.
).to(device)

with torch.no_grad():
    outputs = model(tokens_tensor, segments_tensors)
    # Evaluating the model will return a different number of objects based on
    # how it's  configured in the `from_pretrained` call earlier. In this case,
    # because we set `output_hidden_states = True`, the third item will be the
    # hidden states from all layers. See the documentation for more details:
    # https://huggingface.co/transformers/model_doc/bert.html#bertmodel
    hidden_states = outputs[2]
    print(hidden_states)

    token_embeddings = torch.stack(hidden_states, dim=0)
    print('embeddings shape', token_embeddings.size())
    # embeddings shape torch.Size([13, 1, 209, 768])
    # [# layers, # batches, # tokens, # features]
    # Desired dimensions:
    # [# tokens, # layers, # features]

    # Let’s get rid of the “batches” dimension since we don’t need it.
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    # swap layers and tokens dimensions
    token_embeddings = token_embeddings.permute(1, 0, 2)
    print(token_embeddings.size())

    embedding = token_embeddings[12, -2, :]
    print(embedding, embedding.size())
    # torch.Size([209, 13, 768])