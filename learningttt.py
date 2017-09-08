import random

def main():
    states = {}
    stepsize = eval(input("What would you like to set the stepsize to: "))
    explore = eval(input("What would you like to set the exploration rate to value from (0 to 1): "))
    numberofgames = eval(input("How many games would you like to play to train the computer: "))
    selftrain = eval(input("Would you like to train the computer yourself, or for it to train itself (0 for you to train, 1 for selftrain): "))
    for i in range(numberofgames):
        S = [" "," "," "," "," "," "," "," "," "]
        Player = "X"
        callnumber = 0
        WinOrNot, DrawChecker = False, False
        DrawBoard(S)
        while WinOrNot == False and DrawChecker == False:
            if Player == "X":
                if selftrain == 1:
                    S, endgame = TreeBuildAB(S, Player)
                    Player = "O"
                    DrawBoard(S)
                    WinOrNot, XorO = CheckWinner(S)
                    DrawChecker = True
                    for i in range(len(S)):
                        if S[i] == " ":
                            DrawChecker = False
                else:
                    S = CurrentMove(S, Player)
                    Player = "O"
                    WinOrNot, XorO = CheckWinner(S)
                    DrawChecker = True
                    for i in range(len(S)):
                        if S[i] == " ":
                            DrawChecker = False
                        
            elif Player == "O":
                    S, states = Rlearning(states,S,Player,stepsize,explore,callnumber)
                    Player = "X"
                    DrawBoard(S)
                    WinOrNot, XorO = CheckWinner(S)
                    DrawChecker = True
                    for i in range(len(S)):
                        if S[i] == " ":
                            DrawChecker = False
        if WinOrNot == True:
            print("{0} won the game".format(XorO))
        else:
            print("It was a draw")

    
def Rlearning(states,S,Player,stepsize,explore,callnumber):
    WinState = False
    DrawState = True
    WinOrNot, XorO = CheckWinner(S) 
    if WinOrNot == True:
        WinState = True
        if XorO == "O":
            states[str(S)] = 1
        else:
            states[str(S)] = 0
    DrawChecker = True
    for i in range(len(S)):
        if S[i] == " ":
            DrawChecker = False
            DrawState = False
    if DrawChecker == True:
            states[str(S)] = 0
    if str(S) not in states.keys():
        states[str(S)] = 0.5
    if WinState == False and DrawState == False:            
        moves = possiblemoves(S, Player)
        currentstates = []
        currentvalues = []
        Player = Playerchange(Player)            
        for i in moves:
            if str(i) not in states.keys():
                states[str(i)] = 0.5
            placeholder, states = Rlearning(states,i,Player,stepsize,explore,(callnumber+1))
            states[str(S)] = (states[str(S)] + stepsize*(states[str(i)]-states[str(S)]))
            currentvalues = currentvalues + [states.get(str(i))]
    if callnumber == 0:
        if random.random() < explore:
            returnedmove = moves[random.randrange(0,len(moves))]
        else:
            returnedmove = moves[currentvalues.index(max(currentvalues))]
        return returnedmove, states
    else:
        return None, states
    
def Playerchange(Player):
    if Player == "X":
        return "O"
    else:
        return "X"
    
def possiblemoves(S, Player):
    possiblemoves = []
    spacescounter = 0
    placeholder = 0
    for i in range(len(S)):
            if S[i] == " ":
                spacescounter += 1
    for i in range(spacescounter):
        for j in range(placeholder, len(S)):
            if S[j] == " ":
                 placeholder = j + 1
                 possiblemoves = possiblemoves + [(S[:j] + [Player] + S[(j+1):])]
                 break
    return possiblemoves

def CheckWinner(S):
    for i in range(0,7,3):
        if (S[i] != " " and S[i+1] != " " and S[i+2] != " ") and (S[i] == S[i+1] == S[i+2]):
            return True,S[i]
    for i in range(3):
        if (S[i] != " " and S[i+3] != " " and S[i+6] != " ") and (S[i] == S[i+3] == S[i+6]):
            return True,S[i]
    if (S[0] != " " and S[4] != " " and S[8] != " ") and (S[0] == S[4] == S[8]):
        return True,S[0]
    if (S[2] != " " and S[4] != " " and S[6] != " ") and (S[2] == S[4] == S[6]):
        return True,S[2]
    else:
        return False,S[0]

def CurrentMove(S, Player):
    x,y = eval(input("Type in the coordinates of your move separated by a comma (row, column): "))
    position = x*3+y
    while MoveChecker(position,S) == False:
        print("Invalid move try again")
        x,y = eval(input("Type in the coordinates of your move separated by a comma (row, column): "))
        position = x*3+y
    else:
        newboard = Movement(position,S,Player)
        return newboard

def Movement(position, S,Player):
    S = S[:position] + [Player] + S[position+1:]
    DrawBoard(S)
    return S

def MoveChecker(position,S):
    if S[position] != " ":
        return False
    else: return True

def DrawBoard(S):
    j = 0
    print("  0  1  2")
    for i in range(0,7,3):
        print("  -------")
        print("{0} |{1}|{2}|{3}|".format(j,S[i],S[i+1],S[i+2]))
        j+=1
    print("  -------\n")
    
def TreeBuildAB(S, Player):
    DrawChecker = True
    for i in range(len(S)):
        if S[i] == " ":
            DrawChecker = False
    WinOrNot, XorO = CheckWinner(S)
    while (WinOrNot == False) and (DrawChecker==False):    
        spacescounter = 0
        placeholder = 0
        possiblemoves = []
        Alpha = -2
        Beta = 2
        score = []
        
        for i in range(len(S)):
            if S[i] == " ":
                spacescounter += 1
        for i in range(spacescounter):
            for j in range(placeholder, len(S)):
                if S[j] == " ":
                    placeholder = j + 1
                    possiblemoves = possiblemoves + [(S[:j] + [Player] + S[(j+1):])]
                    break
        for i in possiblemoves:
            score = score + [alphabeta(i,Player,Player,Alpha,Beta)]
        nextmove = score.index(max(score))
        return possiblemoves[nextmove], False
    else:
        return S, True

def alphabeta(S, Player, Max, Alpha, Beta):
    if Player == "X":
        Player = "O"
    else:
        Player = "X"
        
    WinOrNot, XorO = CheckWinner(S)
    if WinOrNot == True:
        if XorO == Max:
            return 1
        else:
            return -1
    DrawChecker = True
    for i in range(len(S)):
        if S[i] == " ":
            DrawChecker = False
    if DrawChecker == True:
        return 0
    possiblemoves = []
    spacescounter = 0
    placeholder = 0
    for i in range(len(S)):
        if S[i] == " ":
            spacescounter += 1
    for i in range(spacescounter):
        for j in range(placeholder, len(S)):
            if S[j] == " ":
                placeholder = j + 1
                possiblemoves = possiblemoves + [(S[:j] + [Player] + S[(j+1):])]
                break
    if Player == Max:
        for i in possiblemoves:
            score = alphabeta(i, Player, Max, Alpha, Beta)
            if score > Alpha:
                Alpha = score
            if Alpha >= Beta:
                return Alpha
        return Alpha
    else:
        for i in possiblemoves:
            score = alphabeta(i, Player, Max, Alpha, Beta)
            if score < Beta:
                Beta = score
            if Alpha >= Beta:
                return Beta
        return Beta

main()
