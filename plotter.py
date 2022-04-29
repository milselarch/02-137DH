import time
import numpy as np
import matplotlib.pyplot as plt
import random

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from Extractor import Extractor
from EmbedsReader import EmbedsReader


class Plotter(object):
    def __init__(self, seed=None):
        self.reader = EmbedsReader()
        self.reader.load('extractions/extracts-220429-1935.npy')
        self.reader.load('extractions/extracts-220429-1937.npy')

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

    def plot_tsne(
        self, pair_map: dict, s=5, show=True,
        title='Embeddings', auto_color=False
    ):
        all_indexes, index_mapping = [], {}
        tsne = TSNE(
            n_components=2, verbose=1, perplexity=40, n_iter=300
        )

        plt.style.use('ggplot')
        plt.figure(figsize=(14, 8))
        plt.title(hist_title)
        embedding_groups = []

        for k, pair in enumerate(pair_map):
            tag, word = pair
            embeddings = self.reader.read_embeddings(tag, word)

            if len(embeddings) == 0:
                print(f'{word} HAS NO EMBEDDINGS')
                continue

            embedding_groups.append(embeddings)
            all_indexes.extend([k] * len(embeddings))
            index_mapping[pair] = k

        all_indexes = np.array(all_indexes)
        all_embeds = np.concatenate(embedding_groups)
        tsne_results = tsne.fit_transform(all_embeds)

        for k, pair in enumerate(pair_map):
            tag, word = pair
            color = pair_map[pair]
            indexes = np.where(all_indexes == k)
            positions = tsne_results[indexes]
            color = None if auto_color else color

            plt.scatter(
                positions[:, 0], positions[:, 1],
                c=color, s=s, label=f'{tag}:{word}'
            )

        plt.legend()

        if show:
            plt.show()

    def projection(
        self, source_word, end_word, project_word,
        hist_title='projection', scatter_title='test',
        bins=20, pair_map=None, auto_color=False, s=5
    ):
        all_indexes, index_mapping = [], {}
        tsne = TSNE(
            n_components=2, verbose=1, perplexity=40, n_iter=300
        )

        plt.style.use('ggplot')
        plt.figure(figsize=(14, 8))
        plt.title(hist_title)
        embedding_groups = []

        if pair_map is None:
            pair_map = {}

            for party in ('dem', 'rep'):
                pair_map[(party, source_word)] = None
                pair_map[(party, end_word)] = None
                pair_map[(party, project_word)] = None

        for k, pair in enumerate(pair_map):
            tag, word = pair
            embeddings = self.reader.read_embeddings(tag, word)
            if len(embeddings) == 0:
                print(f'{word} HAS NO EMBEDDINGS')
                continue

            embedding_groups.append(embeddings)
            all_indexes.extend([k] * len(embeddings))
            index_mapping[pair] = k

        all_embeds = np.concatenate(embedding_groups)
        tsne_results = tsne.fit_transform(all_embeds)
        all_indexes = np.array(all_indexes)

        # get average position of source and target word
        source_positions, end_positions = [], []
        for k, pair in enumerate(pair_map):
            tag, word = pair
            indexes = np.where(all_indexes == k)
            positions = tsne_results[indexes]

            if word == source_word:
                source_positions.append(positions)
            elif word == end_word:
                end_positions.append(positions)

        # print(source_positions)
        source_positions = np.concatenate(source_positions)
        end_positions = np.concatenate(end_positions)
        assert len(source_positions) > 0
        assert len(end_positions) > 0

        source_avg = np.average(source_positions, axis=0)
        end_avg = np.average(end_positions, axis=0)
        span = end_avg - source_avg

        # project embedding along a 1D vector
        all_edges = [0]
        hist_handles = []
        hist_labels = []

        for k, pair in enumerate(pair_map):
            tag, word = pair
            indexes = np.where(all_indexes == k)
            positions = tsne_results[indexes]

            if word != project_word:
                continue

            rebased_positions = (positions - source_avg)
            scaled_positions = np.dot(
                rebased_positions, span
            ) / (
                np.linalg.norm(span) * np.linalg.norm(rebased_positions, axis=1)
            )

            """
            plt.hist(
                scaled_positions, color=color, alpha=0.5,
                bins=bins
            )
            """

            color = 'red' if tag == 'rep' else 'blue'
            hist_values, bin_edges = np.histogram(
                scaled_positions, bins=bins
            )

            all_edges.extend(bin_edges)
            handle = plt.bar(
                x=bin_edges[:-1], alpha=0.5,
                height=hist_values / len(scaled_positions),
                width=np.diff(bin_edges),
                align='edge', color=color
            )

            party = 'democrat' if tag == 'dem' else 'republican'
            mean = np.mean(scaled_positions)
            label = f'{party} (mean={mean:.4f})'

            hist_labels.append(label)
            hist_handles.append(handle)

            print(pair, np.mean(scaled_positions))
            print(f'SHOW HIST {pair}')

        plt.xlim(
            min(0, min(all_edges)), max(1, max(all_edges))
        )
        plt.ylabel(f'% of total occurrences of {project_word}')
        plt.xlabel(f'{source_word} (0) to {end_word} (1) projections')
        plt.legend(hist_handles, hist_labels)
        plt.show()

        plt.style.use('ggplot')
        plt.figure(figsize=(14, 8))

        # plot scatter graph
        for k, pair in enumerate(pair_map):
            tag, word = pair
            color = pair_map[pair]
            indexes = np.where(all_indexes == k)
            positions = tsne_results[indexes]
            color = None if auto_color else color

            plt.scatter(
                positions[:, 0], positions[:, 1],
                c=color, s=s, label=f'{tag}:{word}',
            )

        plt.legend()
        plt.title(scatter_title)
        plt.show()

        return pair_map


if __name__ == '__main__':
    plotter = Plotter(seed=42)
    plotter.plot_tsne(pair_map={
        ('rep', 'government'): 'red',
        ('dem', 'government'): 'blue',
        ('rep', 'justice'): 'green',
        ('dem', 'justice'): 'black',
        ('rep', 'evil'): 'orangered',
        ('dem', 'evil'): 'indianred',
    }, title='perceptions of government, freedom and fascism')



