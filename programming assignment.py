import os  #use this to check whether our save loaction exists, which the code for this check is shown in lines 7-9
import random  #we are using randomization so import random
from itertools import zip_longest

save_folder='save_files/' #the variable which contains the string that describes the folder i want

d=os.path.dirname(save_folder)  #creates an object to know if a folder exists (in this case save_folder)
if not os.path.exists(d):
    os.makedirs(d)  #if no save_folder exists it creates that folder (save_folder)

if not os.path.exists(save_folder + 'high_score'):     #if there is no file
    with open(save_folder + 'high_score', 'w') as f:   #opens a new file high_score
        f.write('New_player 0\n')                      #writes this line to the file to make sure there is at least one item in the list (which is 'New_player' with score 0)

HWY, FAC, SHP, HSE, BCH = 8, 8, 8, 8, 8
buildings = ['HWY', 'FAC', 'SHP', 'HSE', 'BCH']

border = '  +-----+-----+-----+-----+'
letters = list('ABCD')  #['A', 'B', 'C', 'D']

board = [[" " for _ in range(4)] for _ in range(4)]  #making a list of lists of empty spaces within range 4

def display_board():  #print 4x4 board
    print('     ' + '     '.join(str(a) for a in letters), '\t', 'Buildings','\t\t', 'Remaining')  #prints the spaces, then buildings, then remaining buildings
    print(border + '\t --------            \t ---------')  #prints the lines of the board (\t means one tab of spacing)
    count = 1
    buildings_num = [HWY, FAC, SHP, HSE, BCH]  

    #zip takes 2 iterables and iterates them at the same time
    #if there are 3 items in list1 and 100 items in list2, zip prints out only 3 items
    #Example:
    #a = [1,2,3]
    #b = [4,5,6]
    #zip(a,b)
    #next() -> (1,4)
    #next() -> (2,5) etc

    #zip_longest -> will stop when both stop and will be (item, None)
    #zip_longest prints out 100 items but will have 97 'none'
    #Example:
    #a = [1,2,3]
    #b = [4,5]
    #zip_longest(a,b)
    #next() -> (1,4)
    #next() -> (2,5)
    #next() -> (3,None)
    
    for row, i, j in zip_longest(board, buildings, buildings_num):  #zip the board with buildings with building numbers 
        elem_row = '| '
        if row != None:  #basically i don't want to print a new row in BCH row
            for col in row:
                elem_row += str(col) + " " * (4 - len(col)) + "| "
            print(count, elem_row,'\t', i, '\t\t\t', j)  #when i want a row, it prints the count(1-4), i(buildings) and j(buildings_num)
        else:
            elem_row = " " * len(border)  #elem_row becomes empty and will be length of border
            print(" ", elem_row,'\t', i, '\t\t\t', j)  #if i don't want a new row i will print an empty space instead of count 5, and will print i(buildings) and j(buildings_num/Remaining)
        if row:
            print(border)
        count += 1

def random_building():  #makes sure that all selected buildings in option 1 and 2 are from supply of remaining buildings
    house_lists = []
    for i in range(FAC):
        house_lists.append('FAC')
    for i in range(BCH):
        house_lists.append('BCH')
    for i in range(HWY):
        house_lists.append('HWY')
    for i in range(HSE):
        house_lists.append('HSE')
    for i in range(SHP):
        house_lists.append('SHP')
    random_build1, random_build2 = random.sample(house_lists, k=2)   #giving the two variables the function to call for random buildings  #k=2 since we want 2 samples
    return random_build1, random_build2

def menu():
    print('Welcome, mayor of Simp City! ')
    print('-----------------------------')
    print('1. Start new game')
    print('2. Load saved game')
    print('3. Show high score')
    print('0. Exit')
    return input('Your choice? ')

