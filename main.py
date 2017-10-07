import random


class QueueOfTiles:
    def __init__(self, max_size):
        self._Contents = []
        self._Rear = -1
        self._MaxSize = max_size
        for Count in range(self._MaxSize):
            self._Contents.append("")
            self.add()

    def is_empty(self):
        if self._Rear == -1:
            return True
        else:
            return False

    def remove(self):
        if self.is_empty():
            return None
        else:
            item = self._Contents[0]
            for Count in range(1, self._Rear + 1):
                self._Contents[Count - 1] = self._Contents[Count]
            self._Contents[self._Rear] = ""
            self._Rear -= 1
            return item

    def add(self):
        if self._Rear < self._MaxSize - 1:
            tile_library = create_tile_library()
            rand_no = random.randint(0, 26)
            self._Rear += 1
            self._Contents[self._Rear] = tile_library[rand_no]

    def show(self):
        if self._Rear != - 1:
            print()
            print("The contents of the queue are: ", end="")
            for Item in self._Contents:
                print(Item, end="")
            print()


def create_tile_library():
    tile_library = []
    for Count in range(26):
        tile_library.append(chr(65 + Count))
    tile_library.append(chr(9608))
    return tile_library


def create_tile_dictionary():
    tile_library = create_tile_library()
    tile_dictionary = dict()
    for Count in range(26):
        if Count in [0, 4, 8, 13, 14, 17, 18, 19]:
            tile_dictionary[tile_library[Count]] = 1
        elif Count in [1, 2, 3, 6, 11, 12, 15, 20]:
            tile_dictionary[tile_library[Count]] = 2
        elif Count in [5, 7, 10, 21, 22, 24]:
            tile_dictionary[tile_library[Count]] = 3
        else:
            tile_dictionary[tile_library[Count]] = 5
    return tile_dictionary


def display_tile_values(tile_dictionary, allowed_words):
    print()
    print("TILE VALUES")
    print()
    for Letter, Points in tile_dictionary.items():
        print("Points for " + Letter + ": " + str(Points))
    print()


def get_starting_hand(tile_queue, start_hand_size):
    hand = ""
    for Count in range(start_hand_size):
        hand += tile_queue.remove()
        tile_queue.add()
    return hand


def load_allowed_words():
    allowed_words = []
    try:
        words_file = open("chilwellwords.txt", "r")
        for Word in words_file:
            allowed_words.append(Word.strip().upper())
        words_file.close()
    except:
        pass
    return allowed_words


def check_word_is_in_tiles(word, player_tiles):
    in_tiles = True
    copy_of_tiles = player_tiles
    for count in range(len(word)):
        if word[count] in copy_of_tiles:
            copy_of_tiles = copy_of_tiles.replace(word[count], "", 1)
        elif word[count] not in copy_of_tiles:
            for i in range(len(word)):
                if word[i] == "█":
                    copy_of_tiles = copy_of_tiles.replace(word[i], "", 1)
        else:
            in_tiles = False
    return in_tiles


def check_word_is_valid(word, allowed_words):
    valid_word = False
    count = 0
    while count < len(allowed_words) and not valid_word:
        if allowed_words[count] == word:
            valid_word = True
        count += 1
    return valid_word


def add_end_of_turn_tiles(tile_queue, player_tiles, new_tile_choice, choice):
    if new_tile_choice == "1":
        no_of_end_of_turn_tiles = len(choice)
    elif new_tile_choice == "2":
        no_of_end_of_turn_tiles = 3
    else:
        no_of_end_of_turn_tiles = len(choice) + 3
    for Count in range(no_of_end_of_turn_tiles):
        player_tiles += tile_queue.remove()
        tile_queue.add()
    return tile_queue, player_tiles


def fill_hand_with_tiles(tile_queue, player_tiles, max_hand_size):
    while len(player_tiles) <= max_hand_size:
        player_tiles += tile_queue.remove()
        tile_queue.add()
    return tile_queue, player_tiles


def get_score_for_word(word, tile_dictionary):
    score = 0
    for Count in range(len(word)):
        score += tile_dictionary[word[Count]]
    if len(word) > 7:
        score += 20
    elif len(word) > 5:
        score += 5
    return score


def update_after_allowed_word(word, player_tiles, player_score, player_tiles_played, tile_dictionary, allowed_words):
    player_tiles_played += len(word)
    for Letter in word:
        player_tiles = player_tiles.replace(Letter, "", 1)
    player_score += get_score_for_word(word, tile_dictionary)
    return player_tiles, player_score, player_tiles_played


def update_score_with_penalty(player_score, player_tiles, tile_dictionary):
    for Count in range(len(player_tiles)):
        player_score -= tile_dictionary[player_tiles[Count]]
    return player_score


def get_choice():
    print()
    print("Either:")
    print("     enter the word you would like to play OR")
    print("     press 1 to display the letter values OR")
    print("     press 4 to view the tile queue OR")
    print("     press 7 to view your tiles again OR")
    print("     press 0 to fill hand and stop the game.")
    choice = input(">")
    print()
    choice = choice.upper()
    return choice


