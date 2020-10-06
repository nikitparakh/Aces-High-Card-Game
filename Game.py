###############################################################################
# Algorithm
#   display main header
#   display options
#   define necessary functions
#   initiate stock, tableau and foundation
#   start game
#       prompt for input
#       call function according to input
#       modify tableau, stock and foundation accordingly
#       display stock, tableau and foundation
#       prompt for user input
#       break loop if game won or user quits
#   End of program
###############################################################################


import cards  # required !!!

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card
        of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game
'''

def init_game():

    '''
        This function initiates stock, tableau and foundation using cards.py
        and returns them as a tuple
    '''
    stock = cards.Deck()                                                        # create stock deck
    stock.shuffle()                                                             # shuffle stock
    foundation = []                                                             # initiate empty foundation and tableau
    tableau = []

    for i in range(4):
        tableau.append([stock.deal()])                                          # deal one card to each column of tableau

    return (stock, tableau, foundation)                                         # return as tuple

def deal_to_tableau( stock, tableau ):
    '''
        This function deals one card each to every column of the tableau
        and is of no return type
    '''
    for i in range(4):                                                          # loop four times
        tableau[i].append(stock.deal())                                         # add card to column


def display( stock, tableau, foundation ):
    '''Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))

    # determine the number of rows to be printed -- determined by the most
    #           cards in any tableau column
    max_rows = 0
    for col in tableau:
        if len(col) > max_rows:
            max_rows = len(col)

    for i in range(max_rows):
        # display stock (only in first row)
        if i == 0:
            display_char = "" if stock.is_empty() else "XX"
            print("{:<8s}".format(display_char),end='')
        else:
            print("{:<8s}".format(""),end='')

        # display tableau
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print("{:4s}".format( str(col[i]) ), end='' )

        # display foundation (only in first row)
        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')

        print()

def get_option():
    '''
        This function prompts the user for an option and checks that the input
        supplied by the user is of the form requested in the menu.
        If the input is not of the required form, the function prints
        an error message and returns None.
    '''
    i = False                                                                   # create flag
    r = input('Input an option (DFTRHQ): ')                                     # prompt for input
    x = list(r.replace(' ', '').upper())                                        # create list of input
    if len(x)>0 and len(x)<=3:                                                  # if size of list is valid
        if len(x) == 1:
            if x[0] in 'DRHQ':                                                  # if input is one of 'DRHQ', set flag to True
                i = True
        elif len(x) == 2:
            if x[0] == 'F':                                                     # if first character is 'F'
                if x[1].isdigit():                                              # if second character is an int
                    if int(x[1])>=1 and int(x[1])<=4:                           # if int is in valid range, set flag to True
                        i = True
        else:
            if x[0] == 'T':                                                     # if first character is 'T'
                if x[1].isdigit() and x[2].isdigit():                           # if second and third characters are ints
                    if int(x[1])>=1 and int(x[1])<=4 and int(x[2])>=1 and int(x[2])<=4 and int(x[1])!=int(x[2]): # if they are in valid range and not equal, set flag to True
                        i = True
    if i == True:                                                               # if flag is True
        return x                                                                # return input
    else:
        print('Error in option: ', r)                                           # error message

def validate_move_to_foundation(tableau, from_col):
    '''
        This function checks if the card from inputted column can be moved to foundation.
        The function will return True, if the move is valid; and False, otherwise.
        In the latter case, it will also print an appropriate error
        message. There are two errors that can be caught: from_col is empty or move is invalid.
    '''
    r = 0                                                                       # initiate counter
    if from_col<1 or from_col>4:                                                # if value is valid
        return False
    elif tableau[from_col-1]==[]:                                               # if column is empty, return False
        return False
    elif tableau[from_col-1][-1].rank()==1:                                     # if card is an ace, return False
        return False
    else:
        for i in tableau:                                                       # for every column
            if i!=[]:                                                           # if not empty
                if i[-1].rank()!=1:                                             # if last card is not ace
                    if tableau[from_col-1][-1].rank()<i[-1].rank() and tableau[from_col-1][-1].suit()==i[-1].suit(): # compare cards, return True if valid
                        return True
                    else:                                                       # modify counter if not valid
                        r += 1
                else:                                                           # if last card is ace
                    if tableau[from_col-1][-1].suit()==i[-1].suit():            # compare cards, return True if valid
                        return True
                    else:                                                       # modify counter if not valid
                        r += 1
    if r!=0:                                                                    # return False if counter is modified
        return False

