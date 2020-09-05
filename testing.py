"""
Testing

In order to test the best performance and robustness of the enhanced BA, 
eight continuous-type benchmark functions with diﬀerent complexity and dimensions are applied 
to this new enhanced BA variant.

List of selected benchmark functions:
  - Ackley (10D)
  - Schaﬀer (2D)
  - Schwefel (2D)
  - Easom (2D)
  - Goldstein and Price (2D)
  - Rastrigin (10D)
  - Hypersphere (10D)
  - Martin and Gaddy (2D)

af means average ﬁtness, sdf means means standard deviation of ﬁtness
ai means average iterations, sdi means standard deviation of iterations

Requirements:
  - pandas
Python:
  - 3.7.7
"""

import math
import pandas as pd
import enhancedBA

Ackley_bees_parameters = {'ns':30, 'nb':8, 'nr':80, 'stlim':5}
Schaffer_bees_parameters = {'ns':40, 'nb':5, 'nr':100, 'stlim':10}
Schwefel_bees_parameters = {'ns':35, 'nb':8, 'nr':80, 'stlim':10}
Easom_bees_parameters = {'ns':35, 'nb':8, 'nr':80, 'stlim':10}
GoldsteinAndPrice_bees_parameters = {'ns':35, 'nb':10, 'nr':80, 'stlim':10}
Rastrigin_bees_parameters = {'ns':30, 'nb':10, 'nr':80, 'stlim':5}
Hypersphere_bees_parameters = {'ns':35, 'nb':10, 'nr':80, 'stlim':10}
MartinGaddy_bees_parameters = {'ns':30, 'nb':8, 'nr':100, 'stlim':10}

robustness_test =  {'ns':35, 'nb':8, 'nr':80, 'stlim':10}

def test_on_function(function_name, test_function, lower_bound, upper_bound, bees_parameters, optimum_fitness, ba_class=enhancedBA.EnhancedBA):
    n_runs = 50
    results=[]
    print("Run\tIteration\tFitness")
    print("="*30)
    
    for i in range(n_runs):
        a = ba_class(test_function, lower_bound, upper_bound, ns=bees_parameters['ns'], nb=bees_parameters['nb'], nr=bees_parameters['nr'], stlim=bees_parameters['stlim'])
        iteration, fitness = a.stoppingCriterion(max_iteration=5000, max_fitness=optimum_fitness - 0.001)
        results += [(iteration, fitness)]
        if i % 5 == 0:
            print(str(i) + '\t' + str(iteration) + '\t' + str(fitness))

    iteration_avg = sum([float(r[0]) for r in results]) / n_runs
    sd_iteration = math.sqrt(sum([pow(r[0] - iteration_avg, 2) for r in results]) / n_runs)
    fitness_avg = sum([r[1] for r in results]) / n_runs
    sd_fitness = math.sqrt(sum([pow(r[1] - fitness_avg, 2) for r in results]) / n_runs)
    print('')
    print("ai: " + str(iteration_avg) + " sdi: " + str(sd_iteration))
    print("af: " + str(fitness_avg) + " sdf: " + str(sd_fitness))
    return [function_name, bees_parameters['stlim'], bees_parameters['ns'], bees_parameters['nb'], bees_parameters['nr'], fitness_avg, sd_fitness, iteration_avg, sd_iteration]
    
def write_csv(file_name, data):
    df = pd.DataFrame({'Benchmark': [data[i][0] for i in range(len(data))],
                        'stlim': [data[i][1] for i in range(len(data))],
                        'ns': [data[i][2] for i in range(len(data))],
                        'nb': [data[i][3] for i in range(len(data))],
                        'nr': [data[i][4] for i in range(len(data))],
                        'af': [data[i][5] for i in range(len(data))],
                        'sdf': [data[i][6] for i in range(len(data))],
                        'ai': [data[i][7] for i in range(len(data))],
                        'sdi': [data[i][8] for i in range(len(data))]})
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    import python_benchmark_functions.benchmark_functions as bf
    test_results = []

    print("Function Ackley")
    b_func = bf.Ackley(n_dimensions=10,opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_ackley = test_on_function("Ackley(10D)", b_func, lb, ub, Ackley_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_ackley)

    print('')
    print("Function Schaffer")
    b_func = bf.Schaffer(opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_schaffer = test_on_function("Schaffer(2D)", b_func, lb, ub, Schaffer_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_schaffer)

    print('')
    print("Function Schwefel")
    b_func = bf.Schwefel(n_dimensions=2,opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_schwefel = test_on_function("Schwefel(2D)", b_func, lb, ub, Schwefel_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_schwefel)

    print('')
    print("Function Easom")
    b_func = bf.Easom(opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_easom = test_on_function("Easom(2D)", b_func, lb, ub, Easom_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_easom)
    
    print('')
    print("Function Goldstein and Price")
    b_func = bf.GoldsteinAndPrice(opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_goldsteinandprice = test_on_function("Goldstein And Price(2D)", b_func, lb, ub, GoldsteinAndPrice_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_goldsteinandprice)

    print('')
    print("Function Rastrigin")
    b_func = bf.Rastrigin(n_dimensions=10, opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_rastrigin = test_on_function("Rastrigin(10D)", b_func, lb, ub, Rastrigin_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_rastrigin)

    print('')
    print("Function Hypersphere")
    b_func = bf.Hypersphere(n_dimensions=10, opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_hypersphere = test_on_function("Hypersphere(10D)", b_func, lb, ub, Hypersphere_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_hypersphere)

    print('')
    print("Function Martin and Gaddy")
    b_func = bf.MartinGaddy(opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    result_of_martingaddy = test_on_function("Martin and Gaddy(2D)", b_func, lb, ub, MartinGaddy_bees_parameters, b_func.getMaximum()[0])
    test_results.append(result_of_martingaddy)

    write_csv("test.csv", test_results)


