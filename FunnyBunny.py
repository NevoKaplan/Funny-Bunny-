import random

global player_list


class Bunny:
    def __init__(self, name):
        self.name = name
        self.loc_list = [[1, -1], [2, -1], [3, -1], [4, -1]]

    def get_alive(self):
        count = -2
        for j in range(len(self.loc_list)):
            if self.loc_list[j][1] != -2:
                count += 1
        return count

    def next_bunny(self, num):
        for r in range(len(self.loc_list)):
            if r > num and self.loc_list[r][1] != -2:
                return r
        return -2

    def furthest_bunny(self):
        maxi = -1
        index = -10
        for t in range(len(self.loc_list) - 1, -1, -1):
            if self.loc_list[t][1] >= maxi:
                maxi = self.loc_list[t][1]
                index = t
        return index


class Board:
    def __init__(self):
        self.board = ["empty"]*30
        self.bridgeEnabled = True
        self.gateOpen = False
        self.holeLoc = -3

    def set_hole(self, num):
        self.board[num] = "hole"
        self.board[self.holeLoc] = "empty"
        self.holeLoc = num

    def set_loc(self, num, pre_num):
        if num <= 27 and self.board[num] != "hole":
            self.board[num] = "occ"
        self.board[pre_num] = "empty"

    def get_hole(self):
        return self.holeLoc

    def is_location_valid(self, current, future):
        valid = True
        if current <= 13 and future >= 14 and not self.bridgeEnabled:
            valid = False
        return valid

    def find_leader(self):
        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i] == "occ":
                q, w = find_bunny(i)
                return q, w
        return -2, -2


def random_card():
    card = random.randint(1, 4)
    events = -1
    if card == 4:
        card = random.randint(1, 25)
        events = random.randint(1, 3)
        print("hole created at " + str(card) + " and event number " + str(events))
    return card, events


sen_choice = ["burned in a fire. He's dead.", "was sent to the abyss.", "is an asshole. He's with god now.",
              "is a loser... He died.", "is in a better place now. Maybe?", "was removed from the game.",
              "is dead, sorry.", "fell out of the world.", "is playing Bibi's Adventure, we'll leave him alone.",
              "went to sleep. Forever.", "is 6 feet deep."]


def find_bunny(n):
    global player_list
    for q in range(len(player_list)):
        if player_list[q] is not None:
            for w in range(len(player_list[q].loc_list)):
                if player_list[q].loc_list[w][1] == n:
                    return q, w
    return -1, -1


def enter(dead_bunny, dead_player, board):
    global player_list
    while True:
        go = input("Press enter to continue\n")
        go = go.lower()
        if go == "l":
            f, g = board.find_leader()
            if player_list[f] is not None and f != -2 and player_list[f].loc_list[g][1] >= 0:
                print("The leader is " + player_list[f].name + " with bunny number " +
                      str(player_list[f].loc_list[g][0]) + " at " + str(player_list[f].loc_list[g][1]))
            else:
                print("All bunnies are at the start... or dead.")
        elif go == "d":
            print("Number of dead bunnies: " + str(dead_bunny) + "\nNumber of dead players: " +
                  str(dead_player))
        elif go == "barifan" or go == "hamar":
            print("Nice.")
        else:
            return


