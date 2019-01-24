from models import Cosmos
from operations import evaluate, mate, choose_partner, consume_resources


def main():
    cosmos = Cosmos()
    fitnesses = {}
    for i in range(8):
        print(i)
        # Evaluate population
        for individual in cosmos.population:
            if individual not in fitnesses:
                fitnesses[individual] = evaluate(cosmos.environment, individual)
        # Reduce population
        consume_resources(cosmos)
        # Reproduce population
        new_generation = []
        for individual in cosmos.population:
            new_generation.append(mate(individual, choose_partner(individual, cosmos.population, fitnesses)))
        cosmos.population += new_generation
    return cosmos


if __name__ == '__main__':
    main()
