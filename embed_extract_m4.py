import numpy as np

from Extractor import Extractor
from datetime import datetime

words_list = [
    'government', 'tyrant', 'necessity',
    'america', 'confederate', 'martyr', 'hero',
    'traitor', 'russia', 'china', 'justice', 'injustice',
    'racist', 'tolerant', 'victim', 'welfare',
    'necessary', 'need', 'want',

    'republican', 'democrat', 'evil', 'good',
    'healthcare', 'libertarian', 'authoritarian',
    'liberal', 'conservative', 'drugs', 'weed',
    'cannabis', 'marijuana', 'necessity'

    'rights', 'right', 'left', 'freedom', 'liberty',
    'police', 'immigrants', 'immigrant', 'illegal',
    'legal', 'privilege', 'entitled', 'angry', 'lazy',
    'dilligent', 'stupid', 'intelligent',
    'communist', 'communism', 'fascist', 'fascism',
    'socialist', 'socialism'
]

dem_filename = 'dem-comments-220424-1305-cc.csv'
dem_extractor = Extractor(filename=dem_filename, )
dem_extractor.extract_all(
    export=True, tag='dem', words=words_list
)

rep_filename = 'rep-comments-220424-1133-cc.csv'
rep_extractor = Extractor(filename=rep_filename)
rep_extractor.extract_all(
    export=True, tag='rep', words=words_list
)