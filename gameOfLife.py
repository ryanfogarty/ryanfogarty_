from mpi4py import MPI


def print_grid(matrix):
    for i in matrix:
        print(i)
    print()


def set_grid(x, y):
    empty_grid = []
    for i in range(x):
        empty_grid.append([0] * y)
    return empty_grid
x, y = 5, 5

#new_grid = set_grid(x, y)


    # y,x

"""grid[0][2] = 1
grid[1][2] = 1
grid[2][2] = 1
grid[3][2] = 1
grid[4][2] = 1
grid[2][0] = 1
grid[2][1] = 1
grid[2][3] = 1
grid[2][4] = 1
grid[1][1] = 1
grid[1][3] = 1
grid[3][2] = 1
grid[3][3] = 1
"""
"""grid[0][3] = 1
grid[0][2] = 1
grid[1][2] = 1"""


def worker(max_x, max_y, x, y):
    tmp = x
    x = y
    y = tmp
    small_grid = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]
    small_grid[1][1] = grid[y][x]
    if 0 < x < max_x - 1 and 0 < y < max_y - 1:
        small_grid[0] = grid[y-1][x - 1:x + 2]
        small_grid[1][0] = grid[y][x - 1]
        small_grid[1][2] = grid[y][x + 1]
        small_grid[2] = grid[y+1][x - 1:x + 2]
    elif 0 < x < max_x - 1 and y == 0:
        small_grid[0] = ['', '', '']
        small_grid[1][0] = grid[y][x - 1]
        small_grid[1][2] = grid[y][x + 1]
        small_grid[2] = grid[y + 1][x - 1:x + 2]
    elif 0 < x < max_x - 1 and y == max_y - 1:
        small_grid[0] = grid[y - 1][x - 1:x + 2]
        small_grid[1][0] = grid[y][x - 1]
        small_grid[1][2] = grid[y][x + 1]
        small_grid[2] = ['', '', '']
    elif x == 0 and 0 < y < max_y - 1:
        small_grid[0] = [''] + grid[y - 1][x:x + 2]
        small_grid[1][0] = ''
        small_grid[1][2] = grid[y][x + 1]
        small_grid[2] = [''] + grid[y + 1][:x + 2]
    elif x == max_x - 1 and 0 < y < max_y - 1:
        small_grid[0] = grid[y - 1][x - 1:x + 1] + ['']
        small_grid[1][0] = grid[y][x - 1]
        small_grid[1][2] = ''
        small_grid[2] = grid[y + 1][x - 1:x + 1] + ['']
    elif x == 0 and y == 0:
        small_grid[0] = ['', '', '']
        small_grid[1][0] = ''
        small_grid[1][2] = grid[y][x + 1]
        small_grid[2] = [''] + grid[y + 1][x:x + 2]
    elif x == 0 and y == max_y-1:
        small_grid[0] = [''] + grid[y-1][x:x + 2]
        small_grid[1][0] = ''
        small_grid[1][2] = grid[y][x + 1]
        small_grid[2] = ['', '', '']
    elif x == max_x - 1 and y == 0:
        small_grid[0] = ['', '', '']
        small_grid[1][0] = grid[y][x - 1]
        small_grid[1][2] = ''
        small_grid[2] = grid[y + 1][x-1:x + 1] + ['']
    elif x == max_x - 1 and y == max_y-1:
        small_grid[0] = grid[y - 1][x - 1:x + 1] + ['']
        small_grid[1][0] = grid[y][x - 1]
        small_grid[1][2] = ''
        small_grid[2] = ['', '', '']

    count = [row.count(1) for row in small_grid]
    result = sum(count)
    if small_grid[1][1] == 1:
        result -= 1
    cell = grid[y][x]
    if result < 2 or result > 3:
        cell = 0
    elif result == 3:
        cell = 1
    return cell

#for i in range(10):
#if i == 0:
grid = set_grid(x, y)
grid[0][2] = 1
grid[1][2] = 1
grid[2][2] = 1
grid[3][2] = 1
grid[4][2] = 1
max_x = x
max_y = y
x_pos = 0
y_pos = 0
data = [max_x, max_y, x_pos, y_pos, grid]
cells = x * y
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank == 0:
    print_grid(data[4])
    comm.send(data, dest=1)
    data = comm.recv(source=(size - 1))
    print_grid(data[4])

for i in range(1, size):
    if rank == i:
        data = comm.recv(source=(i - 1))
        new_grid2 = data[4]
        new_grid2[data[2]][data[3]] = worker( data[0], data[1], data[2], data[3])
        if data[2] < max_x - 1:
            data[2] += 1
        else:
            data[2] = 0
            data[3] += 1
        comm.send(data, dest=(i + 1)%size)
        if i == max_x * max_y - 1:
            grid = new_grid2
            print("test1")
"""for z in range(10):
    for i in range(0, x):
        for j in range(0, y):
            new_grid[i][j] = worker(x, y, i, j)
    print_grid(new_grid)
    grid = new_grid
    new_grid = set_grid(x, y)"""