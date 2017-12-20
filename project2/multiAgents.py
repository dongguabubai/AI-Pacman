# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    if 'Stop' in legalMoves:
      legalMoves.pop(legalMoves.index('Stop'))
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
    curFoodList = currentGameState.getFood().asList()
    newFoodList = newFood.asList()
    # newGhostStates[0].configuration.getPosition()
    # newGhostStates[0].configuration.getDirection()
    directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0),
                   Directions.STOP:  (0, 0)}
    ghostPosition = newGhostStates[0].configuration.getPosition()
    newghostPosition = tuple(x-y for x, y in zip(ghostPosition, directions[newGhostStates[0].configuration.getDirection()]))
    distance = [manhattanDistance(dis, newPos) for dis in newFoodList]
    if cmp(ghostPosition, newPos) == 0:
      return -1000
    elif cmp(newghostPosition, newPos) == 0:
      return -1000
    if newPos in curFoodList:
      return 100
    return 1.0/min(distance)

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
import sys
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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    score = -sys.maxint
    depth = self.depth
    agentAction = gameState.getLegalActions(0)
    NumAgents = gameState.getNumAgents()
    if 'Stop' in agentAction:
      agentAction.pop(agentAction.index('Stop'))
    successors = [[action, gameState.generateSuccessor(0, action)] for action in agentAction]
    for successor in successors:
      v = minValue(self, successor[1], 1, depth, range(1, NumAgents))
      if v > score:
        score = v
        nextAction = successor[0]
    return nextAction

def maxValue(self, gameState, depth, d):
  if gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  score = -sys.maxint
  agentAction = gameState.getLegalActions(0)
  NumAgents = gameState.getNumAgents()
  if 'Stop' in agentAction:
    agentAction.pop(agentAction.index('Stop'))
  for action in agentAction:
      successor = gameState.generateSuccessor(0, action)
      score = max(score, minValue(self, successor, depth, d, range(1, NumAgents)))
  return score

def minValue(self, gameState, depth, d, ghostsList):
  if gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  if depth >= d:
    return self.evaluationFunction(gameState)
  score = sys.maxint
  ghost = ghostsList[0]
  ghostAction = gameState.getLegalActions(ghost)
  if len(ghostsList) == 1:
    depth += 1
    for action in ghostAction:
      successor = gameState.generateSuccessor(ghost, action)
      score = min(score, maxValue(self, successor, depth, d))
  else:
    for action in ghostAction:
      successor = gameState.generateSuccessor(ghost, action)
      score = min(score, minValue(self, successor, depth, d, ghostsList[1:]))
  return score


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    score = -sys.maxint
    depth = self.depth
    agentAction = gameState.getLegalActions(0)
    NumAgents = gameState.getNumAgents()
    a = -sys.maxint
    b = sys.maxint
    if 'Stop' in agentAction:
      agentAction.pop(agentAction.index('Stop'))
    successors = [[action, gameState.generateSuccessor(0, action)] for action in agentAction]
    for successor in successors:
      v = AlphaBetaMinValue(self, successor[1], 1, depth, range(1, NumAgents), a, b)
      if v >= score:
        score = v
        nextAction = successor[0]
    return nextAction

def AlphaBetaMaxValue(self, gameState, depth, d, a , b):
  if gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  score = -sys.maxint
  agentAction = gameState.getLegalActions(0)
  NumAgents = gameState.getNumAgents()
  if 'Stop' in agentAction:
    agentAction.pop(agentAction.index('Stop'))
  for action in agentAction:
      successor = gameState.generateSuccessor(0, action)
      score = max(score, AlphaBetaMinValue(self, successor, depth, d, range(1, NumAgents), a, b))
      if score >= b:
        return score
      a = max(a, score)
  return score

def AlphaBetaMinValue(self, gameState, depth, d, ghostsList, a, b):
  if gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  if depth >= d:
    return self.evaluationFunction(gameState)
  score = sys.maxint
  ghost = ghostsList[0]
  ghostAction = gameState.getLegalActions(ghost)
  if len(ghostsList) == 1:
    depth += 1
    for action in ghostAction:
      successor = gameState.generateSuccessor(ghost, action)
      score = min(score, AlphaBetaMaxValue(self, successor, depth, d, a, b))
      if score <= a:
        return score
      b = min(b, score)
  else:
    for action in ghostAction:
      successor = gameState.generateSuccessor(ghost, action)
      score = min(score, AlphaBetaMinValue(self, successor, depth, d, ghostsList[1:], a, b))
      if score <= a:
        return score
      b = min(b, score)
  return score


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
    # util.raiseNotDefined()
    score = -sys.maxint
    depth = self.depth
    agentAction = gameState.getLegalActions(0)
    NumAgents = gameState.getNumAgents()
    if 'Stop' in agentAction:
      agentAction.pop(agentAction.index('Stop'))
    successors = [[action, gameState.generateSuccessor(0, action)] for action in agentAction]
    for successor in successors:
      v = ExpectiMinVaule(self, successor[1], 1, depth, range(1, NumAgents), NumAgents - 1)
      if v >= score:
        score = v
        nextAction = successor[0]
    return nextAction
