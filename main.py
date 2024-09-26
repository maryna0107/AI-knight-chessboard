import time
import psutil

move_counter = 0
over_10m_printed = False
memory_counter = 0


def stay_in_matrix(x_cur, y_cur, mtrx_size):  # checks if entered start coordinates fit the entered matrix size
    if 0 <= x_cur < mtrx_size and 0 <= y_cur < mtrx_size:
        return True


def knight_moves(chessboard, x_cur, y_cur, counter, mtrx_size, start_time):
    global move_counter, over_10m_printed, memory_counter
    if move_counter > 10000000 and not over_10m_printed:  # check move limit
        print("Moves limit of 10M moves is reached")
        over_10m_printed = True
        return False
    else:
        move_counter += 1  # increment the move counter

    if counter == mtrx_size * mtrx_size:  # Check if the counter has reached the maximum number of moves
        for row in range(mtrx_size):
            for cell in range(mtrx_size):
                if chessboard[row][cell] == -1:
                    chessboard[row][cell] = mtrx_size * mtrx_size
        print(f"Moves counter: {move_counter}")

        return True

    if time.time() - start_time > max_time:
        return False

    chessboard[x_cur][y_cur] = counter

    moves = [  # set of available knight`s moves
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (2, -1), (1, -2)
    ]

    for x, y in moves:
        new_x, new_y = x_cur + x, y_cur + y  # calculate the new coordinates after the move
        if move_counter > 10000000 and not over_10m_printed:
            print("Moves limit of 10M moves is reached")
            over_10m_printed = True
            return False
        else:
            move_counter += 1
            if stay_in_matrix(new_x, new_y, mtrx_size) and chessboard[new_x][new_y] == -1:
                # checking if a move is within the chessboard and the cell are not visited

                if knight_moves(chessboard, new_x, new_y, counter + 1, mtrx_size, start_time):
                    return True

    chessboard[x_cur][y_cur] = -1
    return False


def knight_tour(mtrx_size, start_x, start_y):  # printing out the results
    chessboard = [[-1 for _ in range(mtrx_size)] for _ in range(mtrx_size)]

    start_time = time.time()
    memory_start = psutil.virtual_memory().used

    chessboard[start_x][start_y] = 0

    if over_10m_printed:
        print("Not a successful tour or the time limit is over \U0001F614")
    if knight_moves(chessboard, start_x, start_y, 1, mtrx_size, start_time):
        memory_end = psutil.virtual_memory().used
        memory_consumption = memory_end - memory_start
        if memory_consumption < 0:
            memory_consumption = memory_consumption*(-1)
        print(f"Memory usage (bytes): {memory_consumption}")
        end_time = time.time()
        execution_time = end_time - start_time
        print("Success! \U0001F44D")
        print(f"Execution time in seconds: {execution_time: .5f}")
        tour(chessboard)
        return execution_time
    else:
        print("Not a successful tour or the time limit is over \U0001F614")


def tour(chessboard):  # printing out the chessboard
    for row in chessboard:
        for cell in row:
            print(f'{cell:2}', end=' ')
        print()


if __name__ == "__main__":

    matrix_size = int(input("Enter the size of the chessboard: "))
    max_time = int(input("Enter execution time limit in seconds: "))
    start_x = int(input(f"Enter x: (0-{matrix_size - 1}): "))
    start_y = int(input(f"Enter y: (0-{matrix_size - 1}): "))

    if 0 <= start_x < matrix_size and 0 <= start_y < matrix_size:
        execution_time = knight_tour(matrix_size, start_x, start_y)
    else:
        print("Invalid starting position.")
