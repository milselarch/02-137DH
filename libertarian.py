from plotter import Plotter

plotter = Plotter(seed=105)
plotter.plot_tsne(pair_map={
    ('rep', 'republican'): 'red',
    ('dem', 'republican'): 'blue',
    ('rep', 'democrat'): 'green',
    ('dem', 'democrat'): 'black',
    ('rep', 'libertarian'): 'orangered',
    ('dem', 'libertarian'): 'indianred',
}, title='perceptions of libertarians, democrats and republicans')


