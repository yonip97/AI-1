
import ex1
import search
import time


def timeout_exec(func, args=(), kwargs={}, timeout_duration=10, default=None):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default

        def run(self):
            # try:
            self.result = func(*args, **kwargs)
            # except Exception as e:
            #    self.result = (-3, -3, e)

    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.is_alive():
        return default
    else:
        return it.result


def check_problem(p, search_method, timeout):
    """ Constructs a problem using ex1.create_wumpus_problem,
    and solves it using the given search_method with the given timeout.
    Returns a tuple of (solution length, solution time, solution)"""

    """ (-2, -2, None) means there was a timeout
    (-3, -3, ERR) means there was some error ERR during search """

    t1 = time.time()
    s = timeout_exec(search_method, args=[p], timeout_duration=timeout)
    t2 = time.time()

    if isinstance(s, search.Node):
        solve = s
        solution = list(map(lambda n: n.action, solve.path()))[1:]
        return (len(solution), t2 - t1, solution)
    elif s is None:
        return (-2, -2, None)
    else:
        return s


def solve_problems(problems):
    solved = 0
    f = open("results.txt", 'w')
    for problem in problems:
        try:
            p = ex1.create_drone_problem(problem)
        except Exception as e:
            print("Error creating problem: ", e)
            return None
        # TODO: change back
        timeout = 60
        result = check_problem(p, (lambda p: search.greedy_best_first_graph_search(p, p.h)), timeout)
        f.write("GBFS " + str(result) + '\n')
        print("GBFS ", result)
        if result[2] != None:
            if result[0] != -3:
                solved = solved + 1
    f.close()


