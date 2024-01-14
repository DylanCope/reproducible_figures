import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


matplotlib.use("pdf")


def create_nx_figure(data: pd.DataFrame):
    data.columns = data.index
    graph = nx.from_pandas_adjacency(data)
    nx.draw(graph)


def reproduce_figure():
    data = pd.read_csv("figures/test_nx_fig/data.csv")
    create_nx_figure(data)
    plt.savefig("figures/test_nx_fig/test_nx_fig.pdf", bbox_inches="tight")


if __name__ == "__main__":
    reproduce_figure()
