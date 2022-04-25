import numpy as np

from Extractor import Extractor
from datetime import datetime

filename = 'dem-comments-220424-1305.csv'
extractor = Extractor(filename=filename)
extractor.extract_embeddings('fascist', export=True)