def main():
    print(ex1.ids)
    """Here goes the input you want to check"""
    problems = [

        {
            "map": [['P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'P'], ],
            "drones": {'drone 1': (3, 3)},
            "packages": {'package 1': (0, 2),
                         'package 2': (2, 0)},
            "clients": {'Yossi': {"path": [(0, 1), (1, 1), (1, 0), (0, 0)],
                                  "packages": ('package 1', 'package 2')}}
        },

        # {
        #     "map": [['P', 'P', 'P', 'P'],
        #             ['P', 'P', 'P', 'P'],
        #             ['P', 'P', 'P', 'P'],
        #             ['P', 'P', 'P', 'P'], ],
        #     "drones": {'drone 1': (3, 3)},
        #     "packages": {'package 1': (2, 1),
        #                  'package 2': (2, 0)},
        #     "clients": {'Yossi': {"path": [(0, 1), (1, 1), (1, 0), (0, 0)],
        #                           "packages": ('package 1', 'package 2')}}
        # },
        #
        # {
        #     "map": [['P', 'P', 'P', 'P'],
        #             ['P', 'P', 'P', 'P'],
        #             ['P', 'I', 'P', 'I'],
        #             ['P', 'P', 'P', 'P'], ],
        #     "drones": {'drone 1': (3, 3),
        #                'drone 2': (1, 0)},
        #     "packages": {'package 1': (0, 3),
        #                  'package 2': (3, 0),
        #                  'package 3': (2, 1)},
        #     "clients": {'Sarah': {"path": [(0, 2), (2, 2), (2, 0), (0, 0)],
        #                           "packages": ('package 1', 'package 2', 'package 3')}}
        # },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'], ],
            "drones": {'drone 1': (3, 3),
                       'drone 2': (1, 0)},
            "packages": {'package 1': (0, 4),
                         'package 2': (3, 2),
                         'package 3': (2, 1),
                         'package 4': (2, 4), },
            "clients": {'Alice': {"path": [(0, 1), (1, 1), (1, 0), (0, 0), (2, 2)],
                                  "packages": ('package 1', 'package 2', 'package 3')},
                        'Bob': {"path": [(4, 3), (2, 2), (4, 2), (4, 4)],
                                "packages": ('package 4',)},
                        }
        },
    ]
    non_competitive_inputs = [
        {
            "map": [['P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'P'], ],
            "drones": {'drone 1': (3, 3)},
            "packages": {'package 1': (0, 2),
                         'package 2': (0, 2)},
            "clients": {'Alice': {"path": [(0, 1), (1, 1), (1, 0), (0, 0)],
                                  "packages": ('package 1', 'package 2')}}
        },

        {
            "map": [['P', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P'],
                    ['P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'P'], ],
            "drones": {'drone 1': (3, 3)},
            "packages": {'package 1': (0, 2),
                         'package 2': (0, 2)},
            "clients": {'Alice': {"path": [(0, 1), (1, 1), (2, 0), (0, 0)],
                                  "packages": ('package 1', 'package 2')}}
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (3, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
                                  "packages": ('package 1',)}}
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0), },
            "packages": {'package 1': (3, 4),
                         'package 2': (3, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
                                  "packages": ('package 1',)},
                        'Bob': {"path": [(2, 0), (2, 1), (2, 3), (2, 4)],
                                "packages": ('package 2',)}
                        }
        },

        {
            "map": [['P', 'P', 'P'],
                    ['P', 'P', 'P'],
                    ['P', 'I', 'P']],
            "drones": {'drone 1': (0, 1)},
            "packages": {'package 1': (0, 2),
                         'package 2': (0, 2)},
            "clients": {'Alice': {"path": [(2, 0), (2, 2)],
                                  "packages": ('package 1', 'package 2')}}
        },

    ]

    competitive_inputs = [
        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (3, 4),
                         'package 2': (3, 4),
                         'package 3': (3, 4),
                         'package 4': (3, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
                                  "packages": ('package 1', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (5, 4),
                         'package 2': (5, 4),
                         'package 3': (5, 4),
                         'package 4': (5, 4),
                         'package 5': (5, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 1', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(5, 1)],
                                    "packages": ('package 5',)},
                        }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4),
                       'drone 3': (5, 0)},
            "packages": {'package 1': (5, 4),
                         'package 2': (5, 4),
                         'package 3': (5, 4),
                         'package 4': (5, 4),
                         'package 5': (5, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 5', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(5, 1)],
                                    "packages": ('package 1',)},
                        }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (5, 4),
                         'package 2': (5, 4),
                         'package 3': (5, 4),
                         'package 4': (5, 4),
                         'package 5': (5, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 1', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(5, 1)],
                                    "packages": ('package 5',)},
                        }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'I', 'P'],
                    ['P', 'I', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'I', 'I', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P']],
            "drones": {'drone 1': (14, 10),
                       'drone 2': (8, 11),
                       'drone 3': (9, 3),
                       'drone 4': (6, 0),
                       'drone 5': (1, 12),
                       'drone 6': (13, 2)},
            "packages": {'p1': (9, 6),
                         'p2': (9, 6),
                         'p3': (9, 6),
                         'p4': (9, 6),
                         'p5': (9, 6),
                         'p6': (9, 6),
                         'p7': (9, 6),
                         'p8': (9, 6),
                         'p9': (9, 6),
                         'p10': (9, 6),
                         'p11': (9, 6),
                         'p12': (9, 6),
                         'p13': (9, 6),
                         'p14': (9, 6),
                         'p15': (9, 6),
                         'p16': (9, 6),
                         'p17': (9, 6),
                         'p18': (9, 6),
                         'p19': (9, 6),
                         'p20': (9, 6)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (1, 1), (1, 0)],
                                  "packages": ('p1', 'p2', 'p3', 'p4', 'p5')},
                        'Bob': {"path": [(4, 4), (4, 5), (5, 5), (5, 4)],
                                "packages": ('p6', 'p7', 'p8', 'p9', 'p10')},
                        'Charlie': {"path": [(8, 11), (9, 3), (8, 0), (3, 12)],
                                    "packages": ('p11', 'p12', 'p13', 'p14', 'p15')},
                        'David': {"path": [(14, 14), (3, 13), (6, 6), (6, 7)],
                                  "packages": ('p16', 'p17', 'p18', 'p19', 'p20')},
                        }
        },

    ]
    my = [{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'I', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['I', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'I', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P']], 'drones': {'drone 0': (2, 5), 'drone 1': (3, 3), 'drone 2': (2, 2), 'drone 3': (2, 2)}, 'packages': {'package 0': (1, 1), 'package 1': (5, 3), 'package 2': (3, 4), 'package 3': (2, 4)}, 'clients': {'BPKGM': {'path': [(2, 2), (3, 3), (2, 1), (5, 5), (3, 3)], 'packages': ('package 0',)}, 'DCDNJ': {'path': [(4, 4), (5, 5), (3, 5), (3, 3)], 'packages': ('package 1', 'package 2', 'package 3')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'I', 'P']], 'drones': {'drone 0': (5, 5), 'drone 1': (4, 3)}, 'packages': {'package 0': (2, 1), 'package 1': (1, 4), 'package 2': (4, 5), 'package 3': (3, 5), 'package 4': (3, 4), 'package 5': (2, 2), 'package 6': (1, 4), 'package 7': (1, 1), 'package 8': (1, 1), 'package 9': (4, 5), 'package 10': (4, 5), 'package 11': (5, 5)}, 'clients': {'XLRIE': {'path': [(4, 4), (2, 4), (4, 1), (1, 4), (2, 1), (1, 3)], 'packages': ('package 0', 'package 1', 'package 2', 'package 3', 'package 4', 'package 5', 'package 6', 'package 7', 'package 8', 'package 9', 'package 10', 'package 11')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'I', 'P', 'P', 'I']], 'drones': {'drone 0': (5, 4), 'drone 1': (5, 4), 'drone 2': (2, 2), 'drone 3': (2, 1)}, 'packages': {'package 0': (4, 1), 'package 1': (4, 1), 'package 2': (4, 5), 'package 3': (2, 1), 'package 4': (3, 1), 'package 5': (1, 4), 'package 6': (4, 5), 'package 7': (5, 4), 'package 8': (2, 3), 'package 9': (3, 3), 'package 10': (2, 3), 'package 11': (1, 4)}, 'clients': {'BOYXB': {'path': [(1, 4), (2, 5), (2, 4), (2, 1)], 'packages': ('package 0', 'package 1', 'package 6', 'package 10')}, 'TLWRY': {'path': [(2, 5), (2, 2), (2, 2), (5, 3), (3, 3), (3, 5)], 'packages': ('package 2', 'package 3', 'package 4', 'package 5', 'package 7', 'package 8', 'package 9', 'package 11')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'I', 'P', 'I', 'P'], ['I', 'P', 'P', 'P', 'P', 'I']], 'drones': {'drone 0': (3, 2), 'drone 1': (2, 3)}, 'packages': {'package 0': (3, 2), 'package 1': (4, 5), 'package 2': (2, 1), 'package 3': (5, 1)}, 'clients': {'VXKAN': {'path': [(3, 1), (2, 3), (5, 2), (1, 3), (5, 5), (4, 2)], 'packages': ('package 0', 'package 1', 'package 2', 'package 3')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'I', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'I', 'P']], 'drones': {'drone 0': (2, 2), 'drone 1': (2, 2), 'drone 2': (4, 5)}, 'packages': {'package 0': (3, 5), 'package 1': (3, 4), 'package 2': (3, 1), 'package 3': (3, 1)}, 'clients': {'IAYLP': {'path': [(1, 4), (4, 1), (1, 2), (5, 3)], 'packages': ('package 0', 'package 1', 'package 2', 'package 3')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'I', 'P']], 'drones': {'drone 0': (4, 5), 'drone 1': (2, 3), 'drone 2': (2, 5)}, 'packages': {'package 0': (1, 5), 'package 1': (4, 5), 'package 2': (2, 1), 'package 3': (4, 5)}, 'clients': {'WLGOZ': {'path': [(1, 4), (2, 5), (5, 1), (3, 5), (4, 3), (1, 1)], 'packages': ('package 3',)}, 'EILEC': {'path': [(5, 4), (3, 4), (4, 5), (1, 4), (3, 1)], 'packages': ('package 0', 'package 1', 'package 2')}, 'QHOWV': {'path': [(4, 1), (2, 1), (3, 4), (4, 5), (2, 3), (1, 1)], 'packages': ()}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'I', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P']], 'drones': {'drone 0': (1, 3), 'drone 1': (5, 3), 'drone 2': (5, 2)}, 'packages': {'package 0': (3, 2), 'package 1': (1, 5), 'package 2': (5, 1), 'package 3': (3, 1), 'package 4': (1, 5), 'package 5': (3, 4), 'package 6': (4, 5), 'package 7': (2, 2), 'package 8': (3, 5), 'package 9': (1, 4), 'package 10': (1, 1)}, 'clients': {'OSQNB': {'path': [(2, 2), (4, 1), (2, 3), (1, 2)], 'packages': ('package 0', 'package 1', 'package 2', 'package 3', 'package 4', 'package 5', 'package 6', 'package 7', 'package 8', 'package 9', 'package 10')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'I', 'P'], ['I', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['I', 'P', 'P', 'P', 'I', 'P']], 'drones': {'drone 0': (2, 2), 'drone 1': (5, 2), 'drone 2': (5, 4), 'drone 3': (1, 3)}, 'packages': {'package 0': (5, 3), 'package 1': (2, 3), 'package 2': (4, 2), 'package 3': (5, 2), 'package 4': (2, 5), 'package 5': (5, 5), 'package 6': (4, 1), 'package 7': (5, 1), 'package 8': (1, 5), 'package 9': (1, 1)}, 'clients': {'EGOQB': {'path': [(1, 2), (3, 5), (2, 2), (3, 3)], 'packages': ('package 0', 'package 1', 'package 2', 'package 6', 'package 7', 'package 9')}, 'CDFBU': {'path': [(3, 3), (3, 5), (1, 1), (3, 5), (4, 5), (5, 4)], 'packages': ('package 3', 'package 4', 'package 5', 'package 8')}}}
,{'map': [['P', 'P', 'I', 'P', 'P', 'P'], ['P', 'I', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['I', 'P', 'P', 'P', 'P', 'P']], 'drones': {'drone 0': (3, 4), 'drone 1': (3, 2), 'drone 2': (3, 2)}, 'packages': {'package 0': (4, 1), 'package 1': (2, 1), 'package 2': (2, 3), 'package 3': (2, 4), 'package 4': (3, 1), 'package 5': (2, 1), 'package 6': (4, 2), 'package 7': (4, 1), 'package 8': (2, 4)}, 'clients': {'SQYBC': {'path': [(4, 1), (1, 5), (2, 1), (4, 3), (1, 3), (4, 2)], 'packages': ('package 0', 'package 1', 'package 2', 'package 3', 'package 4', 'package 5', 'package 6', 'package 7', 'package 8')}}}
,{'map': [['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'I', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'I', 'I', 'P']], 'drones': {'drone 0': (1, 5), 'drone 1': (3, 2)}, 'packages': {'package 0': (2, 1), 'package 1': (5, 5), 'package 2': (3, 1), 'package 3': (4, 1), 'package 4': (4, 3)}, 'clients': {'RYEHV': {'path': [(1, 5), (5, 5), (2, 4), (3, 5), (5, 2), (3, 3)], 'packages': ('package 0', 'package 1', 'package 3', 'package 4')}, 'YIJJW': {'path': [(5, 2), (1, 2), (5, 2), (5, 1)], 'packages': ('package 2',)}}}
,{'map': [['I', 'P', 'P', 'P', 'P', 'I'], ['P', 'P', 'P', 'P', 'P', 'P'], ['I', 'P', 'P', 'P', 'P', 'P'], ['P', 'I', 'P', 'P', 'P', 'P'], ['P', 'P', 'P', 'P', 'P', 'P'], ['I', 'P', 'P', 'P', 'P', 'P']], 'drones': {'drone 0': (2, 5), 'drone 1': (5, 1), 'drone 2': (2, 3)}, 'packages': {'package 0': (3, 5), 'package 1': (3, 2), 'package 2': (4, 3), 'package 3': (1, 3), 'package 4': (2, 5), 'package 5': (5, 1)}, 'clients': {'LIQQV': {'path': [(2, 2), (1, 3), (1, 4), (3, 5)], 'packages': ('package 0', 'package 1', 'package 2', 'package 3', 'package 4', 'package 5')}}}
]
    ziv =[{
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (3, 4),
                         'package 2': (0, 0),
                         'package 3': (3, 4),
                         'package 4': (0, 2)},
            "clients": {
                'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
                          "packages": ('package 1', 'package 2')},
                'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                        "packages": ('package 3', 'package 4')},
            }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'I'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (5, 4),
                         'package 2': (0, 0),
                         'package 3': (5, 4),
                         'package 4': (0, 3),
                         'package 5': (5, 2)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 1', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(5, 1)],
                                    "packages": ('package 5',)},
                        }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4),
                       'drone 3': (5, 0)},
            "packages": {'package 1': (5, 4),
                         'package 2': (1, 3),
                         'package 3': (5, 2),
                         'package 4': (0, 2),
                         'package 5': (5, 4)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 5', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(5, 1)],
                                    "packages": ('package 1',)},
                        }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (5, 4),
                         'package 2': (2, 1),
                         'package 3': (5, 4),
                         'package 4': (3, 4),
                         'package 5': (0, 0)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 1', 'package 2')},
                        'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(5, 1)],
                                    "packages": ('package 5',)},
                        }
        },
