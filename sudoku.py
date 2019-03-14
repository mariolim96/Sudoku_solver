#Sudoku solution by Mario Esposito
#formatting the sudoku
import pdb
import random
def print_sudoku(board):
    
    numrow = 0
    for row in board:
        if numrow % 3 == 0 and numrow != 0:
            print (' ')
        print (row[0:3], ' ', row[3:6], ' ', row[6:9])
        numrow += 1
#undo an element into the board
def undo(board, x, y):
    board[x][y] = 0
    return board

#used to insert a value into board
def insert(board, x, y, val):
    
    if (0 <= y <= 8 and 0 <= x <= 8 and 1 <= val <= 9):
        if is_valid(board, x, y, val):
            board[x][y] = val
            return board
        else:
            board[x][y] = 0
            print('impossibile inserire il numero')
    else:
        print('i parametri sono sbagliati')
    return board


#checking if a value can go in a square
def is_valid(board,x, y,val):
    #for rows
    if val in board[x]:
        return False
    #for colum
    for col in board:
        if val == col[y]:
            return False
    x = 3*(x // 3)
    y = 3*(y // 3)
    #for square 
    for i in range(x, x+3):
            if val in board[i]:
                return False
    return True

#finding a free cell
def find_next_cell(board):
    #Look for an unfilled board location
    for x in range(9):
        for y in range(9):
            if board[x][y] == 0:
                return x,y
    return -1,-1


# find the possible value of the cell
def set_value(board,x,y,set_a):
    
    for i in range(1,10):
        if(is_valid(board,x,y,i)):
            set_a.add(i)
            
    return set_a


#find the value that cannot be into the cell observing row and colums 
def set_row_value(board, x, y):
    sector=3*(x//3)
    set_a={1,2,3,4,5,6,7,8,9}
    setb=set({})
    for i in range(sector,sector+3):
        if i != x:
            for j in range(9):
                if  board[i][j] != 0:
                    setb.add(board[i][j])
            set_a = set_a & setb
            setb.clear()
        
    print('row',set_a)

    return set_a


def set_col_value(board,x,y):
    sector=3*(y//3)
    set_a={1,2,3,4,5,6,7,8,9}
    setb=set({})
    for i in range(sector,sector+3):
        if i == y:
            continue
        else:
            for j in range(9):
                if  board[j][i] != 0:
                    setb.add(board[j][i])
        set_a = set_a & setb
        setb.clear()
    print('col',set_a)

    return set_a

#find if there is a singleton into cell and put it 
def implication(set_a, x, y, board):
    #if the set is a singleton
    print_sudoku(board)
    if len(set_a)==1:
        board[x][y]=set_a.pop()
        return True
    else:# intersection between row and set
        setcopy = set_a.copy()
        setrow = set_row_value(board,x,y)
        setcopy = setcopy - setrow
        if len(setcopy) == 1:
            board[x][y] = setcopy.pop()
            return True
        else:# intersection between col and set
            setcol = set_col_value(board,x,y)
            setcopy = set_a.copy()
            setcopy = setcopy - setcol
            if len(setcopy) == 1:
                board[x][y] = setcopy.pop()
                return True
            else:# intersection between row, col and set 
                set_a=((set_a - setcol) - setrow)
                if len(set_a) == 1:
                    board[x][y] = set_a.pop()
                    return True
    return False

def sudoku_solver(board,i = 0,j = 0):
   
    global backtracks
    i,j = find_next_cell(board)
    if i == -1:
        return True
    set_a = set()
    set_a = set_value(board, i, j, set_a)
    for k in set_a:
        board[i][j] = k
        #if implication(set_a,i,j,board):
        if sudoku_solver(board, i, j):
            return True
        backtracks += 1
        board[i][j] = 0
    return False
    
def random_sudoku(board, n):
    
    set_a = set()
    for i in range(n):
        idx_i = random.randrange(9)
        idx_j = random.randrange(9)
        set_a = set_value(board,idx_i, idx_j,set_a)
        val = random.sample(set_a,1)
        board[idx_i][idx_j] = val[0]
        set_a.clear()
backtracks = 0
def main():
    
    empty = 0
    board =  [[5,1,7,6,0,0,0,3,4],
                    [2,8,9,0,0,4,0,0,0],
                    [3,4,6,2,0,5,0,9,0],
                    [6,0,2,0,0,0,0,1,0],
                    [0,3,8,0,0,6,0,4,7],
                    [0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0],
                    [0,9,0,0,0,0,0,7,8],
                    [7,0,3,4,0,0,5,6,0]]
    
    while True:
        print('menu')
        print('0 stampa la il sudoku\n')
        print('1 inserisci valore \n')
        print('2 risolvi sudoku\n')
        print('3 random sudoku  \n')
        print('4 pulisci sudoku \n')
        print('5 cancella valore\n')
        print('6 esci \n')
        scelta = input('digita la scelta: ')
        if (scelta == '1'):
            val = int(input('inserisci il numero compreso tra 1 e 9:'))
            x = int(input('inserisci il cordinata x compresa tra 0 e 8:'))
            y = int(input('inserisci la cordinata y compresa tra 0 e 8:'))
            board = insert(board,x,y,val)
            print(print_sudoku(board))
        if (scelta == '0'):
            print(print_sudoku(board))
        if (scelta == '2'):
            sudoku_solver(board)
            print(print_sudoku(board)," backtracks",backtracks)
        if (scelta == '3'):
            val = int(input('quanti numeri vuoi inserire?'))
            random_sudoku(board,val)
        if (scelta == '4'):
            board = [[empty for i in range(9)]for j in range(9)]
        if (scelta == '5'):
            x = int(input('inserisci il cordinata x compresa tra 0 e 8:'))
            y = int(input('inserisci la cordinata y compresa tra 0 e 8:'))
            board = undo(board,x,y)
        if (scelta == '6'):
            break

main()