def run():
    global player_list
    player_list = []
    board = Board()
    dead_bunny = 0
    dead_player = 0
    nm = True
    while nm:
        players_num = input("Welcome to Funny Bunny.\nCreated by Nevo Kaplan.\nEnter amount of players: ")
        if players_num.isnumeric():
            players_num = int(players_num)
            if players_num != 0:
                nm = False
                if players_num > 4:
                    print("I generally don't recommend going above 4 players.\nBut if you insist, go ahead.")
                    enter(dead_bunny, dead_player, board)
            else:
                print("Number can't be 0.\n")
        else:
            print("That's not a positive whole number!\n")

    for i in range(players_num):
        p_name = input("Enter player number " + str(i + 1) + "'s name: ")
        player_list.append(Bunny(p_name))

    while True:
        for i in range(players_num):
            if player_list[i] is not None:
                print(player_list[i].name + "'s turn")
                multiple = player_list[i].get_alive()
                hop, event = random_card()
                bunny_num = player_list[i].furthest_bunny()
                if bunny_num == -10:
                    player_list[i] = None
                else:
                    count = 0
                    while event == -1 and \
                            (player_list[i].loc_list[bunny_num][1] + hop == board.get_hole() or board.board[
                            player_list[i].loc_list[bunny_num][1] + hop] == "occ" or not board.is_location_valid(
                            player_list[i].loc_list[bunny_num][1], player_list[i].loc_list[bunny_num][1] + hop)):
                        new_bunny = player_list[i].next_bunny(count)
                        if new_bunny != -2:
                            bunny_num = new_bunny
                        count += 1
                        if count == 4 and player_list[i].loc_list[bunny_num][1] + hop == board.get_hole():
                            break
                        elif count == 4 or (multiple == -1 and player_list[i].loc_list[bunny_num][1] +
                                            hop != board.get_hole()):
                            hop, event = random_card()
                            count = 0

                    if event == -1:
                        print("bunny number " + str(bunny_num+1) + " is playing and he will hop " + str(hop) +
                              " spaces")
                        current = player_list[i].loc_list[bunny_num][1]
                        board.set_loc(current + hop, player_list[i].loc_list[bunny_num][1])
                        print("bunny was at " + str(player_list[i].loc_list[bunny_num][1]))
                        player_list[i].loc_list[bunny_num][1] = current
                        player_list[i].loc_list[bunny_num][1] += hop
                        if player_list[i].loc_list[bunny_num][1] >= 26:
                            print("bunny is at 26 (final spot)")
                            print("Number of dead bunnies: " + str(dead_bunny) + "\nNumber of dead players: " +
                                  str(dead_player))
                            print("Game Over!\n" + player_list[i].name + " Won!!\n")
                            return

                        else:
                            print("bunny is at " + str(player_list[i].loc_list[bunny_num][1]))
                        if player_list[i].loc_list[bunny_num][1] == board.get_hole():
                            player_list[i].loc_list[bunny_num][1] = -2
                            print(player_list[i].name + "'s bunny number " + str(bunny_num + 1) + " " + random.choice(
                                sen_choice))
                            dead_bunny += 1
                            if multiple == -1:
                                print(player_list[i].name + " is out of the game.")
                                player_list[i] = None
                                dead_player += 1

                    else:
                        if board.board[hop] == "occ":
                            q, w = find_bunny(hop)
                            if q != -1:
                                player_list[q].loc_list[w][1] = -2
                                print(player_list[q].name + "'s bunny number " + str(player_list[q].loc_list[w][0]) +
                                      " " + random.choice(sen_choice))
                                dead_bunny += 1
                                if multiple == -1:
                                    print(player_list[q].name + " is out of the game.")
                                    player_list[q] = None
                                    dead_player += 1
                        if event == 1:
                            n = hop - 1
                            print("The mole was found")
                            if board.board[n] == "occ":
                                q, w = find_bunny(n)
                                if q != -1:
                                    player_list[q].loc_list[w][1] = -1
                                    board.board[n] = "empty"
                                    print("The mole appeared and knocked " + player_list[q].name + "'s bunny number " +
                                          str(player_list[q].loc_list[w][0]) + " down to the start")
                        elif event == 2:
                            if board.bridgeEnabled:
                                board.bridgeEnabled = False
                                print("Bridge lifted")
                            else:
                                board.bridgeEnabled = True
                                print("Bridge walkable")
                        elif event == 3:
                            if board.gateOpen:
                                board.gateOpen = False
                                print("Gate closed")
                            else:
                                board.gateOpen = True
                                print("Gate opened")
                                if board.board[24] == "occ":
                                    q, w = find_bunny(24)
                                    if q != -1:
                                        board.board[24] = "empty"
                                        if board.board[9] == "empty":
                                            player_list[q].loc_list[w][1] = 9
                                            board.board[9] = "occ"
                                            print("The gate knocked " + player_list[q].name + "'s bunny number " +
                                                  str(player_list[q].loc_list[w][0]) +
                                                  " down to spot number 9")
                                        else:
                                            player_list[q].loc_list[w][1] = -1
                                            print("The gate knocked " + player_list[q].name + "'s bunny number " + str(
                                                player_list[q].loc_list[w][0]) + " down to the start")
                        board.set_hole(hop)
                enter(dead_bunny, dead_player, board)

            else:
                boolean = False
                for s in range(len(player_list)):
                    if player_list[s] is not None:
                        boolean = True

                if not boolean:
                    print("Game Over. Everyone is dead. :(\n")
                    return


def again():
    while True:
        answer = input("Would you like to play again?\nEnter y for yes or n for no: ")
        answer = answer.lower()
        if answer == "yes" or answer == "y":
            return True
        elif answer == "no" or answer == "n":
            return False
        else:
            print("Invalid answer, try again.\n")


if __name__ == "__main__":
    play = True
    while play:
        run()
        play = again()
