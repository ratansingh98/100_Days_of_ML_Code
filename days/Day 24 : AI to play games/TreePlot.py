'''
@author: Devangini Patel
'''

import pydotplus
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pylab as pl
import CSP


class TreePlot:
    """
    This class creates tree plot for search tree
    """
    
    def __init__(self):
        """
        Constructor
        """
        # create graph object
        self.graph = pydotplus.Dot( graph_type='graph', dpi = 800)
        
        #index of node
        self.index = 0

    
    def createGraph(self, node, currentNode):
        """
        This method adds nodes and edges to graph object
        Similar to printTree() of Node class
        """
           
        #create html code for the node
        image = node.state.drawState()
        htmlString = "<<table>"
        rows, cols, _ = image.shape
        for i in range(rows):
            htmlString += "<tr>"
            for j in range(cols):
                if image[i, j, 0] == 255:
                    htmlString += "<td bgcolor='#FF0000'>&nbsp;</td>"
                elif image[i, j, 1] == 255:
                    htmlString += "<td bgcolor='#00FF00'>&nbsp;</td>"
                elif image[i, j, 2] == 255:
                    htmlString += "<td bgcolor='#0000FF'>&nbsp;</td>"
                else:
                    htmlString += "<td bgcolor='#000000'>&nbsp;</td>"
            htmlString += "</tr>"
        htmlString += "</table>>"            
        
            
        #create node
        parentGraphNode = pydotplus.Node(str(self.index), shape = "plaintext" , label = htmlString)
        self.index += 1
        
        #add node
        self.graph.add_node(parentGraphNode)
        
        #call this method for child nodes
        for childNode in node.children:
            childGraphNode = self.createGraph(childNode, currentNode)
            
            #create edge
            edge = pydotplus.Edge(parentGraphNode, childGraphNode)
            
            #add edge
            self.graph.add_edge(edge)
            
        return parentGraphNode
        
    
    def generateDiagram(self, rootNode, currentNode):
        """
        This method generates diagram
        """
        #add nodes to edges to graph
        self.createGraph(rootNode, currentNode)
        
        #show the diagram
        self.graph.write_png('graph.png')
        img = mpimg.imread('graph.png')
        
        
        f = pl.figure()
        #draw search tree
        f.add_subplot(1, 3, 1)  
        pl.imshow(img)
        pl.axis('tight')
        pl.axis('off')
        #draw state
        f.add_subplot(1, 3, 2)  
        pl.imshow(currentNode.state.drawState())
        pl.axis('tight')
        pl.axis('off')
        #draw possible values
        ax = f.add_subplot(1, 3, 3)  
        pl.imshow(currentNode.state.drawPossibleValues())
        ax.set_yticks(range(len(CSP.variables)))
        ax.set_yticklabels(CSP.variables)
        
        pl.axis('tight')
        pl.axis('off')
        mng = plt.get_current_fig_manager()
        #mng.window.state('zoomed')
        plt.axis('tight')
        plt.axis('off')
        plt.show()
