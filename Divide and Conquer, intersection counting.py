'''
Implement a solution in either C, C+ +, C#, Java, or Python to the following problem.
Suppose you are given two sets of n points, one set {p1,p2, ...,pn} on the line y = 0 and the other
set {q1, q2, ..., qn} on the line y = 1. Create a set of n line segments by connecting each point pi to
the corresponding point qi. Your goal is to develop an algorithm to determine how many pairs of these
line segments intersect. Your algorithm should take the 2n points us input, and return the number
of intersections. Using divide-and-conquer, you should be able to develop an algorithm that runs in
O(n log n) time.
Hint: What does this problem have in common with the problem of counting inversions in a list?
Input should be read in from stdin. The first line will be the number of instances. For each instane,
the first line will contain the umber of pairs of points (n). The next n lines each contain the location
of a point g on the top line. Followed by the final n lines of the instance each containing the location

Sample input:
2
4
1
10
8
6
6
2
5
1
5
9
21
1
5
18
2
4
6
10
1

Sample output:
4
7
'''

from math import floor

def main():
    n = int(input())
    for i in range(n):
        numOfPoints = int(input())
        q = []
        pair = []
        for j in range(numOfPoints):
            q.append(int(input()))
        for j in range(numOfPoints):
            pair.append((q[j], int(input())))
        pair.sort(key=lambda k:k[0])
        (p,c) = intersect(pair)
        print(c)

def intersect(pair):
    if len(pair) == 1:
        return (pair, 0)
    (p1, c1) = intersect(pair[:floor(len(pair)/2)])
    (p2, c2) = intersect(pair[floor(len(pair)/2):])
    (pair, c) = merge(p1, p2)
    return (pair, c+c1+c2)

def merge(a, b):
    c = 0
    s = []
    while len(a) != 0 or len(b) != 0:
        if len(a) == 0:
            s.append(b.pop(0))
            continue
        if len(b) == 0:
            s.append(a.pop(0))
            continue
        mn = min(a[0], b[0], key=lambda k: k[1])
        if mn in b and mn not in a:
            s.append(b.pop(0))
            c += len(a)
        else:
            s.append(a.pop(0))
    return (s,c)

if __name__ == '__main__':
    main()
