# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem:SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    #Memory initialization
    fringe = util.Stack() #initialize a LIFO queue (Stack) for fringes
    discovered = {} #dictionary for checking if a node has been in the set

    #Default/initial state
    state = problem.getStartState() #get initiali/starting state of the game    
    fringe.push((state, [])) #push initial state to fringe

    #Run DFS
    while(fringe.isEmpty() is False):
        state, directions = fringe.pop() #retrieves last state and directions on the fringe
        if(problem.isGoalState(state)):#has found a goal state?
            return directions #proper action path
        if(state not in discovered):
            discovered[state] = True
            transition = list(zip(*problem.getSuccessors(state))) #stack vertically
            next_state, direction, _  = transition if len(transition) >= 1 else ([], [], [])
            for s, d in zip(next_state, direction):
                fringe.push((s, [*directions, d])) #squeeze original directions list with new direction

    return [] #couldn't find a solution

      
        
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #Memory initialization
    fringe = util.Queue() #initialize a FIFO queue for fringes
    discovered = {} #dictionary for checking if a node has been in the set

    #Default/initial state
    state = problem.getStartState() #get initial/starting state of the game  
    fringe.push((state, [])) #push initial state to fringe

    #mark initial state as visited
    discovered[state] = True
    #Run BFS
    while(not fringe.isEmpty()):
        state, directions = fringe.pop() #retrieves last state and directions on the fringe
        if(problem.isGoalState(state)):#has found a goal state?
            return directions #proper action path
        
        transition = list(zip(*problem.getSuccessors(state))) #stack vertically
        next_state, direction, _  = transition if len(transition) >= 1 else ([], [], []) #check for none
        for s, d in zip(next_state, direction):
            if(s not in discovered):
                fringe.push((s, [*directions, d])) #squeeze original directions list with new direction
                discovered[s] = True

    return [] #couldn't find a solution

def uniformCostSearch(problem:SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #Memory initialization
    fringe = util.PriorityQueue()
    discovered = {}

    #Initial/stating state
    state = problem.getStartState() #get initial/starting state of the game
    fringe.push((state, []), 0)

    #mark initial state as visited
    discovered[state] = 0

    #Run UCS
    while(not fringe.isEmpty()):
        state, directions = fringe.pop() #retrieves last state and directions on the fringe

        if(problem.isGoalState(state)):#has found a goal state?
            return directions #proper action path
        
        transition = list(zip(*problem.getSuccessors(state))) #stack vertically
        next_state, direction, _  = transition if len(transition) >= 1 else ([], [], None) #check for none
        
        for s, d in zip(next_state, direction):
            actions = [*directions, d]
            priority = problem.getCostOfActions(actions) #store priority for Heap
            
            #If path already found, check if that path has a lower priority.
            #if not, append the new path to the queue so that'll be popped first.
            if(s in discovered and discovered[s] > priority):
                fringe.update((s, actions), priority)

            #New path found in search. append to Queue and mark it as discovered.
            if(s not in discovered):
                fringe.push((s, actions), priority) #squeeze original directions list with new direction
                discovered[s] = priority
    return [] #couldn't find a solution

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem:SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #Memory initialization
    fringe = util.PriorityQueue()
    discovered = {}

    #Initial/stating state
    state = problem.getStartState() #get initial/starting state of the game
    fringe.push((state, []), 0)

    #mark initial state as visited
    discovered[state] = 0

    #Run A*
    while(not fringe.isEmpty()):
        state, directions = fringe.pop() #retrieves last state and directions on the fringe

        if(problem.isGoalState(state)):#has found a goal state?
            return directions #proper action path
        
        transition = list(zip(*problem.getSuccessors(state))) #stack vertically
        next_state, direction, _  = transition if len(transition) >= 1 else ([], [], None) #check for none
        
        for s, d in zip(next_state, direction):
            actions = [*directions, d]
            priority = problem.getCostOfActions(actions) + heuristic(s, problem) #store priority for heap

            # If path already found, check if that path has a lower priority.
            # if not, append the new path to the queue so that'll be popped first.
            if(s in discovered and discovered[s] > priority):
                fringe.update((s, actions), priority)

            # New path found in search. append to Queue and mark it as discovered.
            if(s not in discovered):
                fringe.push((s, actions), priority) #squeeze original directions list with new direction
                discovered[s] = priority
    return [] #couldn't find a solution

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
