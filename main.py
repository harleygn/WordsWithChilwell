import csv
import time
import random
import operator
import letter_frequencies


class QueueOfTiles():
    def __init__(self, MaxSize):
        self._Contents = []
        self._Rear = -1
        self._MaxSize = MaxSize
        for Count in range(self._MaxSize):
            self._Contents.append("")
            self.Add()

    def IsEmpty(self):
        if self._Rear == -1:
            return True
        else:
            return False

    def Remove(self):
        if self.IsEmpty():
            return None
        else:
            Item = self._Contents[0]
            for Count in range(1, self._Rear + 1):
                self._Contents[Count - 1] = self._Contents[Count]
            self._Contents[self._Rear] = ""
            self._Rear -= 1
            return Item

    def Add(self):
        if self._Rear < self._MaxSize - 1:
            TileLibrary = CreateTileLibrary()
            # generates 1 non-uniform random sample from probability list tile_frequency
            RandNo = random.choices(range(letter_frequencies.num_of_tiles), letter_frequencies.tile_frequency)[0]
            self._Rear += 1
            self._Contents[self._Rear] = TileLibrary[RandNo]

    def Show(self):
        if self._Rear != - 1:
            print()
            print("The contents of the queue are: ", end="")
            for Item in self._Contents:
                print(Item, end="")
            print()


def CreateTileLibrary():
    TileLibrary = []
    for Count in range(26):
        TileLibrary.append(chr(65 + Count))
    TileLibrary.append(chr(9610))
    return TileLibrary


def CreateTileDictionary():
    TileLibrary = CreateTileLibrary()
    TileDictionary = dict()
    for Count in range(27):
        if Count in [0, 4, 8, 13, 14, 17, 18, 19]:
            TileDictionary[TileLibrary[Count]] = 1
        elif Count in [1, 2, 3, 6, 11, 12, 15, 20]:
            TileDictionary[TileLibrary[Count]] = 2
        elif Count in [5, 7, 10, 21, 22, 24]:
            TileDictionary[TileLibrary[Count]] = 3
        elif Count == 26:
            TileDictionary[TileLibrary[Count]] = 0
        else:
            TileDictionary[TileLibrary[Count]] = 5
    return TileDictionary


def DisplayTileValues(TileDictionary, AllowedWords):
    print()
    print("TILE VALUES")
    print()
    for Letter, Points in TileDictionary.items():
        print("Points for " + Letter + ": " + str(Points))
    print()


def GetStartingHand(TileQueue, StartHandSize):
    Hand = ""
    for Count in range(StartHandSize):
        Hand += TileQueue.Remove()
        TileQueue.Add()
    return Hand


def LoadAllowedWords():
    AllowedWords = []
    try:
        WordsFile = open("chilwellwords.txt", "r")
        for Word in WordsFile:
            AllowedWords.append(Word.strip().upper())
        WordsFile.close()
    except:
        pass
    return AllowedWords


def CheckWordIsInTiles(Word, PlayerTiles):
    MissingTiles = 0
    CopyOfTiles = PlayerTiles
    for Count in range(len(Word)):
        if Word[Count] in CopyOfTiles:
            CopyOfTiles = CopyOfTiles.replace(Word[Count], "", 1)
        else:
            MissingTiles += 1
    WildcardNumber = 0
    for char in CopyOfTiles:
        if char == "▊":
            WildcardNumber += 1
    return (WildcardNumber >= MissingTiles)


def CheckWordIsValid(Word, AllowedWords):
    ValidWord = False
    Count = 0
    while Count < len(AllowedWords) and not ValidWord:
        if AllowedWords[Count] == Word:
            ValidWord = True
        Count += 1
    return ValidWord


def AddEndOfTurnTiles(TileQueue, PlayerTiles, NewTileChoice, Choice):
    if NewTileChoice == "1":
        NoOfEndOfTurnTiles = len(Choice)
    elif NewTileChoice == "2":
        NoOfEndOfTurnTiles = 3
    else:
        NoOfEndOfTurnTiles = len(Choice) + 3
    for Count in range(NoOfEndOfTurnTiles):
        PlayerTiles += TileQueue.Remove()
        TileQueue.Add()
    return TileQueue, PlayerTiles


def FillHandWithTiles(TileQueue, PlayerTiles, MaxHandSize):
    while len(PlayerTiles) <= MaxHandSize:
        PlayerTiles += TileQueue.Remove()
        TileQueue.Add()
    return TileQueue, PlayerTiles


def GetScoreForWord(Word, TileDictionary):
  done1 = 0
  done2 = 0
  Score = 0
  NewWord = [] 
  for Count in range (len(Word)):
    Score += TileDictionary[Word[Count]]
  if len(Word) > 7:
    Score += 20
  elif len(Word) > 5:
    Score += 5
  for Letters in range(len(Word)):
      NewWord.append(Word[Letters])
  for Letter in range(len(NewWord)):
        if done1 == 1:
            break
        if NewWord[Letter] == NewWord[Letter + 1]:
            letter1 = Letter 
            letter2 = Letter 
            removekey(NewWord, letter1, letter2)
            for DiffLetters in range(len(NewWord)):
                if NewWord[DiffLetters] == NewWord[DiffLetters + 1]:
                    Score += 20
                    done1 = 1
                    break 
  return Score