def main_menu_loop():
    global HWY, FAC, SHP, HSE, BCH
    while True:     #a loop that goes infinitely unless we break out of it or return it(breaking)
        choice1 = menu()
        if choice1 == '0':
            print('Thanks for playing!')
            print()
            break
        elif choice1 == '1':
            global board    #makes board a global variable in order to load brand new empty board when starting new game
            board = [[' ', ' ', ' ', ' ']
                   , [' ', ' ', ' ', ' ']
                   , [' ', ' ', ' ', ' ']
                   , [' ', ' ', ' ', ' ']]

            HWY, FAC, SHP, HSE, BCH = 8, 8, 8, 8, 8  #remaining buildings all become 8 at option 1(start new game)
            random_build1, random_build2 = random_building()
            game_loop(random_build1, random_build2, turn_count=0)  

        elif choice1 == '2':
            turn_count, HWY, FAC, SHP, HSE, BCH, random_build1, random_build2 = load_game()  #if there is no saved game, it will start new game
            game_loop(random_build1, random_build2, turn_count)    #if no saved game, will be starting the game with original settings of starting turn_count 0 and 8 buildings each

        elif choice1 == '3':
            high_scores = load_high_score()  #loading high scores with load_high_score() and storing it in variable high_scores
            print_high_score(high_scores)    #printing the high scores variable in print_high_scores function

        else:
            print()
            print('Invalid input. Please type again.')
            print()

def print_score(number_list):
    for index, number in enumerate(number_list):   #enumerate to find index of element and not only element  #index will be number_list[0] etc
        print(str(number),end='')                  #end='' is to ensure everything is printed ona straight line (3 + 1 + 4 = 8 etc)
        if index == len(number_list) - 1:          #if this was the last numbers in the list (etc 4), print a '='
            print(' = ', end='')
        else:                                      #else if not last number in line, print '+'
            print(' + ', end='')
    print(sum(number_list))

#used to find specific neighbouring buildings of a certain building. SHP and HSE count points according to what neighbouring buildings, so function is used to find out their neighbours
def find_neighbours(row,column):
    neighbours=[]
    
    #to find neighbours above and below. row +1 finds below existing building. row -1 finds if there's building above existing builing.
    for i in [-1,1]:
        if 0<=row + i<len(board):  #checking if it's still within the board
            if board[row+i][column] != ' ':  #checking if it's a building or an empty space
                neighbours.append(board[row+i][column])
                
    #to find neighbours left and right. column +1 finds right of existing building. column -1 finds if there's building left of existing builing.
    for i in [-1,1]:
        if 0<=column + i<len(board[row]):
            if board[row][column+i] != ' ':
                neighbours.append(board[row][column+i])  #if within the board and not an empty space, appends left & right building into neighbours list
                                                         #another function checks what buildings are in the list to calculate score etc
    return neighbours

#function will be used to find if place in the board is empty or not
#can be used to find and check if place in board already has building or not to prevent player from placing buildings on already placed buildings on the board
def has_neighbour(row,column):  #when it runs the has_neighbour function it needs the 2 required arguments/parameters: row and column

    #check if there are neighbours above or below
    for i in [-1, 1]:
        if 0 <= row + i < len(board):  #check if row is inside of the (4x4)board
            if board[row + i][column] != ' ':  #check if the space is not empty
                return True  #if row is inside board and is not empty, then is a True(correct) turn

    #check if there are neighbours left right
    for i in [-1, 1]:
        if 0 <= column + i < len(board[row]):  #check if column is inside of the (4x4)board
            if board[row][column + i] != ' ':  #check if the space is not empty
                return True  #if column is inside board and is not empty, then is a True(correct) turn
    return False  #else becomes a False(failed) turn and loops back


def display_game_menu(random_build1,random_build2):
    print('1. Build a ' + random_build1)
    print('2. Build a ' + random_build2)
    print('3. See current score')
    print()
    print('4. Save game')
    print('0. Exit to game menu')

                                                        #'with' opens the file and 'f' is stated as variable name. 'as f' --> 'as' functions as backwards '='.
