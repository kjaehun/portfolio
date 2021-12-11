// Junit tests to test the Dijkstra function in Graph
// 12/09/2021

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.platform.console.ConsoleLauncher;
import java.lang.invoke.MethodHandles;

/**
 * Tests Graph for the implementation of Dijsktra's Shortest Path algorithm.
 */
public class GraphTest {

    private Graph<String> graph;

    /**
     * Instantiate sample graph.
     */
    @BeforeEach
    public void createGraph() {
        graph = new Graph<>();
        // insert vertices A-F
        graph.insertVertex("A");
        graph.insertVertex("B");
        graph.insertVertex("C");
        graph.insertVertex("D");
        graph.insertVertex("E");
        graph.insertVertex("F");

        graph.insertEdge("A","B",6);
        graph.insertEdge("A","C",2);
        graph.insertEdge("A","D",5);
        graph.insertEdge("B","E",1);
        graph.insertEdge("B","C",2);
        graph.insertEdge("C","B",3);
        graph.insertEdge("C","F",1);
        graph.insertEdge("D","E",3);
        graph.insertEdge("E","A",4);
        graph.insertEdge("F","A",1);
        graph.insertEdge("F","D",1);
    }

    /**
     * Checks the distance/total weight cost from the vertex A to F.
     */
    @Test
    public void testPathCostAtoF() {
        assertTrue(graph.getPathCost("A", "F") == 3);
    }

    /**
     * Checks the distance/total weight cost from the vertex A to D.
     */
    @Test
    public void testPathCostAtoD() {
        assertTrue(graph.getPathCost("A", "D") == 4);
    }

    /**
     * Checks the ordered sequence of data within vertices from the vertex 
     * A to D.
     */
    @Test
    public void testPathAtoD() {
        assertTrue(graph.shortestPath("A", "D").toString().equals(
                "[A, C, F, D]"
        ));
    }

    /**
     * Checks the ordered sequence of data within vertices from the vertex 
     * A to F.
     */
    @Test
    public void testPathAtoF() {
        assertTrue(graph.shortestPath("A", "F").toString().equals(
                "[A, C, F]"
        ));
    }

    /**
     * Checks the distance/total weight cost from the vertex D to B.
     */
    @Test
    public void testPathCostDtoB() {
        assertTrue(graph.getPathCost("D", "B") == 12);
    }

    /**
     * Checks the ordered sequence of data within vertices from the vertex
     * D to B.
     */
    @Test
    public void testPathDtoB() {
        assertTrue(graph.shortestPath("D", "B").toString().equals(
                "[D, E, A, C, B]"
        ));
    }

    /**
     * Checks the distance/total weight cost from the vertex B to F.
     */
    @Test
    public void testPathCostBtoF() {
        assertTrue(graph.getPathCost("B", "F") == 3);
    }

    /**
     * Checks the predecessor to vertex B along the shortest
     * path from vertex F to B.
     */
    @Test
    public void testPredecessorFtoB() {
        int index = graph.shortestPath("F", "B").size();
        // .get(index-2) returns second-to-last element, which is the
        // predecessor to vertex B
        assertTrue(graph.shortestPath("F", "B").get(index-2).equals("C"));
    }

    /**
     * Checks the distance/total weight cost from the vertex A to B.
     */
    @Test
    public void testPathCostAtoB() {
        assertTrue(graph.getPathCost("A", "B") == 5);
    }

    /**
     * Checks the ordered sequence of data within vertices from the vertex
     * A to B.
     */
    @Test
    public void testPathAtoB() {
        assertTrue(graph.shortestPath("A", "B").toString().equals(
                "[A, C, B]"
        ));
    }

    /**
     * Checks the distance/total weight cost from the vertex B to A.
     */
    @Test
    public void testPathCostBtoA() {
        assertTrue(graph.getPathCost("B", "A") == 4);
    }

    /**
     * Checks the ordered sequence of data within vertices from the vertex
     * B to A.
     */
    @Test
    public void testPathBtoA() {
        assertTrue(graph.shortestPath("B", "A").toString().equals(
                "[B, C, F, A]"
        ));
    }

    public static void main(String[] args) {
        String className = MethodHandles.lookup().lookupClass().getName();
        String classPath = System.getProperty("java.class.path").replace(" ", "\\ ");
        String[] arguments = new String[] {
                "-cp",
                classPath,
                "--include-classname=.*",
                "--select-class=" + className };
        ConsoleLauncher.main(arguments);
    }

}