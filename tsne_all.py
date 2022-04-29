from plotter import Plotter

words_list = [
    'tyrant', 'america', 'confederate', 'martyr', 'hero',
    'traitor', 'evil'
]

pairs = {}
for word in words_list:
    pairs[('rep', word)] = None
    pairs[('dem', word)] = None

pairs[('dem', 'hero')] = 'teal'
plotter = Plotter(seed=42)
plotter.plot_tsne(pair_map={
    ('rep', 'tyrant'): 'red',
    ('dem', 'tyrant'): 'red',
    ('rep', 'america'): 'black',
    ('dem', 'america'): 'black',
    ('rep', 'confederate'): 'green',
    ('dem', 'confederate'): 'green',
    ('rep', 'hero'): 'blue',
    ('dem', 'hero'): 'blue',
}, title='perceptions of government, freedom and fascism')
