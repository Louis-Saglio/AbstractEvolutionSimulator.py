from time import time

from conf import DEFAULT_COSMOS_RESOURCE_REGENERATION_RATE
from metrics import MetricComputer
from models import Cosmos
from operations import evaluate, mate, choose_partner, consume_resources


def main():
    metric = MetricComputer()
    metric.process.start()
    cosmos = Cosmos()
    fitnesses = {}
    start = time()
    metric_time, evaluation_time, reduce_time, reproduction_time = 0, 0, 0, 0
    for i in range(10000):
        try:
            if i % 100 == 0:
                print(i)
            # Evaluate population
            deb = time()
            for individual in cosmos.population:
                if individual not in fitnesses:
                    fitnesses[individual] = evaluate(cosmos.environment, individual)
            evaluation_time += (time() - deb)
            # Reduce population
            deb = time()
            cosmos.population, cosmos.resources = consume_resources(cosmos)
            reduce_time += (time() - deb)
            # todo : remove deads from fitness
            # Reproduce population
            deb = time()
            new_generation = []
            for individual in cosmos.population:
                new_generation.append(mate(individual, choose_partner(individual, cosmos.population, fitnesses)))
            cosmos.population += new_generation
            cosmos.resources += DEFAULT_COSMOS_RESOURCE_REGENERATION_RATE
            reproduction_time += (time() - deb)
            deb = time()
            metric.add(cosmos)
            metric_time += (time() - deb)
        except KeyboardInterrupt:
            break
    print("evaluation_time", evaluation_time)
    print("reduce_time", reduce_time)
    print("reproduction_time", reproduction_time)
    print("metric_time", metric_time)
    print("main loop time", time() - start)
    metric.join()
    return cosmos, metric.output_queue.get()


if __name__ == '__main__':
    result = main()
