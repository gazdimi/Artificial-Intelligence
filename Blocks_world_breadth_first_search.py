from random import sample, randint
from itertools import combinations, chain
from operator import sub
from graphics import *
from time import sleep
import math

class State():
    def __init__(self, initial_state, middle_state, block_interest, goal_state):        #initialization of attributes
        self.initial_state = initial_state
        self.middle_state = middle_state
        self.block_interest = block_interest
        self.goal_state = goal_state
        self.parent = None

    def problem_solved(self):                                                           #initial_state == goal_state
        if self.middle_state == self.goal_state:
            return True                                                                 #problem solved
        else:
            return False

def print_state(p_list, blocks, message):                                               #print state in command line window
    print(message)
    if(len(p_list)==blocks and p_list[0]==1):
        digits = len(str(len(p_list)))
        spaces = "  " * 12
        for i in range(len(p_list)-1,-1,-1):
            print(spaces, "-" * (digits + 4))
            if(len(str(p_list[i])) == digits):
                print(spaces,"|", p_list[i],"|")
            else:
                print(spaces,"| ", p_list[i],"|")
    else:
        temp_step = []
        for s in p_list:
            if(len(s)-1 not in temp_step):
                temp_step.append(len(s)-1)

        temp_step.sort()
        for x in range(temp_step[len(temp_step)-1],-1,-1):
            if(x not in temp_step):
                temp_step.append(x)
        fixed = []
        for i in range(len(temp_step)-1,-1,-1):
            temp = []
            for stack in p_list:
                for j in stack:
                    if(stack.index(j)==i):
                        temp.append(j)
            fixed.append(temp)

        if(len(p_list)==1):
            flag = True
        else:
            flag = False

        spaces = "  " * 12
        initial_spaces = spaces
        for sublist in fixed:
            first = True                                                                                  #for changing step of blocks
            digits = len(str(len(sublist)))
            for j in sublist:
                if(flag):
                    print(spaces, "-" * (digits + 4))
                    if(len(str(j)) == digits):
                        print(spaces,"|", j,"|",end="",flush=True)
                    else:
                        print(spaces,"| ", j,"|",end="",flush=True)
                else:
                    if(fixed.index(sublist)!=len(fixed)-1 and sublist.index(j)==0):                     #if not last nested list in fixed and current block is the first one
                        for stack in p_list:
                            if(j in stack):
                                temp_index = p_list.index(stack)
                                break
                        spaces += "          " * temp_index
                        if(first):
                            print(spaces, "-" * (digits + 4),end="",flush=True)
                            for i in range(len(sublist)-1):
                                print("    ", "-" * (digits + 4),end="",flush=True)
                            print("")
                            first = False

                        if(len(str(j)) == digits):
                            print(spaces,"|", j,"|",end="",flush=True)
                        else:
                            print(spaces,"| ", j,"|",end="",flush=True)

                    elif(fixed.index(sublist)==len(fixed)-1 and sublist.index(j)==0):
                        spaces = initial_spaces
                        if(first):
                            print(spaces, "-" * (digits + 4),end="",flush=True)
                            for i in range(len(sublist)-1):
                                print("    ", "-" * (digits + 4),end="",flush=True)
                            print("")
                            first = False

                        if(len(str(j)) == digits):
                            print(spaces,"|", j,"|",end="",flush=True)
                        else:
                            print(spaces,"| ", j,"|",end="",flush=True)

                    else:
                        if(first):
                            print(spaces, "-" * (digits + 4),end="",flush=True)
                            for i in range(len(sublist)-1):
                                print("    ", "-" * (digits + 4),end="",flush=True)
                            print("")
                            first = False

                        if(len(str(j)) == digits):
                            print("     |", j,"|",end="",flush=True)
                        else:
                            print("     | ", j,"|",end="",flush=True)
            print("")
            spaces = initial_spaces

    print("GROUND ------------------------------------------------------------------------------------------------")