def get_new_tile_choice():
    new_tile_choice = ""
    while new_tile_choice not in ["1", "2", "3", "4"]:
        print("Do you want to:")
        print("     replace the tiles you used (1) OR")
        print("     get three extra tiles (2) OR")
        print("     replace the tiles you used and get three extra tiles (3) OR")
        print("     get no new tiles (4)?")
        new_tile_choice = input(">")
    return new_tile_choice


def display_tiles_in_hand(player_tiles):
    print()
    print("Your current hand:", player_tiles)


def have_turn(player_name, player_tiles, player_tiles_played, player_score, tile_dictionary, tile_queue, allowed_words,
              max_hand_size, no_of_end_of_turn_tiles):
    print()
    print(player_name, "it is your turn.")
    display_tiles_in_hand(player_tiles)
    new_tile_choice = "2"
    valid_choice = False
    while not valid_choice:
        choice = get_choice()
        if choice == "1":
            display_tile_values(tile_dictionary, allowed_words)
        elif choice == "4":
            tile_queue.Show()
        elif choice == "7":
            display_tiles_in_hand(player_tiles)
        elif choice == "0":
            valid_choice = True
            tile_queue, player_tiles = fill_hand_with_tiles(tile_queue, player_tiles, max_hand_size)
        else:
            valid_choice = True
            if len(choice) == 0:
                valid_word = False
            else:
                valid_word = check_word_is_in_tiles(choice, player_tiles)
            if valid_word:
                valid_word = check_word_is_valid(choice, allowed_words)
                if valid_word:
                    print()
                    print("Valid word")
                    print()
                    player_tiles, player_score, player_tiles_played = update_after_allowed_word(choice, player_tiles, player_score, player_tiles_played, tile_dictionary, allowed_words)
                    new_tile_choice = get_new_tile_choice()
            if not valid_word:
                print()
                print("Not a valid attempt, you lose your turn.")
                print()
            if new_tile_choice != "4":
                tile_queue, player_tiles = add_end_of_turn_tiles(tile_queue, player_tiles, new_tile_choice, choice)
            print()
            print("Your word was:", choice)
            print("Your new score is:", player_score)
            print("You have played", player_tiles_played, "tiles so far in this game.")
    return player_tiles, player_tiles_played, player_score, tile_queue


def display_winner(player_one_score, player_two_score):
    print()
    print("**** GAME OVER! ****")
    print()
    print("Player One your score is", player_one_score)
    print("Player Two your score is", player_two_score)
    if player_one_score > player_two_score:
        print("Player One wins!")
    elif player_two_score > player_one_score:
        print("Player Two wins!")
    else:
        print("It is a draw!")
    print()


def play_game(allowed_words, tile_dictionary, random_start, start_hand_size, max_hand_size, max_tiles_played, no_of_end_of_turn_tiles):
    player_one_score = 50
    player_two_score = 50
    player_one_tiles_played = 0
    player_two_tiles_played = 0
    tile_queue = QueueOfTiles(20)
    if random_start:
        player_one_tiles = get_starting_hand(tile_queue, start_hand_size)
        player_two_tiles = get_starting_hand(tile_queue, start_hand_size)
    else:
        player_one_tiles = "BTAHANDENONSARJ"
        player_two_tiles = "CELZXIOTNESMUAA"
    while player_one_tiles_played <= max_tiles_played and player_two_tiles_played <= max_tiles_played and len(
            player_one_tiles) < max_hand_size and len(player_two_tiles) < max_hand_size:
        player_one_tiles, player_one_tiles_played, player_one_score, tile_queue = have_turn("Player One", player_one_tiles, player_one_tiles_played, player_one_score, tile_dictionary, tile_queue, allowed_words, max_hand_size, no_of_end_of_turn_tiles)
        print()
        input("Press Enter to continue")
        print()
        player_two_tiles, player_two_tiles_played, player_two_score, tile_queue = have_turn("Player Two", player_two_tiles, player_two_tiles_played, player_two_score, tile_dictionary, tile_queue, allowed_words, max_hand_size, no_of_end_of_turn_tiles)
    player_one_score = update_score_with_penalty(player_one_score, player_one_tiles, tile_dictionary)
    player_two_score = update_score_with_penalty(player_two_score, player_two_tiles, tile_dictionary)
    display_winner(player_one_score, player_two_score)


def display_menu():
    print()
    print("=========")
    print("MAIN MENU")
    print("=========")
    print()
    print("1. Play game with random start hand")
    print("2. Play game with training start hand")
    print("9. Quit")
    print()


def main():
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("+ Welcome to the WORDS WITH CHILWELL game +")
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print()
    print()
    allowed_words = load_allowed_words()
    tile_dictionary = create_tile_dictionary()
    max_hand_size = 20
    max_tiles_played = 50
    no_of_end_of_turn_tiles = 3
    start_hand_size = 15
    choice = ""
    while choice != "9":
        display_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            play_game(allowed_words, tile_dictionary, True, start_hand_size, max_hand_size, max_tiles_played, no_of_end_of_turn_tiles)
        elif choice == "2":
            play_game(allowed_words, tile_dictionary, False, 15, max_hand_size, max_tiles_played, no_of_end_of_turn_tiles)


if __name__ == "__main__":
    main()
