"""
Visualization

The positions of best sites and recruits can be seen in diﬀerent colors 
in the plot of each benchmark function so that users can have a more intuitive 
understanding of the running process of the enhanced BA.

Users can choose to manually and automatically control the iteration process of the enhanced BA.

Requirements:
  - numpy
  - matplotlib
Python:
  - 3.7.7
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import enhancedBA

Ackley_bees_parameters = {'ns':30, 'nb':8, 'nr':80, 'stlim':5}
Schaffer_bees_parameters = {'ns':40, 'nb':5, 'nr':100, 'stlim':10}
Schwefel_bees_parameters = {'ns':35, 'nb':8, 'nr':80, 'stlim':10}
Easom_bees_parameters = {'ns':35, 'nb':8, 'nr':80, 'stlim':10}
GoldsteinAndPrice_bees_parameters = {'ns':35, 'nb':10, 'nr':80, 'stlim':10}
Rastrigin_bees_parameters = {'ns':30, 'nb':10, 'nr':80, 'stlim':5}
Hypersphere_bees_parameters = {'ns':35, 'nb':10, 'nr':80, 'stlim':10}
MartinGaddy_bees_parameters = {'ns':30, 'nb':8, 'nr':100, 'stlim':10}

def visualization(function_name, test_function, search_boundaries, bees_parameters, ba_class=enhancedBA.EnhancedBA):
    a = ba_class(test_function, search_boundaries[0], search_boundaries[1], ns=bees_parameters['ns'], nb=bees_parameters['nb'], nr=bees_parameters['nr'], stlim=bees_parameters['stlim'])

    a.keep_bees_trace=True

    x = np.linspace(search_boundaries[0][0], search_boundaries[1][0], 50)
    y = np.linspace(search_boundaries[0][1], search_boundaries[1][1], 50)

    X, Y = np.meshgrid(x, y)
    Z = np.asarray([[-test_function((X[i][j],Y[i][j])) for j in range(len(X[i]))] for i in range(len(X))])
    p_size=(search_boundaries[1][0] - search_boundaries[0][0])*.01
    fig = plt.figure()
    iteration=0
    points=[]
    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none',alpha=.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(30, 35)
    while True:
        iteration+=1
        a.singleIteration()
        fig.canvas.set_window_title("Benchmark Function " + function_name)
        fig.suptitle("Iteration " + str(iteration) + "," + " Best Solution " + str(a.bestSolution.fitness))
        points_x=[]
        points_y=[]
        points_z=[]
        colors=[]
        sizes=[]
        for bs in a.to_save_best_sites:
            points_x+=[bs.position[0]]
            points_y+=[bs.position[1]]
            colors+=['blue']
            sizes+=[p_size*2.0]
        for rs in a.to_save_recruits:
            for r in rs:
                points_x+=[r.position[0]]
                points_y+=[r.position[1]]
                colors+=['purple']
                sizes+=[p_size]
        points_z=[-test_function([points_x[i],points_y[i]]) for i in range(len(points_x))]
        points=ax.scatter(points_x,points_y,points_z,c=colors,s=sizes)
        fig.show()
        plt.pause(1)
        # To manually control the iteration process, please uncomment the following line of code
        # input("Press any key to start next iteration...")
        points.remove()
        
if __name__ == "__main__":
    import python_benchmark_functions.benchmark_functions as bf

    # Uncomment specific code blocks to visualize different benchmark functions.
    b_func = bf.Ackley(n_dimensions=2, opposite=True)
    lb, ub = b_func.getSuggestedBounds()
    visualization("Ackley", b_func, (lb, ub), Ackley_bees_parameters)

    # b_func = bf.Schaffer(opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Schaffer", b_func, (lb, ub), Schaffer_bees_parameters)

    # b_func = bf.Schwefel(n_dimensions=2, opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Schwefel", b_func, (lb, ub), Schwefel_bees_parameters)
    
    # b_func = bf.Easom(opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Easom", b_func, (lb, ub), Easom_bees_parameters)

    # b_func = bf.GoldsteinAndPrice(opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Goldstein & Price", b_func, (lb, ub), GoldsteinAndPrice_bees_parameters)

    # b_func = bf.Rastrigin(opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Rastrigin", b_func, (lb, ub), Rastrigin_bees_parameters)

    # b_func = bf.Hypersphere(opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Hypersphere", b_func, (lb, ub), Hypersphere_bees_parameters)

    # b_func = bf.MartinGaddy(opposite=True)
    # lb, ub = b_func.getSuggestedBounds()
    # visualization("Martin & Gaddy", b_func, (lb, ub), MartinGaddy_bees_parameters)