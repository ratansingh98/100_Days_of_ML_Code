from State import State
from Node import Node
import CSP
from TreePlot import TreePlot


class BacktrackingSearch():
    """
    This performs backtracking search
    """
    
    def search(self):
        """
        This method performs the search
        """
        #get the initial state
        initialState = State()
        
        #create root node
        rootNode = Node(initialState)
        
        #show the search tree explored so far
        treeplot = TreePlot()
        treeplot.generateDiagram(rootNode, rootNode)
        
        #perform search from root node
        self.performBacktrackSearch(rootNode, rootNode)
        
        rootNode.printTree()
            
    
    def performBacktrackSearch(self, rootNode, node):
        """
        This creates the search tree
        """
        
        print ("-- proc --", node.state.assignment)
        
        #check if we have reached goal state
        if node.state.checkGoalState():
            print ("reached goal state")
            return True
            
        else:
            
            #check if there is a case of early failure
            #if node.state.forwardCheck(): 
            if node.state.arcConsistency():
            
                #find an unassigned variable 
                variable = node.state.selectUnassignedVariable()
                
                #for all values in the domain
                for value in node.state.orderDomainValues():
                    
                    #check if constraints are satisfied
                    if CSP.checkConstraints(node.state.assignment,
                                            variable, value):
                    
                        #create child node
                        childNode = Node(State(node.state.assignment, 
                                               node.state.possibleValues, variable, value))
                    
                        node.addChild(childNode)
                        
                        #show the search tree explored so far
                        treeplot = TreePlot()
                        treeplot.generateDiagram(rootNode, childNode)
                        
                        result = self.performBacktrackSearch(rootNode, childNode)
                        if result == True:
                            return True
            return False        
                        
        
bts = BacktrackingSearch()
bts.search()    