##################################################################
        {
            "map": [['P', 'P', 'P', 'P', 'P','P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'P', 'I','P', 'I','P'], ],
            "drones": {'drone 1': (0, 9),
                       'drone 2': (1, 2),
                       'drone 3': (0, 9),},

            "packages": {'package 1': (3, 1),
                         'package 2': (3, 4),
                         'package 3': (2, 4),
                         'package 4': (1, 4)},
            "clients": {
                'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)],
                          "packages": ('package 1', 'package 2')},
                'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                        "packages": ('package 3', 'package 4')},
            }
        },

        {
            "map": [['P', 'P', 'P', 'P', 'I'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ['P', 'I', 'I', 'P', 'P'],
                    ['P', 'I', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'], ],
            "drones": {'drone 1': (3, 0),
                       'drone 2': (2, 4)},
            "packages": {'package 1': (5, 4),
                         'package 2': (0, 0),
                         'package 3': (5, 4),
                         'package 4': (0, 3),
                         'package 5': (5, 0),
                         'package 6': (5, 0)},
            "clients": {'Alice': {"path": [(0, 0), (0, 1), (0, 3), (0, 4)],
                                  "packages": ('package 1', 'package 2')},
                        'Bob': {"path": [(2, 3), (4, 3)],
                                "packages": ('package 3', 'package 4')},
                        'Charlie': {"path": [(4, 1), (3, 1), (2, 1), (1, 1), (3, 3)],
                                    "packages": ('package 5',)},
                        }
        },
        {
            "map": [['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'P', 'I', 'P', 'I', 'P'],
                    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'P', 'P', 'P', 'P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P', 'P', 'I', 'P', 'I', 'P'],
                    ],
            "drones": {'drone 1': (0, 9),
                       'drone 2': (4, 5),
                        },

            "packages": {'package 1': (3, 1),
                         'package 2': (3, 4),
                         'package 3': (2, 4),
                         'package 4': (1, 4),
                         'package 5': (6, 6),
                         'package 6': (7, 4),
                         },
            "clients": {
                'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                                   (0, 5), (0, 6), (0, 7), (0, 8)],
                          "packages": ('package 1', 'package 2')},
                'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                        "packages": ('package 3', 'package 4')},
            }
        },
        {
            "map": [['P', 'P', 'P', 'P', 'P'],
                    ['P', 'I', 'I', 'I', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'I', 'P', 'P'],
                    ['P', 'P', 'P', 'I', 'P'],
                    ['P', 'I', 'P', 'P', 'P'],
                    ],
            "drones": {'drone 1': (0, 4),
                       'drone 2': (4, 4),
                       'drone 3': (5, 3),
                       },

            "packages": {'package 1': (3, 1),
                         'package 2': (3, 4),
                         'package 3': (2, 4),
                         'package 4': (0, 0),
                         },
            "clients": {
                'Alice': {"path": [(0, 0), (0, 1), (0, 2), (0, 3)],
                          "packages": ('package 1', 'package 2')},
                'Bob': {"path": [(2, 3), (3, 3), (3, 2)],
                        "packages": ('package 3', 'package 4')},
            }
        }]
    # from test_generator import create_test,if_solvable
    # for i in range(100):
    #     prob = create_test(6,6,4,12,3)
    #     if if_solvable(prob):
    #         print(prob)
    #         my.append(prob)
    #         if len(my) >10:
    #             break

    solve_problems(competitive_inputs)



if __name__ == '__main__':
    main()
