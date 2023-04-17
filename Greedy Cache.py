'''
For this question you will implement "Furthest in the future paging" in cither C, C++, C#, Java, or
Python.
The input will start with a positive integer, giving the number of instances that follow. For each
instance, the first line will be a positive integer, giving the number of pages in the cache. The second
line of the instance will be a positive integer giving the number of page requests. The third and final
line of each instance will be space delimited positive integers which will be the request sequence.
A sample input is the following:
3
2
7
1 2 3 2 3 1 2
4
12
12 3 33 14 12 20 12 3 14 33 12 20
3
15
1 2 3 4 5 1 2 3 4 5 1 2 3 4 5

Sample output:
4
6
9

Note: Some of the test cases are quite large and a naive implementation is likely to timeout. 
'''

def main():
    k = int(input())
    for a in range(k):
        cacheSize = int(input())
        n = int(input())
        cache = []
        fault = 0
        requests = []
        r = input().split()
        future = {}
        for i in range(n):
            m = int(r[i])
            requests.append(m)
            if m not in future:
                future[m] = [i]
            else:
                future[m].append(i)
        for j in range(n):
            if requests[j] not in cache and len(cache) == cacheSize:
                fault += 1
                mx = 0
                cur = None
                for c in cache:
                    if len(future[c]) == 0:
                        cur = c
                        break
                    if future[c][0] >= mx:
                        cur = c
                        mx = future[c][0]
                cache.remove(cur)
                cache.append(requests[j])
            elif requests[j] not in cache:
                fault += 1
                cache.append(requests[j])
            if len(future[requests[j]]) > 0:
                future[requests[j]].pop(0)
        print(fault)

if __name__ == '__main__':
    main()
