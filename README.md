# X-Puzzle
[Project repo](https://github.com/ribal-aladeeb/state-space-search)

## Project
The aim of the project is to implement and analyze various search algorithms
that will solve the X-Puzzle. In this project, we start off by looking at 2x4
puzzle boards. Our job is to solve the boards using Uniform Cost, Greedy Best
First & A* algorithms. Finally, we'll look into scalability options for our
solution to handle bigger boards.

## Setting the environment
### Using Conda
Make sure you have Conda installed on your machine
```
conda env create --name 472 --file=environment.yml
conda activate 472
```
I you don't have conda, pip install the modules listed in environment.yml


## Running search algorithms
In order to run the project, run the following command:
```
python run.py
```
You will see a prompt that asks you to either [1] provide an input file [2]
Generate random puzzle. The run script will generate a results/ folder that will
contain the solution path and search path of every puzzle-algorithm-heuristic
combination. It will also generate an analysis.txt summary of the results in the
root of the project. If you choose option [2], the random puzzles will be save
in random_puzzles.txt in the root of the project

## Navigating the code
board.py contains a Board class which represents a game of 8-puzzle. It also
contains all the methods for manipulating a board and modifying its state.

node.py contains a Node class which represents a node in a state-space search
algorithm. It contains a board along with other state and behavior useful for
searching.

search.py contains the bulk of the search logic along with a small main function
to run a small test case.

heuristics.py contains the heuristic functions

## Analysis of heuristics

In [analysis.ipynb](https://github.com/ribal-aladeeb/state-space-search/blob/main/analysis.ipynb) You can find an insightful analysis of the heuristic functions implemented. Some were taken from the textbook and some others we came up with (although I'm sure we are not the first to do so). We discuss an empirical approach to analysing properties of heuristic functions. You can also see how this implementation handles larger puzzles in this [notebook](https://github.com/ribal-aladeeb/state-space-search/blob/main/scaling_up.ipynb).