def ExpectiMaxVaule(self, gameState, depth, d):
  if gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  score = -sys.maxint
  agentAction = gameState.getLegalActions(0)
  NumAgents = gameState.getNumAgents()
  if 'Stop' in agentAction:
    agentAction.pop(agentAction.index('Stop'))
  for action in agentAction:
      successor = gameState.generateSuccessor(0, action)
      score = max(score, ExpectiMinVaule(self, successor, depth, d, range(1, NumAgents), NumAgents - 1))
  return score

def ExpectiMinVaule(self, gameState, depth, d, ghostsList, length):
  if gameState.isWin() == True or gameState.isLose() == True:
    return self.evaluationFunction(gameState)
  if depth >= d:
    return self.evaluationFunction(gameState)
  score = 0
  ghost = ghostsList[0]
  ghostAction = gameState.getLegalActions(ghost)
  l = len(ghostAction)
  if len(ghostsList) == 1:
    depth += 1
    for action in ghostAction:
      successor = gameState.generateSuccessor(ghost, action)
      score += ExpectiMaxVaule(self, successor, depth, d)
      return score/length
  else:
    for action in ghostAction:
      successor = gameState.generateSuccessor(ghost, action)
      score += ExpectiMinVaule(self, successor, depth, d, ghostsList[1:], length)
  score = score/l
  return score

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    There are several factors matter I think for this case.
    The first one is power pill in the game. After several testing case, I found if pacman ate the power pill at very first time. It is really helpful to get a high score in the final and promote the wining chance.
    About the power pill there are paramters. The summation of remaining scared time of each ghost. It is positive relatived to the evaluation score. And if the ghost is scared we can omit the relative position of ghost to pacman.
    The second one is relative position between pacman and each ghost. Because pacman make decision only depend on current game state and the ghost seems move randomly. I consider it is more dangerous when ghost is close to pacman. And when ghost is too close to pacman, I give a extra penalty to avoid that danger case.
    The food remained in the map is also key factor here. We want pacman move toward food and avoid pacman to replanning. So we compute manhattan distance to make pacman move close to food point and if pacman eat a food point in next movement we give it a reward(when the length of food list become short, evaluation value become larger).
    We can assure the weights before parameter should be positive or negative. But the exactly value of each weight can only obtain by guessing and tuning over and over.
  """
  "*** YOUR CODE HERE ***"
  # util.raiseNotDefined()
  evaluationValue = 0

  directions = {Directions.NORTH: (0, 1),
                   Directions.SOUTH: (0, -1),
                   Directions.EAST:  (1, 0),
                   Directions.WEST:  (-1, 0),
                   Directions.STOP:  (0, 0)}
  FoodList = currentGameState.getFood().asList()
  pos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates()
  ScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

  ghostPositions = currentGameState.getGhostPositions()
  disToGhost = sys.maxint
  scaredTime = sum(ScaredTimes)
  evaluationValue += 5*scaredTime
  gNumber = 0
  for ghost in ghostStates:
    ghostScaredTime = ghost.scaredTimer
    if ghostScaredTime > 0:
      continue
    ghostPosition = ghost.getPosition()
    curDis = util.manhattanDistance(pos, ghostPosition)
    if curDis < 5:
      gNumber += 1
    disToGhost = min(disToGhost, curDis)
  
  if disToGhost < 2:
      return -1000
  if disToGhost < 5:
    evaluationValue -= (1000/disToGhost)*gNumber

  disToFood = sys.maxint
  for food in FoodList:
    disToFood = min(util.manhattanDistance(food, pos), disToFood)
  evaluationValue += 10/disToFood

  remainFoodNum = len(FoodList) + 1
  evaluationValue += 10000/remainFoodNum
  score = currentGameState.getScore()
  evaluationValue += 2.5*score

  return evaluationValue
# Abbreviation


better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

