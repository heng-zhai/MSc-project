# Enhanced Bees Algorithm

This repository contains the complete python code of MSc summer project.

**Python environment**: 3.7.7

**Required libraries**: numpy, matplotlib, pandas

This project is based on the [original python code of the standard bees algorithm](https://gitlab.com/bees-algorithm/bees_algorithm_python) to modify and use the provided benchmark functions for algorithm performance testing. To get more information about optimisation test functions and datasets, please visit [this website](https://www.sfu.ca/~ssurjano/optimization.html).

One of the main reasons for modifying the bees algorithm is the excessive number of parameters of standard bees algorithm which has always hindered the wider application of the bees algorithm. The initialization of parameters highly depends on the researchers' existing knowledge and experience, and researchers who do not understand the algorithm or the target problem itself cannot set the algorithm to get the best performance. In most cases, the parameter tuning is a huge and time-consuming work for users, and this should not have been spent by the user. Ideally, the users just need to provide a limited number of basic parameters or even don't have to provide any parameters and this algorithm has the ability to perform adaptive analysis according to different complex problems to automatically adjust internal computation.

## Standard bees algorithm parameters

- Number of scout bees(ns)
- Number of elite sites(ne)
- Number of best sites(nb)
- Recruited bees for elite sites(nre)
- Recruited bees for remaining best sites(nrb)
- Initial size of neighbourhood(ngh)
- Limit of stagnation cycles for site abandonment(stlim)

## Enhanced bees algorithm parameters

- Number of scout bees(ns)
- Number of best sites or flower patches(nb)
- Total number of recruits in hive(nr)
- Initial size of neighbourhood(ngh)
- Limit of stagnation cycles for site abandonment(stlim)

Because the process of neighbourhood shrinking and site abandonment have been widely used in the standard bees algorithm and have shown very good performance, parameters ngh and stlim are retained in enhanced bees algorithm.

## Contents of the repository

This git repository contains a main python file for the implementation of enhanced bees algorithm, a folder belonging to the benchmark functions (*provided by supervisor*), a txt file for pseudo code, a README markdown file, a python file for testing (*pandas* library required), a python file for visualization (*numpy*, *matplotlib* libraries required), a jupyter notebook for usage (*matplotlib* library required) and a csv file for storing the results of testing.

## Usage

- To run the usage sample, run the *Usage.ipynb* file directly.
- To apply the enhanced bees algorithm to actual problem, modify the objective function, search boundaries, default parameter settings and stop criteria manually in *Usage.ipynb* file according to the actual problem.
- To test the performance of the enhanced BA on provided benchmark functions, run the *testing.py* file.
- To visualize the benchmark functions and view the search process of enhanced BA, run the *visualization.py* file.

All the below steps can be run in *Usage.ipynb* at once, and the objective function, search boundaries, default parameter settings, stop criteria can be modified manually according to the actual problem.

1. Import the library
2. Define the objective function
3. Provide the search boundaries (lower boundaries and upper boundaries)
4. Create an instance of the enhanced BA
5. Perform a single iteration by using singleIteration() method
6. Perform the search all at once by using stoppingCriterion() method
7. Get the fitness and position of best solution
8. View the fitness curve to know how the best solution changes after each iteration