def removekey(NewWord, letter1, letter2):
    del NewWord[letter1]
    del NewWord[letter2]
    return NewWord


def UpdateAfterAllowedWord(Word, PlayerTiles, PlayerScore, PlayerTilesPlayed, TileDictionary, AllowedWords):
    PlayerTilesPlayed += len(Word)
    for Letter in Word:
        if PlayerTiles.find(Letter) >= 0:
            PlayerTiles = PlayerTiles.replace(Letter, "", 1)
        else:
            PlayerTiles = PlayerTiles.replace("▊", "", 1)
    PlayerScore += GetScoreForWord(Word, TileDictionary)
    return PlayerTiles, PlayerScore, PlayerTilesPlayed


def UpdateScoreWithPenalty(PlayerScore, PlayerTiles, TileDictionary):
    for Count in range(len(PlayerTiles)):
        PlayerScore -= TileDictionary[PlayerTiles[Count]]
    return PlayerScore


def GetChoice():
    print()
    print("Either:")
    print("     enter the word you would like to play OR")
    print("     press 1 to display the letter values OR")
    print("     press 4 to view the tile queue OR")
    print("     press 7 to view your tiles again OR")
    print("     press 0 to fill hand and stop the game.")
    Choice = input(">")
    print()
    Choice = Choice.upper()
    return Choice


def GetNewTileChoice():
    NewTileChoice = ""
    while NewTileChoice not in ["1", "2", "3", "4"]:
        print("Do you want to:")
        print("     replace the tiles you used (1) OR")
        print("     get three extra tiles (2) OR")
        print("     replace the tiles you used and get three extra tiles (3) OR")
        print("     get no new tiles (4)?")
        NewTileChoice = input(">")
    return NewTileChoice


def DisplayTilesInHand(PlayerTiles):
    print()
    print("Your current hand:", PlayerTiles)


def CheckScoresheetExists():
    try:
        open("scores.csv", "r")
        pass
    except FileNotFoundError:
        with open("scores.csv", "a", newline="") as Scoresheet:
            FieldNames = ["Name", "Score", "Date"]
            Scoresheet = csv.DictWriter(Scoresheet, fieldnames=FieldNames)
            Scoresheet.writeheader()


def LoadScores():
    CheckScoresheetExists()
    with open("scores.csv") as ScoresCSV:
        Scores = csv.reader(ScoresCSV)
        next(Scores, None)
        try:
            ScoreList = sorted(Scores, key=operator.itemgetter(1), reverse=True)
            return ScoreList[:11]
        except IndexError:
            return None


def DisplayLeaderboard():
    ScoreList = LoadScores()
    if not ScoreList:
        print()
        print("Leaderboard is empty")
    else:
        RowNum = 1
        print()
        print("--------------")
        print("TOP 10 PLAYERS")
        print("--------------")
        print()
        print("Pos Name Score Date")
        for Name, Score, Date in ScoreList:
            print(str(RowNum) + ".", Name, Score, Date)
            RowNum += 1
    print()
    input("Press Enter to return to the main menu")


def GetPlayerName(PlayerNumber):
    PlayerName = ""
    print()
    while 0 == len(PlayerName) or len(PlayerName) >= 20:
        PlayerName = input("Player" + " " + str(PlayerNumber) + " " + "enter your name: ")
    return PlayerName


def SavePlayerScores(PlayerOneName, PlayerOneScore, PlayerTwoName, PlayerTwoScore):
    CheckScoresheetExists()
    with open("scores.csv", "a", newline="") as ScoresCSV:
        FieldNames = ["Name", "Score", "Date"]
        Scores = csv.DictWriter(ScoresCSV, fieldnames=FieldNames)
        Scores.writerow({"Name": PlayerOneName, "Score": PlayerOneScore, "Date": time.strftime("%d/%m/%Y")})
        Scores.writerow({"Name": PlayerTwoName, "Score": PlayerTwoScore, "Date": time.strftime("%d/%m/%Y")})


