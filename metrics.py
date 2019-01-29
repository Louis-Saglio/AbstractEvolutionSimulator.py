import multiprocessing as mp

from models import Cosmos


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
        self.generation_sizes = list()

    def handle(self, cosmos: Cosmos):
        self.generation_sizes.append(len(cosmos.population))

    def get_stats(self):
        return self.generation_sizes