def move_to_foundation( tableau, foundation, from_col ):
    '''
        This function moves last card from inputted column to foundation if
        the move is valid
    '''
    i = tableau[from_col-1].pop()                                               # remove last card from column
    foundation.append(i)                                                        # add it to foundation


def validate_move_within_tableau( tableau, from_col, to_col ):
    '''
        This function checks if the card from inputted column can be moved to another empty column.
        The function will return True, if the move is valid; and False, otherwise.
    '''
    if from_col>=1 and from_col<=4 and to_col>=1 and to_col<=4:
        if tableau[to_col-1]==[]:                                               # if to_col is empty
            if tableau[from_col-1]!=[]:                                         # if from_col is not empty, return True
                return True
            else:                                                               # return False otherwise
                return False
        else:
            return False
    else:
        return False

def move_within_tableau( tableau, from_col, to_col ):
    '''
        This function moves last card from inputted column to an empty column if
        the move is valid
    '''
    i = tableau[from_col-1].pop()                                               # remove last card from column
    tableau[to_col-1].append(i)                                                 # add to it empty column


def check_for_win( stock, tableau ):
    '''
        This function checks if user has won the game.
        It returns True, if the stock is empty and the tableau contains only the
        four aces; and False, otherwise.
    '''
    r = 0                                                                       # initiate counter
    if stock.is_empty():                                                        # if stock is empty
        for i in tableau:                                                       # for each column in tableau
            if i!=[]:                                                           # if column is not empty
                if len(i)==1:                                                   # if column only has one card
                    if i[-1].rank()==1:                                         # if card is an Ace, modify counter by one
                        r += 1
                    else:                                                       # return False otherwise
                        return False
                else:
                    return False
            else:
                return False
    else:
        return False
    if r == 4:                                                                  # if all four aces, return True
        return True


def main():
    '''
        This function is the main function.
        It displays rules and options.
        It initiates the game by initializing stock, tableau and foundation
        It asks for user input, calls functions accordingly and modifies stock, tableau and foundation
        It ends loop if user wins or quits
    '''

    stock, tableau, foundation = init_game()                                    # initiate stock, tableau and foundation
    print(MENU)
    display( stock, tableau, foundation )                                       # display stock, tableau and foundation
    print()
    while 1:                                                                    # create loop
        option = get_option()                                                   # get option
        if option!=None:
            if option[0]=='D':
                deal_to_tableau(stock, tableau)                                 # deal cards to tableau and display
                display(stock, tableau, foundation)
                print()
            elif option[0]=='H':
                print(MENU)                                                     # print menu and display
                display(stock, tableau, foundation)
                print()
            elif option[0]=='Q':
                print('You have chosen to quit.')                               # print end message and break loop
                break
            elif option[0]=='R':
                print("=========== Restarting: new game ============")          # restart game
                print(RULES)                                                    # print rules and menu
                print(MENU)
                stock, tableau, foundation = init_game()                        # initiate stock, tableau and foundation and display
                display( stock, tableau, foundation )
                print()
            elif option[0]=='F':
                from_col =  int(option[1])
                if validate_move_to_foundation(tableau, from_col):              # if move is valid
                    move_to_foundation( tableau, foundation, from_col )         # move card to foundation
                else:
                    print("Error, cannot move {}.".format(tableau[from_col-1][-1])) # error message
                if not check_for_win(stock, tableau):                           # display stock, tableau and foundation if game not won yet
                    display( stock, tableau, foundation )
                    print()
            elif option[0]=='T':
                from_col, to_col = int(option[1]), int(option[2])
                if validate_move_within_tableau(tableau, from_col, to_col):     # if move is valid
                    move_within_tableau(tableau, from_col, to_col)              # move card to empty column
                else:
                    print('Invalid move')                                       # error message
                if not check_for_win(stock, tableau):                           # display stock, tableau and foundation if game not won yet
                    display( stock, tableau, foundation )
                    print()
        if option == None:                                                      # if input is invalid, print error message
            print('Invalid option.')
            display( stock, tableau, foundation )
            print()
        if check_for_win(stock, tableau):                                       # if game has been won, print message and break loop
            print("You won!")
            break


if __name__ == "__main__":
    main()                                                                      # call main

# End of program
