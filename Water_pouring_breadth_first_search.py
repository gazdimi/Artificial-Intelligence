import sys
import math

class State:
    def __init__(self, capacity_1, current_volume_1, capacity_2, current_volume_2, target): #initialization of attributes of each state object
        self.capacity_1 = capacity_1
        self.current_volume_1 = current_volume_1
        self.capacity_2 = capacity_2
        self.current_volume_2 = current_volume_2
        self.target = target
        self.parent = None

    def problem_solved(self):
        if(self.current_volume_1 + self.current_volume_2 == self.target):               #check if solution has been reached
            return True
        else:
            return False

    def accepted(self):                                                                 #check if new state can be accepted
        return (self.current_volume_1 <= self.capacity_1 and self.current_volume_2 <= self.capacity_2)

def sequential_conditions(current_state):
    children = []
    if(current_state.current_volume_1 == 0):                                            #jug 1 is empty
        current_state.current_volume_1 = current_state.capacity_1                       #fill it

    elif(current_state.current_volume_2 == current_state.capacity_2):
        current_state.current_volume_2 = 0

    elif(not(current_state.current_volume_1 == 0)):
        target_volume = min(current_state.capacity_2, (current_state.current_volume_2 + current_state.current_volume_1))
        temp_volume = max(0, current_state.current_volume_2 + current_state.current_volume_1 - current_state.capacity_2)
        current_state.current_volume_1 = temp_volume
        current_state.current_volume_2 = target_volume

    new_state = State(current_state.capacity_1, current_state.current_volume_1, current_state.capacity_2, current_state.current_volume_2, current_state.target)
    if (new_state.accepted()):
        new_state.parent = current_state
        children.append(new_state)

    return children

def breadth_first_search(capacity_1, capacity_2, target):                               #breadth first search algorithm
    initial_state = State(capacity_1,0,capacity_2,0,target)
    if initial_state.problem_solved():
        return initial_state
    search_frontier = list()
    closed_set = set()
    search_frontier.append(initial_state)
    while search_frontier:
        state = search_frontier.pop(0)
        if state.problem_solved():
            return state
        closed_set.add(state)
        children = sequential_conditions(state)
        for child in children:
            if (child not in closed_set) or (child not in search_frontier):
                search_frontier.append(child)
    return None


print("\nSolution for Water Pouring problem using breadth first search algorithm with two water jugs")
print("\nGive a capacity number for each jug and then give target number for the algorithm to solve the puzzle\n")
while True:
    try:
        jug_A = int(input("Jug A: "))
        jug_B = int(input("Jug B: "))
        target = int(input("Target: "))
        if (jug_A <= 0 or jug_B <= 0 or target <= 0):
            print("Input numbers must be greater than 0...")
        else:
            break
    except ValueError:
        print("Error type of input, only integers are allowed. Please try again...")

if(jug_A == jug_B):
    print('Water jugs can\'t have equal capacity...')
    sys.exit(1)

if(target > jug_A and target > jug_B):
    print('Target number can\'t be greater than the jug capacities...')
    sys.exit(1)

gcd = math.gcd(jug_A,jug_B)

if(target % gcd != 0):
    print('Τhere is no possible solution for the given numbers..')
    sys.exit(0)

smaller = min(jug_A, jug_B)
larger = max(jug_A, jug_B)
solution = breadth_first_search(smaller, larger, target)

path = []
path.append(solution)
parent = solution.parent
while parent:
    path.append(parent)
    parent = parent.parent
print("\nJug 1 current volume of capacity ", solution.parent.capacity_1," | Jug 2 current volume of capacity ", solution.parent.capacity_2)
print("__________________________________________________________________________"), print("")
for i in range(len(path)-1):
    state = path[len(path) - i - 1]
    print("     "*4,state.current_volume_1,"     "*2,"   |   ","     "*3, state.current_volume_2)
    print("----------------------------------------------------------------------")

input("Press any key to exit...")