def print_graph_window(win, p_list, blocks, message):                                   #print the initial state with graphics
    txt_message = Text(Point(400,15), message)
    txt_message.setTextColor('black'), txt_message.setSize(16), txt_message.setFace('courier'), txt_message.draw(win)

    step = round(((800 - 70)/len(p_list))/len(p_list))
    if(len(p_list)==blocks and p_list[0]==1):
        for i in range(blocks):
            if(i==0):
                rect = Rectangle(Point(70, 400), Point(130,460))
            else:
                x1 = rectangles[i-1].getP1().x + step*blocks
                y1 = rectangles[i-1].getP1().y
                x2 = rectangles[i-1].getP2().x + step*blocks
                y2 = rectangles[i-1].getP2().y
                rect = Rectangle(Point(x1,y1),Point(x2,y2))

            rect.setOutline('black'),rect.setWidth(3), rect.draw(win)

            number = Text(rect.getCenter(),str(i+1))
            number.setTextColor('red'), number.setSize(16), number.draw(win)

            rectangles.append(rect)
            texts.append([number, i+1])
    else:
        i = 0
        for stack in p_list:
            for x in stack:
                if(p_list.index(stack)==0 and stack.index(x)==0):
                    rect = Rectangle(Point(70, 400), Point(130,460))
                    previous_bottom = i
                elif(p_list.index(stack)!=0 and stack.index(x)==0):
                    x1 = rectangles[previous_bottom].getP1().x + step*len(p_list)
                    y1 = rectangles[previous_bottom].getP1().y
                    x2 = rectangles[previous_bottom].getP2().x + step*len(p_list)
                    y2 = rectangles[previous_bottom].getP2().y
                    rect = Rectangle(Point(x1,y1),Point(x2,y2))
                    previous_bottom = i
                else:
                    x1 = rectangles[i-1].getP1().x
                    y1 = rectangles[i-1].getP1().y - 60
                    x2 = rectangles[i-1].getP2().x
                    y2 = rectangles[i-1].getP2().y - 60
                    rect = Rectangle(Point(x1,y1),Point(x2,y2))

                rect.setOutline('black'),rect.setWidth(3), rect.draw(win)

                number = Text(rect.getCenter(),str(i+1))
                number.setTextColor('red'), number.setSize(16), number.draw(win)

                rectangles.append(rect)
                texts.append([number, i+1])
                i += 1

def reconstruct_initial(n):                                                                     #get random block positions for blocks to be placed
    first, middle, last = [0], list(range(1, n)), [n]
    all_combinations = (comb for i in range(n) for comb in combinations(middle, i))
    list_combinations =  list(list(map(sub, chain(a, last), chain(first, a))) for a in all_combinations)
    return (list_combinations[randint(0,len(list_combinations)-1)])

