# X-Puzzle
[Project repo](https://github.com/ribal-aladeeb/state-space-search)

## Project
The aim of the project is to implement and analyze various search algorithms
that will solve the X-Puzzle. In this project, we start off by looking at 2x4
puzzle boards. Our job is to solve the boards using Uniform Cost, Greedy Best
First & A* algorithms. Finally, we'll look into scalability options for our
solution to handle bigger boards.

## Requirements
### Using Conda
Make sure you have Conda installed on your machine
```
conda env create --name project1 --file=environment.yml
conda activate project1
```

## Run
In order to run the project, run the following command:
```
python run.py
```

## Output
You can find the output of the algorithms in the `results` folder. Currently, you should find the output for 50 random 2x4 puzzles. In order to see the puzzles, you can find them in `results/random_puzzles.txt`.