# Snake AI #

There are two sections of this explanation:

1. Snake Path
2. Programming Snake

### Snake Path ###

To generate a random path for the game snake a hamiltonian cycle is used. hamiltonian cycle is a graph path between two
vertices of a graph that visited each vertex exactly once.

There are various ways to create a hamiltonian cycle, but one way is to generate a maze of half the width and half the
height. Then walk the maze by keeping to one side of the walls, eventually the algorithm will close a loop, a cycle.

The result of the algorithm:
![hamiltonian_path_gif.gif](hamiltonian_path_gif.gif)

### Snake ###