#Loading the game_loop                                  #I'm loading file with 'f' as variable (made possible by using 'with' in next lines)
def load_game():                                        #'with' is more convenient as it closes file automatically once code block is exited.
                                                        #Indents show each code block. E.g. lines 177 to 180 is one code block
    global board
    if os.path.exists(save_folder + 'turn_count'):      #checking if there is a saved file
        with open(save_folder+'turn_count','r') as f:   #opens the folder to show turn_count for player to read
            turn_count=int(f.read())

        with open(save_folder+'display_file','r') as f:  #opening the file, reading it and putting result into board variable
            board=[]
            for line in f.readlines():                #'f.readlines() returns a list like ['FAC, , , \n', 'HSE,SHP, , \n', ' , , , \n', ' , , , \n']
                board.append(line[:-1].split(','))    #line[:-1] removes \n at end of the commas and makes them split by commas -> ['FAC', ' ', ' ', ' '],  ['HSE', 'SHP', ' ', ' '] etc
                                                      #appends list to board
        #Example of a saved board with buildings:
        #BCH, , , 
        #HSE,SHP, , 
        #SHP, , , 
        #, , , 
        
        with open(save_folder+'remaining_buildings','r') as f:
            numbers=[]
            for s in f.readlines():  #f.readlines() assigns something to be a string.
                numbers.append(int(s))  #appends the converted to int 's' to numbers list
            HWY, FAC, SHP, HSE, BCH = numbers       #loops through list of strings, converts to int and add to list of numbers
                                                    #numbers is a list of 5 things and i am assignning these 5 values (HWY, BCH etc) to each numbers
        with open(save_folder + 'random_build1.txt', 'r') as f:
            random_build1=f.read().strip()  #loading saved game building options 1 & 2

        with open(save_folder + 'random_build2.txt', 'r') as f:
            random_build2=f.read().strip()

        return turn_count, HWY, FAC, SHP, HSE, BCH, random_build1, random_build2  #will return these 8 values into the game whenever we call the function

    else:
        print()
        print('There is no saved game. Please save after playing.')
        board = [[' ', ' ', ' ', ' ']  #stating what board will be
              , [' ', ' ', ' ', ' ']
              , [' ', ' ', ' ', ' ']   #showing that if there is no saved games, an empty board will be printed out
              , [' ', ' ', ' ', ' ']]


        turn_count = 0
        HWY, FAC, SHP, HSE, BCH = 8, 8, 8, 8, 8
        random_build1, random_build2 = random_building()
        return turn_count, HWY, FAC, SHP, HSE, BCH, random_build1, random_build2  #used to return original turn count, building numbers and new randomized random_build1 & 2 


#Loading high scores
def load_high_score():
    try:
      with(open(save_folder+'high_score','r')) as f:  #'r' as 'read' bc player is reading the loaded high score
         high_scores = []                             #high scores --> e.g [('Never',50),('Brad',40)] will be a list of lists
         for line in f.readlines():
             *name , score = line.split()  #'Never 50\n'.split() --> ['Never', '50']  # * makes everything that is not caught by other variables in that line in a list

             #Example:
             #high score name input and calculated score after splitting is ['david', ':)', '20']
             #would now be [['david', ':)'], '20'] instead of ['david', ':)', '20']

             name = " ".join(name)  #turns the list back into a single string of word like 'david :)'
             score = int(score)
             high_scores.append((name, int(score)))
      return high_scores  #will load the current high scores without deleting previous scores
    except ValueError:  #ValueError is when an operation/function receives an argument that has right type but inappropriate value
        
        #E.g. int('dog')
        #'dog' meant to be string not int
        
      return 'there\'s no high score yet!'

#saving high scores
def saving_high_scores(high_scores):
    with open(save_folder + 'high_score', 'w') as f:
        for one_high_score in high_scores:
            f.write(one_high_score[0] + ' ' +str(one_high_score[1]) + '\n')  #example is shown in line 254

#printing high scores
def print_high_score(high_scores):
    print()
    print('---------- HIGH SCORES ---------')
    print('{:5s}{:22s}{:5s}'.format('Pos','Player','Score'))
    print('---  ------                -----')
    for index,one_high_score in enumerate(high_scores):

        #one_high_score -> ('Never', 50)
        #one_high_score[0] -> 'Never'  --> name of player
        #one_high_score[1] -> 50 --> calculated total score of player
        #index -> 0 --> index starts from 0 onwards

        print('{:2d}.  {:<22s}{:>5d}'.format(index+1,one_high_score[0],one_high_score[1]))
    print('--------------------------------')
    print('\n')

