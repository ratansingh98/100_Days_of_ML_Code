import pydot
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pylab as pl
import Config


class TreePlot:
    """
    This class creates tree plot for search tree
    """
    
    def __init__(self):
        """
        Constructor
        """
        # create graph object
        self.graph = pydot.Dot( graph_type='graph', dpi = 800)
        
        #index of node
        self.index = 0

    
    def createGraph(self, node, bestMove):
        """
        This method adds nodes and edges to graph object
        Similar to printTree() of Node class
        """
        
        #create html code for the boardValues
        boardValues = node.state.boardValues
        htmlString = "<<table>"
        rows, cols = boardValues.shape
        for i in range(rows):
            htmlString += "<tr>"
            for j in range(cols):
                if boardValues[i, j] == -1:
                    htmlString += "<td bgcolor='#FF0000'>&nbsp;</td>"
                elif boardValues[i, j] == 0:
                    htmlString += "<td bgcolor='#00FF00'>" + Config.moveTexts[0] + \
                                "</td>"
                elif boardValues[i, j] == 1:
                    htmlString += "<td bgcolor='#0000FF'>" + Config.moveTexts[1] + \
                                "</td>"
                
            htmlString += "</tr>"
        htmlString += "</table>>"            
        
        #decide shape based on whether node is at depth 1 and node's move is bestMove
        shape = "plaintext"
        if node.depth == 1 and node.move == bestMove:
            #draw extra border
            shape = "plain"        
            
        #annotate score if leaf or else alpha-beta
        annotation = ""
        if len(node.children) == 0:
            annotation = node.score 
        else:
            annotation = str(node.alpha) + "," + str(node.beta) + "," + str(node.score)
        
        #create node
        parentGraphNode = pydot.Node(str(self.index), shape = shape, 
                                     label = htmlString, xlabel = annotation)
        self.index += 1
        
        #add node
        self.graph.add_node(parentGraphNode)
        
        #call this method for child nodes
        for childNode in node.children:
            childGraphNode = self.createGraph(childNode, bestMove)
            
            #create edge
            edge = pydot.Edge(parentGraphNode, childGraphNode, label = "[" +
                    str(childNode.move.row) + "," + str(childNode.move.col) + "]")
            
            #add edge
            self.graph.add_edge(edge)
            
        return parentGraphNode
        
    
    def generateDiagram(self, rootNode, bestMove):
        """
        This method generates diagram
        """
        #add nodes to edges to graph
        self.createGraph(rootNode, bestMove)
        
        f = pl.figure()
        f.add_subplot(1, 1, 1)  
        # show search tree
        self.graph.write_png('graph.png')
        img = mpimg.imread('graph.png')
        pl.imshow(img)
        pl.axis('tight')
        pl.axis('off')
        
        
        mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        plt.axis('tight')
        plt.axis('off')
        plt.savefig("figure.jpg")
        plt.show()
