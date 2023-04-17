'''
Implement the optimal algorithm for interval scheduling (see Greedy slides).
Be efficient and implement it in O(n log n) time, where n is the number of jobs.
The input will start with a positive integer, giving the number of instances that follow.
For each instance, there will be a positive integer, giving the number of job.
For each job, there will be a pair of positive integers i and j, where i < j,
and i is the start time and j is the end time.
A sample input is the following:

2
1
1 4
3
1 2
3 4
2 6

Sample output:
1
2
'''

import heapq

def main():
    n = int(input())
    for i in range(n):
        k = int(input())
        pq = []
        result = 0
        for j in range(k):
            job = input().split()
            heapq.heappush(pq, (int(job[1]), int(job[0])))
        while (len(pq) > 0):
            cur = heapq.heappop(pq)
            result += 1
            while (len(pq) > 0 and cur[0] > pq[0][1]):
                heapq.heappop(pq)
        print(result)

if __name__ == '__main__':
    main()