def game_loop(random_build1, random_build2, turn_count=0):   #starts after choosing 1 or 2 in the main menu
    global HWY, FAC, SHP, HSE, BCH
    fail_turn = False  
    valid_num = ['1','2','3','4','0']
    buildings = ["HWY", "FAC", "SHP", "HSE", "BCH"]
    buildings_num = [8, 8, 8, 8, 8]
    while turn_count <= 15:
        turn_count = turn_count + 1
        print("\n")
        print('Turn ' + str(turn_count))
        buildings = ['HWY','FAC','SHP','HSE','BCH']
        remaining = [HWY, FAC, SHP, HSE, BCH]
        display_board()  #prints display_board() function
        display_game_menu(random_build1,random_build2)  #displaying game menu with random_build1 & random_build2 arguments

        your_choice = ''
        while your_choice not in ('1', '2', '3', '4', '0'):   #a loop to ensure player inputs the correct input

            your_choice = input('Your choice? ')

            #loop for choices 3,4,0
            if (your_choice == '3'):  #show current score
                print()
                show_score(FAC)  #FAC score depends on number of FAC built so FAC required as argument
                turn_count-=1  #reduce turn count by 1 to ensure turn count remains the same unless moving on to new turn

            elif (your_choice == '4'):  #Saving the game
                turn_count -= 1
                with open(save_folder + 'turn_count', 'w') as f:  #saving current turn_count
                    f.write(str(turn_count))

                with open(save_folder + 'display_file', 'w') as f:  #Basically:
                    for row in range(len(board)):                   #adds a ',' if it is not the last thing in the list (from [FAC,HSE,SHP,HWY] to [FAC,HSE,SHP,HWY,])
                        for column in range(len(board)):            #after finish writing the row we write a \n so we have ',' seperating columns and \n seperating rows
                            f.write(board[row][column])
                            if column<len(board)-1:
                                f.write(',')
                        f.write('\n')  #only want a new line after we have completed writing the row down

                with open(save_folder + 'remaining_buildings', 'w') as f:  #five supply buildings stored in a single file
                    for x in (HWY, FAC, SHP, HSE, BCH):  #loops over the 5 variables
                        f.write(str(x)+'\n')  #convert to string and add a newline(to print them in one straiht row) and save into file

                with open(save_folder + 'random_build1.txt', 'w') as f:  #savin current random_build1 & 2 as Text Document file
                    f.write(str(random_build1))

                with open(save_folder + 'random_build2.txt', 'w') as f:
                    f.write(str(random_build2))

                print()
                print('Game saved!')
                break

            elif (your_choice == '0'):
                print('Thanks for playing!')
                print()
                return  #exits the funtion #break won't work because there is 2 loops(line 271,281) and break will only break the second loop(line 281)

            else:
                if (your_choice.isalpha()) or (your_choice not in valid_num) or (your_choice == '3'):  #if not any of numbers option then print this
                    print('Wrong input. Please type in a correct number.')

        if (your_choice=='1') or (your_choice=='2'):  #loop and conditions for choices 1 and 2

            while True:  #while it is a correct turn
                build_where = input('Build where? ')
                if len(build_where) == 2:  #because build_where only supposed to be 'a1', 'b2' etc. Length should only be 2
                    x = build_where[0]
                    try:  #catch any cases where the int() conversion fails because a letter is input instead of a number #checking eligibility of build_where input
                        row = int(build_where[1]) - 1  #python tries this code and checks second character in build_where and makes it an int.
                                                       #if cannot make into int, then is ValueError

                    except ValueError:   #ValueError --> when an operation/function receives an argument that has right type but inappropriate value
                                         #e.g. int("a") --> ValueError
                        row = None  #if there is no ValueError in try code, row becomes nothing

                    if (x == 'a'):  #build_where[0] == 'x' == letter 'a' in 'a1' etc
                        column = 0  #column 0 is column A in board etc
                    elif (x == 'b'):
                        column = 1
                    elif (x == 'c'):
                        column = 2
                    elif (x == 'd'):
                        column = 3
                    else:
                        column = None  #if column is not a,b,c or d, column becomes nothing

                    if column is not None and row is not None and (row>=0 and row<len(board)):  #this code is for correct build_where input.
                                                                                                #if column & row not nothing and is in board then correct input
                                                                                              #else, if build_where input wrong, will print line 357/359 and go back to while True loop
                        break     #will break out of the checking for eligibility of build_where input if build_where == correct input
                    else:
                        print('Please type again. You have either typed something out of the board or the letter is capitalized.')
                else:
                    print('Please type again. Please type something in the form of a2 etc.')  #prints this if len of build_where input != 2

            if (has_neighbour(row,column) or turn_count == 1) and (board[row][column] == ' '):  #find out if position in board has a building already or has a spacing

                if (your_choice=='1') or (your_choice=='2'):
                    if (your_choice == '1'):  #placed this here to ensure that building options 1 & 2 remaing the same if player builds wrongly
                        building = random_build1
                        random_build1, random_build2 = random_building()  #will only randomize choices 1 & 2 buildings after every successful build

                    elif (your_choice == '2'):
                        building = random_build2
                        random_build1, random_build2 = random_building()

                    if (building == 'BCH'):   #removes 1 building each if each one is placed in board
                        BCH -= 1
                    if (building == 'FAC'):
                        FAC -= 1
                    if (building == 'HSE'):
                        HSE -= 1
                    if (building == 'SHP'):
                        SHP -= 1
                    if (building == 'HWY'):
                        HWY -= 1

                board[row][column] = building
                fail_turn=False    #not a fail turn since building onto board input is correct


            else:
                if (board[row][column] != ' '):  #if building placed in a space with existing building which is not an empty space
                    print('You must build in an empty spot in the board.')


                else:  #if building placed in a space with existing building which is an empty space, print:
                    print('You must build next to an existing building')
                turn_count=turn_count-1
                fail_turn=True  #is a failed turn since player build on existing building or not next to existing building

    else:
        end_game()  #prints out end game function after turn count becomes 16 and board is filled up

