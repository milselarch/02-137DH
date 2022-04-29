from plotter import Plotter

plotter = Plotter(seed=12312)
# plotter.projection('justice', 'evil', 'government')
pair_map = {
    ('rep', 'healthcare'): 'red',
    ('dem', 'healthcare'): 'blue',
    ('rep', 'entitled'): 'green',
    ('dem', 'entitled'): 'black',
    ('rep', 'necessary'): 'orangered',
    ('dem', 'necessary'): 'indianred',
}

plotter.projection(
    'entitled', 'necessary', 'healthcare',
    pair_map=pair_map,
    hist_title='[healthcare] Embeddings projection between entitled (0) and necessary (1)',
    scatter_title='Embeddings of healthcare, entitled, and necessary'
)

