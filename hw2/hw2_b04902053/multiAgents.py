# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodPos = [(i,j)
                   for i,col in enumerate(newFood)
                   for j,row in enumerate(col) if row]
        foodDis = [manhattanDistance(newPos, pos)
                   for pos in foodPos]
        foodDis.sort()
        foodScore = min(foodDis) if len(foodDis) != 0 else 0
        # foodScore = - foodScore - 20*len(foodPos)
        foodScore = - 2*foodScore - 40*len(foodPos)

        ghostPos = [state.getPosition()
                    for state in newGhostStates]
        ghostDis = [manhattanDistance(newPos, pos)
                    for pos in ghostPos]
        ghostDis.sort()
        ghostScore = min(ghostDis) if len(ghostDis) != 0 else 0
        ghostScore = 100 if ghostScore > 2 else ghostScore

        score = foodScore + ghostScore

        # please change the return score as the score you want
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        INFINITY = 1e300

        def min_value(state, depth, agent):
            """The min value ghost can choose.
                return: a utility value
            """
            actions = state.getLegalActions(agent)
            if len(actions) == 0:
                return self.evaluationFunction(state)
            value = INFINITY
            for a in actions:
                if agent == state.getNumAgents() - 1:
                    if depth == self.depth:
                        value = min(value, self.evaluationFunction(state.generateSuccessor(agent, a)))
                    else:
                        value = min(value, max_value(state.generateSuccessor(agent, a), depth+1))
                else:
                    value = min(value, min_value(state.generateSuccessor(agent, a), depth, agent+1))
            return value

        def max_value(state, depth, ret_action=False):
            """The max value pacman can choose.
                return: a utility value or an action
            """
            actions = state.getLegalActions(0)
            if len(actions) == 0:
                return self.evaluationFunction(state)
            action = 0
            value = - INFINITY
            for a in actions:
                new_value = min_value(state.generateSuccessor(0, a), depth, 1)
                if value < new_value:
                    action = a
                    value = new_value
            if ret_action:
                return action
            else:
                return value

        return max_value(gameState, 1, ret_action=True)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        INFINITY = 1e300

        def min_value(state, depth, agent, alpha, beta):
            """The min value ghost can choose.
                return: a utility value
            """
            actions = state.getLegalActions(agent)
            if len(actions) == 0:
                return self.evaluationFunction(state)
            value = INFINITY
            for a in actions:
                if agent == state.getNumAgents() - 1:
                    if depth == self.depth:
                        value = min(value, self.evaluationFunction(state.generateSuccessor(agent, a)))
                    else:
                        value = min(value, max_value(state.generateSuccessor(agent, a), depth+1, alpha, beta))
                else:
                    value = min(value, min_value(state.generateSuccessor(agent, a), depth, agent+1, alpha, beta))
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_value(state, depth, alpha, beta, ret_action=False):
            """The max value pacman can choose.
                return: a utility value or an action
            """
            actions = state.getLegalActions(0)
            if len(actions) == 0:
                return self.evaluationFunction(state)
            action = 0
            value = - INFINITY
            for a in actions:
                new_value = min_value(state.generateSuccessor(0, a), depth, 1, alpha, beta)
                if value < new_value:
                    action = a
                    value = new_value
                if value > beta:
                    return value
                alpha = max(alpha, value)
            if ret_action:
                return action
            else:
                return value

        return max_value(gameState, 1, - INFINITY, INFINITY, ret_action=True)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        INFINITY = 1e300

        def mean(nums):
            """The mean of a list, and it will deal with integer-truncate problem."""
            return float(sum(nums)) / max(len(nums), 1)

        def avg_value(state, depth, agent):
            """The average value ghosts choose.
                return: a utility value
            """
            actions = state.getLegalActions(agent)
            if len(actions) == 0:
                return self.evaluationFunction(state)
            values = []
            for a in actions:
                if agent == state.getNumAgents() - 1:
                    if depth == self.depth:
                        values += [self.evaluationFunction(state.generateSuccessor(agent, a))]
                    else:
                        values += [max_value(state.generateSuccessor(agent, a), depth+1)]
                else:
                    values += [avg_value(state.generateSuccessor(agent, a), depth, agent+1)]
            return mean(values)

        def max_value(state, depth, ret_action=False):
            """The max value pacman can choose.
                return: a utility value or an action
            """
            actions = state.getLegalActions(0)
            if len(actions) == 0:
                return self.evaluationFunction(state)
            action = 0
            value = - INFINITY
            for a in actions:
                new_value = avg_value(state.generateSuccessor(0, a), depth, 1)
                if value < new_value:
                    action = a
                    value = new_value
            if ret_action:
                return action
            else:
                return value

        return max_value(gameState, 1, ret_action=True)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

