'''
Implement depth first search in either C, C++, C#, Java, or Python. Be efficient and implement itin
O(n + m) time, where n is the number of graph nodes, and m is the number of graph edges. Remember
to submit a makefile along with your code, just as with week 1's coding question.
Input format: the input will start with a positive integer, giving the number of instances that follow.
For each instance, there will be a positive integer, giving the number of graph nodes. For each node there
will be a line of space-delimited input. The first string in a line will be the node name. Al following
strings in a line will be the names of the adjacent nodes to the first node in the line.
You can asume the order the nodes will be listed is in increasing lexogaphic order (0-9, then A-Z, then
a-z), both in each list of adjacent nodes, as well as the order nodes' lines are listed.
A sample input is the following:
2
3
A B
B A
C
9
1 2 9
2 3 5 6
3 2 7
4 6
5 3
6 2 4
7 3
8 9
9 1 8

Sample output:
ABC
1 2 3 7 5 6 4 9 8
'''

def main():
    n = int(input())
    for i in range(n):
        k = int(input())
        adjList = {}
        nodes = []
        for j in range(k):
            adj = input().split()
            nodes.append(adj[0])
            if len(adj) > 1:
                adjList[adj[0]] = adj[1:]
            else:
                adjList[adj[0]] = []
        result = [nodes[0]]
        dfs(nodes[0], adjList, result)
        for a in range(len(nodes)):
            if nodes[a] not in result:
                result.append(nodes[a])
                dfs(nodes[a], adjList, result)
        for b in range(len(result) - 1):
            print(result[b], end=" ")
        print(result[-1])

def dfs(curNode, adjList, visited):
    for i in range(len(adjList[curNode])):
        if adjList[curNode][i] not in visited:
            visited.append(adjList[curNode][i])
            dfs(adjList[curNode][i],adjList,visited)


if __name__ == '__main__':
    main()
