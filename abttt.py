def main():
    gamemode = eval(input("Type 0 for a computer game, 1 for a 1 player game, or 2 for a 2 player game: "))
    S = eval(input("Initial state of game: "))
    Player = input("X or O: ")
    DrawBoard(S)

    if gamemode == 0:
        endgame = False
        while endgame != True:
            S, endgame = TreeBuildAB(S, Player)
            if endgame == False:
                DrawBoard(S)
                if Player == "X":
                    Player = "O"
                else: Player = "X"
            else:
                WinOrNot, placeholder = CheckWinner(S)
                if WinOrNot == True:
                    print("{0} won the game".format(Player))
                else: print("Draw")

    if gamemode == 1:
        WinOrNot, XorO = CheckWinner(S)
        DrawChecker = True
        for i in range(len(S)):
            if S[i] == " ":
                DrawChecker = False
        while WinOrNot == False and DrawChecker == False:
            if Player == "X":
                S = CurrentMove(S, Player)
                Player = "O"
                WinOrNot, XorO = CheckWinner(S)
                DrawChecker = True
                for i in range(len(S)):
                    if S[i] == " ":
                        DrawChecker = False
            elif Player == "O":
                S, endgame = TreeBuildAB(S, Player)
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

    if gamemode == 2:
            WinOrNot, XorO = CheckWinner(S)
            DrawChecker = True
            for i in range(len(S)):
                if S[i] == " ":
                    DrawChecker = False
            while WinOrNot == False and DrawChecker == False:
                if Player == "X":
                    S = CurrentMove(S, Player)
                    Player = "O"
                    WinOrNot, XorO = CheckWinner(S)
                    DrawChecker = True
                    for i in range(len(S)):
                        if S[i] == " ":
                            DrawChecker = False
                elif Player == "O":
                    S = CurrentMove(S, Player)
                    Player = "X"
                    WinOrNot, XorO = CheckWinner(S)
                    DrawChecker = True
                    for i in range(len(S)):
                        if S[i] == " ":
                            DrawChecker = False
            if WinOrNot == True:
                print("{0} won the game".format(XorO))
            else:
                print("It was a draw")
                
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

