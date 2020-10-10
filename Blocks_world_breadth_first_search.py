from random import sample, randint
from itertools import combinations, chain
from operator import sub

def print_state(list):
    digits = len(str(len(list)))
    spaces = "  " * 18
    for i in list:
        print(spaces, "-" * (digits + 4))
        if(len(str(i)) == digits):
            print(spaces,"|", i,"|")
        else:
            print(spaces,"| ", i,"|")

def reconstruct_initial(n):                                                         #get random block positions for blocks to be placed
    first, middle, last = [0], list(range(1, n)), [n]
    all_combinations = (comb for i in range(n) for comb in combinations(middle, i))
    list_combinations =  list(list(map(sub, chain(a, last), chain(first, a))) for a in all_combinations)
    return (list_combinations[randint(0,len(list_combinations)-1)])

#-------------------------------Main program-----------------------------------
print("\nSolution for Blocks World problem using breadth first search algorithm")
while True:
    try:
        blocks = int(input("\nGive number of blocks to create initial state and goal state: "))
        if (blocks <= 2):
            print("Input number must be greater than 2...")
        else:
            break
    except ValueError:
        print("Error type of input, only integers are allowed. Please try again...")

goal_state = [i for i in range(1,blocks+1)]
initial= sample(goal_state,blocks)                                                  #initial block numbers
initial_positions = reconstruct_initial(len(initial))                               #random position for initial blocks to be placed on the ground

initial_state = []                                                                  #will store initial_state blocks (in random positions)
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

#print_state(initial_state)
#print("GROUND ----------------------------------------------------")
