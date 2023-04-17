'''
Implement the optimal algorithm for inversion counting in either C, C++, C#, Java. or Python. Be
eficient and implement it in O(n log n) time, where n is the number of elements in the ranking,
The input will start with a positive integer, giving the number of instances that follow. For each
instance, there will be a positive integer, giving the number of elenments in the ranking. A sample input
is the following:
2
5
5 4 3 2 1
4
1 5 9 8

Sample output:
10
1
'''

from math import floor

def main():
    n = int(input())
    for i in range(n):
        numOfInts = int(input())
        ints = input().split()
        for j in range(len(ints)):
            ints[j] = int(ints[j])
        (a,c) = countsort(ints)
        print(c)

def countsort(a):
    if len(a) == 1:
        return (a,0)
    (a1,c1) = countsort(a[:floor(len(a)/2)])
    (a2,c2) = countsort(a[floor(len(a)/2):])
    (a,c) = mergecount(a1,a2)
    return (a, c+c1+c2)

def mergecount(a, b):
    s = []
    c = 0
    while len(a) != 0 or len(b) != 0:
        if len(a) == 0:
            s.append(b.pop(0))
            continue
        if len(b) == 0:
            s.append(a.pop(0))
            continue
        mn = min(a[0], b[0])
        if mn in b and mn not in a:
            s.append(b.pop(0))
            c += len(a)
        else:
            s.append(a.pop(0))
    return (s,c)

if __name__ == '__main__':
    main()