def score(FAC):
    points_dict = {'BCH':[], 'HSE':[], 'SHP':[], 'HWY':[], 'FAC':[]}     #points_dict is the variable while 'BCH' is the key to take out values in 'BCH' etc
    for row in range(len(board)):  #row & column are both len 4
        for column in range(len(board)):

            #BCH points
            if board[row][column]=='BCH':
                if (column==0) or (column==len(board)-1):  #if column is A or column is D. [len(board)-1 --> 4-1=3 and board[3] is D column] [column[0] is A column]
                    points_dict['BCH'].append(3)  #append 3 points to dictionary
                else:
                    points_dict['BCH'].append(1)

            #HSE points
            elif board[row][column]=='HSE':
                hse_neighbours=find_neighbours(row,column)  #finds neighbours of HSE on board since points depend on HSE neighbours
                hsepoint=0
                for building1 in hse_neighbours:
                    if building1 == 'FAC':
                        hsepoint=1
                        break
                    elif building1 == 'SHP':
                        hsepoint+=1
                    elif building1 == 'HSE':
                        hsepoint+=1
                    elif building1 == 'BCH':
                        hsepoint+=2
                points_dict['HSE'].append(hsepoint)

            #SHP points
            elif board[row][column]=='SHP':                   #if SHP found in the board
                shp_neighbours=find_neighbours(row,column)    #find_neighbours function look at left right up down of SHP
                uniq_items=[]
                for i in shp_neighbours:
                    if i not in uniq_items:                   #removing the duplicate building since additional buildings next to SHP do not score anything
                        uniq_items.append(i)
                shppoint=len(uniq_items)
                points_dict['SHP'].append(shppoint)

    #HWY points
    for row in board:    #looping over each row since HWY only counted according to rows not column. we are also checking row by row only for HWY
        count = 0                                    #how this segment works: if row 1=['HWY', 'FAC', 'HWY', 'HWY'], count start at 0, sees HWY in row 1[0], count goes up by one
        for building in row:                         #next building is FAC and not HWY, so stop increasing count and adds one point to HWY score dict
            if building == 'HWY':                    #next is HWY:count=1, another HWY:count=2
                count += 1                           #reached the end of the row, so we start counting the points added to dict
            elif count > 0:                          #is 1 for one HWY and 2 for 2 HWYs in a row
                for i in range(count):               #since we reached end of row, count resets to 0 and starts all over again to check next row
                    points_dict['HWY'].append(count)
                count = 0
        if count > 0:  #if count is greater thean 0 then append count to HWY dict
            for i in range(count):
                points_dict['HWY'].append(count)

    #FAC points
    FAC_built = 8-FAC
    if FAC_built<5:                                #FAC points is only calculated according to number of FAC built and only 1 point awarded per FAC if more than 4 built
        for i in range(FAC_built):                 #if there is less than 5 FAC in board, we add as many points as no. of FAC built. (if there is 2 FAC: 2+2)
            points_dict['FAC'].append(FAC_built)
    else:
        for i in range(4):                         #if number of FAC built is 6 for example,
            points_dict['FAC'].append(4)           #we add 4 times of 4 (4+4+4+4)
        for i in range(FAC_built - 4):             
            points_dict['FAC'].append(1)           #and 1 point per rest of FAC built, so if FAC built is 6, will be 2 times of 1 --> 4+4+4+4+1+1

    return points_dict

