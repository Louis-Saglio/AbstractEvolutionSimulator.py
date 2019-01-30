import multiprocessing as mp
from collections import OrderedDict

from models import Cosmos
from models import Population


class MetricComputer:

    STOP_MESSAGE = '$reserved_string_close'

    def __init__(self):
        self.input_queue = mp.Queue()
        self.output_queue = mp.Queue()
        self.process = mp.Process(target=self.start, args=())
        self.data_handler = CosmosMetrics()

    def add(self, cosmos: Cosmos):
        self.input_queue.put(cosmos)

    def start(self):
        while True:
            data = self.input_queue.get()
            if data == self.STOP_MESSAGE:
                break
            self.data_handler.handle(data)
        self.output_queue.put(self.data_handler.get_stats())

    def join(self):
        self.input_queue.put(self.STOP_MESSAGE)
        self.process.join()


class MetricData:

    def handle(self, data):
        raise NotImplementedError

    def get_stats(self):
        raise NotImplementedError


class CosmosMetrics(MetricData):

    def __init__(self):
        self.generation_sizes = []
        self.total_gene_nbr = {}
        self.gene_nbr_by_generation = []

    @staticmethod
    def compute_genes_nbr(population: Population, gene_nbr=None):
        if gene_nbr is None:
            gene_nbr = {}
        for individual in population:
            for gene in individual.genome:
                if gene not in gene_nbr:
                    gene_nbr[gene] = 0
                gene_nbr[gene] += 1
        return gene_nbr

    def handle(self, cosmos: Cosmos):
        self.generation_sizes.append(len(cosmos.population))
        self.compute_genes_nbr(cosmos.population, self.total_gene_nbr)
        self.gene_nbr_by_generation.append(self.sort(self.compute_genes_nbr(cosmos.population))[:5])

    @staticmethod
    def sort(data: dict):
        return OrderedDict(sorted(data.items(), key=lambda x: x[1], reverse=True))

    def get_stats(self):
        return {
            "generation_sizes": self.generation_sizes,
            "total_gene_nbr": self.sort(self.total_gene_nbr),
            "gene_nbr_by_generation": self.gene_nbr_by_generation
        }
