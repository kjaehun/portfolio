'''
Impiement the optimal algorithm for Weighted Interval Scheduling (for a defnition of the problen. see
tbe sides on Canvas) in either C. Java. or Python. Be efficient and implement it in O(n^2)
time, where n is the number of jobs. We saw this problem previously in HW3, where we saw that
there was no optimal greedy heuristic.
The input will start with an positive integer. giving the number of instances that follow. For each
instance, there will be a positive integer. giving the number of jobs. For each job. there will be a trio of
positive integers i. j and k, where i < j. and i is the start time. j is the end time, and k is the weight.
A sample input is the following:
2
1
1 4 5
3
1 2 1
3 4 2
2 6 4

Sample output:
5
5
'''

import heapq

def main():
    n = int(input())
    for a in range(n):
        k = int(input())
        jobs = []
        result = 0
        for b in range(k):
            job = input().split()
            jobs.append([int(job[0]), int(job[1]), int(job[2])])
        jobs = sorted(jobs, key=lambda x:x[0])
        jobs = sorted(jobs, key=lambda x:x[1])

        m = [0]
        for j in range(k):
            start = jobs[j][0]
            i = None
            for c in range(j,-1,-1):
                if jobs[c][1] <= start:
                    i = c
                    break
            if i != None:
                m.append(max(m[j], m[i+1]+jobs[j][2]))
            else:
                m.append(max(m[j], jobs[j][2]))
        print(m[k])

if __name__ == '__main__':
    main()
