from plotter import Plotter

plotter = Plotter(seed=105)
plotter.plot_tsne(pair_map={
    ('rep', 'police'): 'red',
    ('dem', 'police'): 'blue',
    ('rep', 'fascist'): 'green',
    ('dem', 'fascist'): 'black',
    ('rep', 'justice'): 'orangered',
    ('dem', 'justice'): 'indianred',
}, title='perceptions of police, fascism and justice')