#ending result
def show_score(FAC):  #since FAC score depends on number of FAC built, FAC required as parameter to be local variable as we want to deduct FAC built from original number 8
    total_points=0
    points_dict = score(FAC)   #counts points according to number of FAC, so we use (FAC) key to take out the FAC scores in the dictionary

    for key in points_dict:
        total_points += sum(points_dict[key])   #loops over the list of numbers in each list('BCH' etc) and adds each number to each other.

    for key in points_dict:
        print(key + ': ', end='')
        print_score(points_dict[key])    #prints each buildings' scores with ':' at the end and prints the score on same line as each building
                                         #e.g. HSE: 1 + 1 + 4 + 5 + 1 = 12
        
    print('Total score: '+str(total_points))
    return total_points

def show_high_score(total_points):  
    i=0
    high_scores = load_high_score()           #dosen't need parameter bc this returns me the high score list. stating high_scores as variable

    if total_points > high_scores[-1][1]:     #if the total score is higher than lowest highscore.
        index = 0                             #highscore list is sorted from low to high so high_scores[-1][1] refers to last element. last element is lowest highscore

        while total_points < high_scores[index][1]:     #starting from the top (high_scores[index][1]), we look to see if total score is higher than top high score.
            index += 1                                  #Index goes up till we find the first high score that is beaten by this new high score. e.g. index 10 is worst high score
                                                        #finds index of total_points among high_scores
        print()
        print('Congratulations! You made the high score board at position '+str(index+1))
        enter_name = input('Please enter your name (max 20 chars): ')
        while i==0:  #to make a loop checking if high score name is less than 20 characters
            if len(enter_name)>20:
                print('Your name exceeds 20 characters. Please type again.')
                enter_name = input('Please enter your name (max 20 chars): ')
            elif enter_name == '':
                print('Your name cannot be a blank. Please type again (max 20 chars)')
                enter_name = input('Please enter your name (max 20 chars): ')
            else:
                break

        #high_scores = high_scores[start : step : stop]
        high_scores = high_scores[:index] + [(enter_name,total_points )] + high_scores[index:9]  #basically inserts enter_name & total_points between specific index of high_scores list
                                                                                                 #inserts between the score that's just higher and lower in high_scores list
        
        #high_scores[:index] --> from the start of high_scores to a index of total_points not including index
        #[(enter_name, total_score)] --> new enter_name input and calculated total_points
        #high_scores[index:9] --> from index of high_scores index 9. Is index 9 because max high_score len of high_score list is 10 and too low numbers & name are removed
        
        saving_high_scores(high_scores)
        print_high_score(high_scores)
    else:
        print("You didn't get into the high score list. Try harder next time!")  #print this if total points didnt exceed any high score number
        print_high_score(high_scores)


#end of game:
def end_game():
    global HWY, FAC, SHP, HSE, BCH
    print()
    print('Final layout of the city')
    buildings = ['HWY','FAC','SHP','HSE','BCH']
    remaining = [HWY, FAC, SHP, HSE, BCH]
    display_board()
    total_points = show_score(FAC)     #show_score is a function that counts scores. We have this function to count the points, then we collect in total_points.
                                       #At the same time show_score prints out normal scores (line 464)
    show_high_score(total_points)      #collected total_points will then be sent to show_high_score function and check accordingly if it can added to high scores
    print('Clearing saved file\'s...')
    saved_files = ['turn_count', 'display_file', 'remaining_buildings']  #the three files that we want to clear are stored in saved_files variable

    for file in saved_files:  #loops over each file in variable: first goes to turn_count, then display_file etc
        try:  #this 'try' tries to remove the file, but if there is an error, it just passes and skips it
            os.remove(save_folder + str(file))  #deletes the file
            HWY, FAC, SHP, HSE, BCH = 8, 8, 8, 8, 8  #returns each building number to original number at same time as it deletes each file
        except:
            pass
    print('File\'s cleared')
    print()

main_menu_loop()   #loop all the way back to main menu to repeat game
