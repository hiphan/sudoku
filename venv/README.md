9 by 9 Sudoku Solver:  
The Python program is able to solve most of the sudoku problems at different levels of difficulty almost instantly. First, it runs the arc-consistency 
algorithm to reduce the domain of each position on the board. Easy sudoku boards can be solved after this step. For harder ones, which arc-consistency can't give additional assignments,
the program runs a backtracking search using the minimum-remaining-values (MRV) heuristic.  
How to run:
python sudoku.py txt_file  
Examples of txt_file are included (with indication of difficulty). More boards can be found at: https://www.websudoku.com/