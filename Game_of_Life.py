# Program to implement Conway's Game of Life

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class GameOfLife:
    @staticmethod
    def Start():
        # Initializing the values of Grid
        Alive = 255
        Dead = 0
        values = [Alive, Dead]

        def randomGrid(N):
            """returns a grid of NxN random values"""
            return np.random.choice(values, N * N, p=[0.2, 0.8]).reshape(N, N)

        def addGlider(i, j, grid):
            """adds a glider with top left cell at (i, j)"""
            glider = np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]])
            grid[i:i + 3, j:j + 3] = glider

        def addGliderGun(i, j, grid):
            """adds a Glider Gun with top left cell at (i, j)"""
            gun = np.zeros(11 * 38).reshape(11, 38)

            gun[5][1] = gun[5][2] = 1
            gun[6][1] = gun[6][2] = 1

            gun[3][13] = gun[3][14] = 1
            gun[4][12] = gun[4][16] = 1
            gun[5][11] = gun[5][17] = 1
            gun[6][11] = gun[6][15] = 1

            gun[6][17] = gun[6][18] = 1
            gun[7][11] = gun[7][17] = 1
            gun[8][12] = gun[8][16] = 1
            gun[9][13] = gun[9][14] = 1

            gun[1][25] = 1
            gun[2][23] = gun[2][25] = 1
            gun[3][21] = gun[3][22] = 1
            gun[4][21] = gun[4][22] = 1
            gun[5][21] = gun[5][22] = 1
            gun[6][23] = gun[6][25] = 1
            gun[7][25] = 1

            gun[3][35] = gun[3][36] = 1
            gun[4][35] = gun[4][36] = 1

            grid[i:i + 11, j:j + 38] = gun

        def update(frameNum, img, grid, N):
            newGrid = grid.copy()
            for i in range(N):
                for j in range(N):
                    total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                                 grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                                 grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                                 grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

                    # applying Conway's rules
                    if grid[i, j] == Alive:
                        if (total < 2) or (total > 3):
                            newGrid[i, j] = Dead
                    else:
                        if total == 3:
                            newGrid[i, j] = Alive

            # update data
            img.set_data(newGrid)
            grid[:] = newGrid[:]
            return img,

        def main():
            parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

            # add arguments
            parser.add_argument('--grid-size', dest='N', required=False)
            parser.add_argument('--mov-file', dest='movfile', required=False)
            parser.add_argument('--interval', dest='interval', required=False)
            parser.add_argument('--glider', action='store_true', required=False)
            parser.add_argument('--gosper', action='store_true', required=False)
            args = parser.parse_args()

            # set grid size
            N = 100
            if args.N and int(args.N) > 8:
                N = int(args.N)

            # set animation update interval
            updateInterval = 50
            if args.interval:
                updateInterval = int(args.interval)

            if args.glider:
                grid = np.zeros(N * N).reshape(N, N)
                addGlider(1, 1, grid)
            elif args.gosper:
                grid = np.zeros(N * N).reshape(N, N)
                addGliderGun(10, 10, grid)

            else:
                grid = randomGrid(N)

            # set up animation
            fig, ax = plt.subplots()
            img = ax.imshow(grid, interpolation='nearest')
            ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,), frames=10, interval=updateInterval,
                                          save_count=50)
            plt.show()

        main()


a = GameOfLife()
a.Start()
"""
If we hover the mouse over cells, we can uniquely identify the cells by there positions, and their status, 0 for dead 
and 255 for Alive
"""