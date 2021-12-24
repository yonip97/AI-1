import pprint
import random
from random import randrange
import string


def create_test(max_length, max_width, drone_amount, pckg_amount, client_amount, seed=None):
    """
    Generates random tests for drone assignment.
    recommended use is like this: "problems = [create_test(5, 5, 2, 4, 2) for i in range(number_of_wanted_tests)]
    :param max_length: maximum length of map, at least 3
    :param max_width:  maximum width of map, at least 3
    :param drone_amount: maximum drone amount on map
    :param pckg_amount: maximum package amount on map
    :param client_amount: maximum client amount on map
    :param seed: (optional) seed to get pseudorandom numbers with fixed values over many iterations.
    :return: a single test
    """
    if seed is not None:
        random.seed(seed)
    # width = randrange(4, max_width)
    # length = randrange(4, max_length)
    length = 6
    width = 6
    test = {"map": [['P' if random.random() > 0.15 else 'I' for i in range(length)] for j in range(width)],
            "drones": {f'drone {i}': (randrange(1, width), randrange(1, length)) for i in
                       range(randrange(2, drone_amount + 1))},
            "packages": {f'package {i}': (randrange(1, width), randrange(1, length)) for i in
                         range(randrange(4, pckg_amount + 1))},
            "clients":
                {''.join(random.choices(string.ascii_uppercase, k=5)):
                     {"path": [(randrange(1, width), randrange(1, length)) for i in range(randrange(4, 7))],
                      "packages": []} for i in range(randrange(1, client_amount + 1))}}
    # assign package to random client

    for pckg, _ in test['packages'].items():
        random_client = random.choice(list(test['clients'].keys()))
        test['clients'][random_client]['packages'].append(pckg, )

    for name, data in test['clients'].items():
        data['packages'] = (*data['packages'],)

    return test


def if_solvable(problem):
    for pckg, (x, y) in problem['packages'].items():
        if problem['map'][x][y] == 'I':
            return False
    return True


if __name__ == '__main__':
    tests = [create_test(5, 5, 2, 4, 2) for i in range(5)]
    pprint.pprint(tests)
