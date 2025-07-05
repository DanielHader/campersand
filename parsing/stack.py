import sys

l = []

prev_size = sys.getsizeof(l)
print(f"initial size of the list is {prev_size} bytes")

for i in range(1000):
    l.append(i)
    curr_size = sys.getsizeof(l)

    if curr_size != prev_size:
        print(f"at {len(l)}, size of list changed to {curr_size} bytes. ratio = ({curr_size / prev_size})")
        prev_size = curr_size

# == RECURSION ==============================================================================================

def is_valid_move(puzzle, row, col, num):
    for x in range(9):
        if puzzle[x][col] == num or puzzle[row][x] == num:
            return False
    
    sub_row = row // 3
    sub_col = col // 3

    for i in range(3):
        for j in range(3):
            if puzzle[sub_row * 3 + i][sub_col * 3 + j] == num:
                return False
   
    return True

def solve_sudoku_recursive(puzzle, index):
    # it's assumed that all positions before index have been filled

    if index == 9*9:
        return True

    row = index // 9
    col = index % 9

    if puzzle[row][col] != 0:
        return solve_sudoku_recursive(puzzle, index + 1)

    for num in range(1, 10):
        if is_valid_move(puzzle, row, col, num):
            puzzle[row][col] = num
            if solve_sudoku_recursive(puzzle, index + 1):
                return True
            puzzle[row][col] = 0
    
    return False

def solve_sudoku(puzzle):
    return solve_sudoku_recursive(puzzle, 0)

def subset_sum_recursive(nums, i, total, target, subset):

    if i >= len(nums):
        if total == target:
            return [subset.copy()]
        else:
            return []

    # if we skip the current number
    subsets1 = subset_sum_recursive(nums, i+1, total, target, subset)

    
    # if we take the current number
    num = nums[i]
    subset.append(num)
    subsets2 = subset_sum_recursive(nums, i+1, total+nums[i], target, subset)
    subset.pop()

    return subsets1 + subsets2

def subset_sum(nums, target):
    return subset_sum_recursive(nums, 0, 0, target, [])

if __name__ == "__main__":
    puzzle = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]

    solve_sudoku(puzzle)

    for row in puzzle:
        print(row)

    pass

    nums = [1, 2, 3, 4, 5, -2, -1]
    subsets = subset_sum(nums, 3)
    for subset in subsets:
        print(subset)