def HaveTurn(PlayerName, PlayerTiles, PlayerTilesPlayed, PlayerScore, TileDictionary, TileQueue, AllowedWords,
             MaxHandSize, NoOfEndOfTurnTiles):
    print()
    print(PlayerName, "it is your turn.")
    DisplayTilesInHand(PlayerTiles)
    NewTileChoice = "2"
    min_word_length = 3
    ValidChoice = False
    while not ValidChoice:
        Choice = GetChoice()
        if Choice == "1":
            DisplayTileValues(TileDictionary, AllowedWords)
        elif Choice == "4":
            TileQueue.Show()
        elif Choice == "7":
            DisplayTilesInHand(PlayerTiles)
        elif Choice == "0":
            ValidChoice = True
            TileQueue, PlayerTiles = FillHandWithTiles(TileQueue, PlayerTiles, MaxHandSize)
        else:
            ValidChoice = True
            if len(Choice) < min_word_length:
                ValidWord = False
            else:
                ValidWord = CheckWordIsInTiles(Choice, PlayerTiles)
            if ValidWord:
                ValidWord = CheckWordIsValid(Choice, AllowedWords)
                if ValidWord:
                    print()
                    print("Valid word")
                    print()
                    PlayerTiles, PlayerScore, PlayerTilesPlayed = UpdateAfterAllowedWord(Choice, PlayerTiles,
                                                                                         PlayerScore, PlayerTilesPlayed,
                                                                                         TileDictionary, AllowedWords)
                    NewTileChoice = GetNewTileChoice()
            if not ValidWord:
                print()
                print("Not a valid attempt, you lose your turn.")
                print()
            if NewTileChoice != "4":
                TileQueue, PlayerTiles = AddEndOfTurnTiles(TileQueue, PlayerTiles, NewTileChoice, Choice)
            print()
            print("Your word was:", Choice)
            print("Your new score is:", PlayerScore)
            print("You have played", PlayerTilesPlayed, "tiles so far in this game.")
    return PlayerTiles, PlayerTilesPlayed, PlayerScore, TileQueue


def DisplayWinner(PlayerOneScore, PlayerTwoScore, PlayerOneName, PlayerTwoName):
    print()
    print("**** GAME OVER! ****")
    print()
    print(PlayerOneName, "your score is", PlayerOneScore)
    print(PlayerTwoName, "your score is", PlayerTwoScore)
    if PlayerOneScore > PlayerTwoScore:
        print(PlayerOneName, "wins!")
    elif PlayerTwoScore > PlayerOneScore:
        print(PlayerTwoName, "wins!")
    else:
        print("It is a draw!")
    print()


def PlayGame(AllowedWords, TileDictionary, RandomStart, StartHandSize, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles):
    PlayerOneName = GetPlayerName(1)
    PlayerTwoName = GetPlayerName(2)
    PlayerOneScore = 50
    PlayerTwoScore = 50
    PlayerOneTilesPlayed = 0
    PlayerTwoTilesPlayed = 0
    TileQueue = QueueOfTiles(20)
    if RandomStart:
        PlayerOneTiles = GetStartingHand(TileQueue, StartHandSize)
        PlayerTwoTiles = GetStartingHand(TileQueue, StartHandSize)
    else:
        PlayerOneTiles = "BTAHANDENONSARJ"
        PlayerTwoTiles = "CELZXIOTNESMUAA"
    while PlayerOneTilesPlayed <= MaxTilesPlayed and PlayerTwoTilesPlayed <= MaxTilesPlayed and len(
            PlayerOneTiles) < MaxHandSize and len(PlayerTwoTiles) < MaxHandSize:
        PlayerOneTiles, PlayerOneTilesPlayed, PlayerOneScore, TileQueue = HaveTurn(PlayerOneName, PlayerOneTiles,
                                                                                   PlayerOneTilesPlayed, PlayerOneScore,
                                                                                   TileDictionary, TileQueue,
                                                                                   AllowedWords, MaxHandSize,
                                                                                   NoOfEndOfTurnTiles)
        print()
        input("Press Enter to continue")
        print()
        PlayerTwoTiles, PlayerTwoTilesPlayed, PlayerTwoScore, TileQueue = HaveTurn(PlayerTwoName, PlayerTwoTiles,
                                                                                   PlayerTwoTilesPlayed, PlayerTwoScore,
                                                                                   TileDictionary, TileQueue,
                                                                                   AllowedWords, MaxHandSize,
                                                                                   NoOfEndOfTurnTiles)
    PlayerOneScore = UpdateScoreWithPenalty(PlayerOneScore, PlayerOneTiles, TileDictionary)
    PlayerTwoScore = UpdateScoreWithPenalty(PlayerTwoScore, PlayerTwoTiles, TileDictionary)
    DisplayWinner(PlayerOneScore, PlayerTwoScore, PlayerOneName, PlayerTwoName)
    SavePlayerScores(PlayerOneName, PlayerOneScore, PlayerTwoName, PlayerTwoScore)


def DisplayMenu():
    print()
    print("=========")
    print("MAIN MENU")
    print("=========")
    print()
    print("1. Play game with random start hand")
    print("2. Play game with training start hand")
    print("3. Display leaderboard")
    print("9. Quit")
    print()


def Main():
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+ Welcome to the WORDS WITH CHILWELL game +")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print()
    print()
    AllowedWords = LoadAllowedWords()
    TileDictionary = CreateTileDictionary()
    MaxHandSize = 20
    MaxTilesPlayed = 50
    NoOfEndOfTurnTiles = 3
    StartHandSize = 15
    Choice = ""
    while Choice != "9":
        DisplayMenu()
        Choice = input("Enter your choice: ")
        if Choice == "1":
            PlayGame(AllowedWords, TileDictionary, True, StartHandSize, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles)
        elif Choice == "2":
            PlayGame(AllowedWords, TileDictionary, False, 15, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles)
        elif Choice == "3":
            DisplayLeaderboard()


if __name__ == "__main__":
    Main()
