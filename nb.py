import sys
import math
import random
import numpy as np
import  time
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
direction = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
weight=[100, -3, 11,  8,  8, 11, -3, 100,
        -3, -7, -4,  1,  1, -4, -7, -3,
        11, -4,  2,  2,  2,  2, -4, 11,
        8,  1,  2, -3, -3,  2,  1,  8,
        8,  1,  2, -3, -3,  2,  1,  8,
        11, -4,  2,  2,  2,  2, -4, 11,
        -3, -7, -4,  1,  1, -4, -7, -3,
        100, -3, 11,  8,  8, 11, -3, 100]



class Node(object):
  """
  蒙特卡罗树搜索的树结构的Node，包含了父节点和直接点等信息，还有用于计算UCB的遍历次数和quality值，还有游戏选择这个Node的State。
  """

  def __init__(self,board,color,bot):
    self.parent = None
    self.children = []
    self.pos=(0,0)
    self.color=color
    self.visit_times = 0
    self.quality_value = 0.0
    self.board=board
    self.bot=bot



def expand(node):
    rest=generate_legal_points(-node.color,node.board)
    for ob in rest:
      nodes=Node(node.board,--node.color,node.bot)
      nodes.pos=ob
      nodes.parent=node
    node.children.append(nodes)

    return




def best_child(node, is_exploration):

  best_score = -sys.maxsize
  best_sub_node = None
  u=np.finfo(np.float64).eps
  # Travel all sub nodes to find the best one
  for sub_node in node.children:

    # Ignore exploration for inference
    if is_exploration:
      C = 0.707106
    else:
      C = 0.0

    # UCB = quality / times + C * sqrt(2 * ln(total_times) / times)
    left = sub_node.quality_value/ (sub_node.visit_times+u)
    right = 1.0 * math.log(node.visit_times+1) / (sub_node.visit_times+u)
    score = left + C * math.sqrt(right)

    if score > best_score:
      best_sub_node = sub_node
      best_score = score

  return best_sub_node

def generate_legal_point( color, chessboard):
      rest = np.where(chessboard == COLOR_NONE)
      rest = list(zip(rest[0], rest[1]))
      legeldic = {x: legalpoint(x, chessboard, color) for x in rest}
      return rest,legeldic
def legalpoint(pos, board,color):
        score = 0
        row =pos[0]
        col =pos[1]
        for i in range(8):
            zs =0
            step = 1
            while (0 <= (row + (step +1)  * direction[i][0]) < 8) and (0 <= (col +(step + 1) * direction[i][1]) < 8)and( board[row + step * direction[i][0]][col + step * direction[i][1]]== -color):
                zs+=1
                if (board[row + (step + 1) * direction[i][0]][col + (step + 1) * direction[i][1]] == color):
                    score += zs
                    break
                step += 1
        return score
def make_next_move(chessboard, x: int, y: int, player: int):
      chessboard[x, y] = player
      for direc in direction:
          ctr = 0
          for i in range(8):
              dx = x + direc[0] * (i + 1)
              dy = y + direc[1] * (i + 1)
              if dx < 0 or dx >= 8 or dy < 0 or dy >= 8:
                  ctr = 0
                  break
              elif chessboard[dx, dy] == player:
                  break
              elif chessboard[dx, dy] == COLOR_NONE:
                  ctr = 0
                  break
              else:
                  ctr += 1
          for i in range(ctr):
              ddx = x + direc[0] * (i + 1)
              ddy = y + direc[1] * (i + 1)
              chessboard[ddx, ddy] = player
      return chessboard



def simulate(node):
    board=node.board
    seq=generate_legal_points(node.color,board)
    color=node.color
    bot=node.bot
    rest = np.where(board == COLOR_NONE)
    rest = len(list(zip(rest[0], rest[1])))
    while True:
        if rest==0:
            if bot==color:
                return 1
            else:
                return 0
        if len(seq)==0:
            color=-color
            seq = generate_legal_points(color, board)
            continue
        choice=random.choice(seq)
        board=make_next_move(board,choice[0],choice[1],color)
        color=-color
        seq=generate_legal_points(color,board)
        rest-=1


def monte_carlo_tree_search(node):

  # Run as much as possible under the computation budget
    clock = time.time_ns()
    node1=node
    while True:
        clock1 = time.time_ns()
        if clock1 - clock > 3000000:
            break
        qu=[]
        while len(node.children) > 0:
            qu.append(node)
            node = best_child(node, True)
        node.board=make_next_move(node.parent.board,node.pos[0],node.pos[1],node.color)
        expand(node)
        for i in range(10):
            reward=simulate(node)
            for ob in qu:
                ob.visit_times+=1
                ob.quality_value+=reward
                reward=1-reward

        node=node1
    best_next_node = best_child(node, False)
    return best_next_node.pos

class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        player=color


    def go(self, chessboard):
        self.candidate_list.clear()
        # rest=self.generate_legal_points(self.color,chessboard)
        # self.candidate_list=rest
        node = Node(chessboard,-self.color,self.color)
        expand(node)

        if len(node.children)==0:
            return
        self.candidate_list=generate_legal_points(self.color,chessboard)
        temp=monte_carlo_tree_search(node)
        self.candidate_list.remove(temp)
        self.candidate_list.append(temp)