def sequential_conditions(current_state):                                                       #change current_state according to previous states
    children = []
    if(len(current_state.middle_state)==1 and current_state.middle_state[0] == current_state.goal_state):   #all blocks on the ground
        temp = current_state.middle_state[0]
        current_state.middle_state.clear()
        current_state.middle_state = [block for block in temp]
        print_state(current_state.middle_state, len(current_state.goal_state), "GOAL STATE ACCOMPLISHED")
        return children
    else:
        if not(not current_state.initial_state):                                                #initial_state not empty
            remove_from_initial = False
            current_stack = current_state.initial_state[len(current_state.initial_state)-1]     #get current stack (from where a block will be moved)
            moving_block = current_stack[len(current_stack)-1]
            if(moving_block==current_state.goal_state[0] or moving_block-current_state.block_interest == 1):
                current_state.block_interest = moving_block

            if not current_state.middle_state:
                current_state.middle_state.append([moving_block])                               #first block added in middle_state
                remove_from_initial = True
            else:
                if(current_state.block_interest==0 or current_state.block_interest==1):         #while first block of goal state doesn't exist on the ground
                    current_state.middle_state.append([moving_block])
                    remove_from_initial = True
                else:
                    middle_stack_index = -1
                    for current_stack in current_state.middle_state:
                        middle_stack_index += 1
                        if(current_stack[0]==current_state.goal_state[0]):
                            if((current_stack[len(current_stack)-1])+1 == moving_block):
                                current_state.middle_state[middle_stack_index].append(moving_block)
                                remove_from_initial = True
                                break
                            else:                                                               #if current moving_block can't be placed in the existing stack with first block equal to first block of goal_state
                                current_state.middle_state.append([moving_block])               #place the block to the ground
                                remove_from_initial = True
                                break
                        if(middle_stack_index==(len(current_state.middle_state)-1)):            #and current_stack[0]!=current_state.goal_state[0]
                            current_state.middle_state.append([moving_block])
                            remove_from_initial = True
                            break

                flag = False
                i = 0
                while ( i < len(current_state.middle_state)):
                    temp_stack = current_state.middle_state[i]
                    if(current_state.block_interest+1 in current_state.middle_state[i] and flag==False):
                        current_state.block_interest += 1
                        print_state(current_state.middle_state, len(current_state.goal_state), "MIDDLE STATE")
                        current_state.middle_state.pop(i)
                        i = -1
                        flag = True
                    if(flag and temp_stack[0]==current_state.goal_state[0]):
                        current_state.middle_state[i].append(current_state.block_interest)
                        flag = False
                        i = -1
                    if(moving_block-current_state.block_interest == 1 and flag==False):
                        break
                    i+=1

            if(remove_from_initial):
                if(len(current_stack)==1):                                                          #if current stack has only one remaining block inside (moving_block needs to be removed from initial after its movement)
                    current_state.initial_state.pop(len(current_state.initial_state)-1)
                else:                                                                               #more than one remaing blocks in current stack
                    current_state.initial_state[len(current_state.initial_state)-1].remove(moving_block)
                for x in current_state.initial_state:
                    if not x:
                        current_state.initial_state.remove(x)
    new_state = State(current_state.initial_state, current_state.middle_state, current_state.block_interest, current_state.goal_state)    #define next state (with above modefied parameters)
    new_state.parent = current_state
    children.append(new_state)
    print_state(current_state.middle_state, len(current_state.goal_state), "MIDDLE STATE")
    return children

def breadth_first_search(initial_state, goal_state):
    initial = State(initial_state,[],0,goal_state)                                      #middle_state represents state from initial to goal
    print_state(initial.initial_state, len(initial.goal_state), "INITIAL STATE")
    print_graph_window(win, initial.initial_state, len(initial.goal_state), "INITIAL STATE")
    if initial.problem_solved():                                                        #check if initial state is goal state, if it is, return initial as solution
        return initial
    search_frontier = list()                                                            #empty (list) represents search frontier for the algorithm
    closed_set = set()                                                                  #closed set for breadth first search algorithm
    search_frontier.append(initial)                                                     #put initial state to search frontier
    while search_frontier:
        state = search_frontier.pop(0)                                                  #current state
        if state.problem_solved():                                                      #if current state is solution, return it
            return state
        closed_set.add(state)
        children = sequential_conditions(state)                                         #look for extensions
        for child in children:
            if (child not in closed_set) or (child not in search_frontier):
                search_frontier.append(child)
    return None

#-------------------------------Main program-----------------------------------
print("\nSolution for Blocks World problem using breadth first search algorithm")
while True:
    try:
        blocks = int(input("\nGive number of blocks to create initial state and goal state: "))
        if (blocks <= 2 or blocks > 10):
            print("Input number must be greater than 2 and less or equal to 10...")
        else:
            break
    except ValueError:
        print("Error type of input, only integers are allowed. Please try again...")

goal_state = [i for i in range(1,blocks+1)]
initial= sample(goal_state,blocks)                                                      #initial block numbers
initial_positions = reconstruct_initial(len(initial))                                   #random position for initial blocks to be placed on the ground

initial_state = []                                                                      #will store initial_state blocks (in random positions)
previous_temp = []
for i in initial_positions:
    temp = []
    counter = i
    for j in initial:
        flat_list = [item for sublist in previous_temp for item in sublist]
        if (j in flat_list):
            continue
        if(counter!=0):
            temp.append(j)
            counter-=1
        else:
            break
    initial_state.append(temp)
    previous_temp.append(temp)

global win
win = GraphWin("Blocks World Puzzle", 800, 500)
ground = Rectangle(Point(0,460),Point(800,500))
ground.setFill('green'), ground.draw(win)

global rectangles
rectangles = []

global texts
texts = []

solution = breadth_first_search(initial_state, goal_state)

input("Press any key to exit...")
win.close()
