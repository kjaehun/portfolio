## A* Search
## 11/15/2021

import numpy as np
import heapq

## calculates the heuristic value of a state
## used the sum of Manhattan distance of each tile to its desired position
##      as the heuristic function
## returns an integer
def calc_h(state):
    sum = 0
    goal = np.append(np.arange(1,9), [0]).reshape(3,3)
    for i in range(1, 9):
        x_g, y_g = np.where(goal == i)
        x_s, y_s = np.where(state == i)
        sum += abs(x_g - x_s)
        sum += abs(y_g - y_s)
    return sum[0]


## returns all possible successors to a given state
## number of successors depends on the position of '0' (blank tile)
## returns a list that has integers 0 to 8 as elements
def return_succ(state):
    s = np.array(state).reshape(3,3)
    x_arr, y_arr = np.where(s == 0)
    x = x_arr[0]
    y = y_arr[0]
    succs = []
    if (x != 0):
        s1 = np.copy(s)
        temp = s[x-1][y]
        s1[x-1][y] = 0
        s1[x][y] = temp
        succs.append(s1.flatten().tolist())
    if (y !=0):
        s2 = np.copy(s)
        temp = s[x][y-1]
        s2[x][y-1] = 0
        s2[x][y] = temp
        succs.append(s2.flatten().tolist())
    if (x != 2):
        s3 = np.copy(s)
        temp = s[x+1][y]
        s3[x+1][y] = 0
        s3[x][y] = temp
        succs.append(s3.flatten().tolist())
    if (y != 2):
        s4 = np.copy(s)
        temp = s[x][y+1]
        s4[x][y+1] = 0
        s4[x][y] = temp
        succs.append(s4.flatten().tolist())
    succs = sorted(succs)
    return succs


## prints the successors of a state
## example output: [1, 2, 0, 4, 5, 3, 6, 7, 8] h=6
def print_succ(state):
    succs = return_succ(state)
    for i in range(len(succs)):
        h = calc_h(np.array(succs[i]).reshape(3,3))
        print(succs[i], "h={}".format(h))


## solves the puzzle and obtains the solution path
## prints the current state, the current h, and the cumulative # of moves so far
## example output: [4, 3, 8, 5, 1, 6, 7, 2, 0] h=10 moves: 0
def solve(state):
    pq = []
    explored = []
    popped = []
    h = calc_h(np.array(state).reshape(3,3))
## used priority queue using heapq
## format of items pushed: (g+h, state, (g, h, parent_index))
## h is obtained using calc_h()
## g represents the # of moves it took to reach the current state, obtained
##      by incrementing the g from the current item by 1
    heapq.heappush(pq, (h, state, (0, h, -1)))
    found = False
    while pq:
        current = heapq.heappop(pq)
        current_state = current[1]
        current_g = current[2][0]
        current_h = current[2][1]
        parent_index = current[2][2]
        explored.append(current_state)
        popped.append(current)
        if current_h == 0:
            found = True
            break;
        succs = return_succ(current_state)
        current_g += 1
        for k in range(len(succs)):
            if succs[k] not in explored: # prevents branching into explored paths
                h = calc_h(np.array(succs[k]).reshape(3,3))
                heapq.heappush(pq, (current_g + h, succs[k], (current_g, h, len(popped) - 1)))
    if found:
        goal = popped[-1]
        p_index = goal[2][2]
        result = []
        result.append((goal[1], goal[2][1]))
        while p_index != -1: # a parent index of -1 denotes the initial state
            cur = popped[p_index]
            result.append((cur[1], cur[2][1])) # (state, h)
            p_index = cur[2][2]
        for i in range(len(result) - 1, -1, -1):
            print(result[i][0], "h={} moves: {}".format(result[i][1], len(result) - i - 1))
    else:
        print("Path not found.")
