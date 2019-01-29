from conf import DEFAULT_COSMOS_RESOURCE_REGENERATION_RATE
from metrics import MetricComputer
from models import Cosmos
from operations import evaluate, mate, choose_partner, consume_resources


def main():
    metric = MetricComputer()
    metric.process.start()
    cosmos = Cosmos()
    fitnesses = {}
    for i in range(1000):
        try:
            if i % 100 == 0:
                print(i)
            # Evaluate population
            for individual in cosmos.population:
                if individual not in fitnesses:
                    fitnesses[individual] = evaluate(cosmos.environment, individual)
            # Reduce population
            cosmos.population, cosmos.resources = consume_resources(cosmos)
            # todo : remove deads from fitness
            # Reproduce population
            new_generation = []
            for individual in cosmos.population:
                new_generation.append(mate(individual, choose_partner(individual, cosmos.population, fitnesses)))
            cosmos.population += new_generation
            cosmos.resources += DEFAULT_COSMOS_RESOURCE_REGENERATION_RATE
            metric.add(cosmos)
        except KeyboardInterrupt:
            break
    metric.join()
    return cosmos, metric.output_queue.get()


if __name__ == '__main__':
    result = main()
