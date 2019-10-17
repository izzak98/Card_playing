import pygame
import os
import random
import numpy
import time
import pandas

WIN_WIDTH = 1200
WIN_HEIGHT = 800
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "background.jpg")))
CARD_BACK = pygame.transform.scale(pygame.image.load(os.path.join("img", "purple_back.png")), (100, 150))
DATA = pandas.DataFrame({"Winner", "Starting Hand Player 1.1", "Starting Hand Player 1.2", "Starting Hand Player 1.3",
                         "Starting Hand Player 2.1", "Starting Hand Player 2.2", "Starting Hand Player 2.3",
                         "Biggest Add", "Most Played Card Player 1", "Most Played Card Player 2",
                         "Most Dangerous Card"})


class Card:
    def __init__(self, suit, val, true_val, ai_value):
        self.suit = suit
        self.value = val
        self.true_value = true_val
        image = pygame.image.load(os.path.join("img", str(self.value) + self.suit + ".png"))
        self.img = pygame.transform.scale(image, (100, 150))
        self.ai_value = ai_value

    def get_image(self):
        return self.img

    def get_value(self):
        return str(self.value) + self.suit

    def get_true_value(self):
        return str(self.true_value)

    def get_ai_value(self):
        return self.ai_value


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ["S", "C", "D", "H"]:
            self.cards.append(Card(s, "A", 14, 1))
            for v in range(2, 11):
                if v != 2 and v != 5 and v != 9 and v != 10:
                    self.cards.append(Card(s, v, v, v))
                elif v == 2:
                    self.cards.append(Card(s, v, "S2", 2))
                elif v == 5:
                    self.cards.append(Card(s, v, "S5", 5))
                elif v == 9:
                    self.cards.append(Card(s, v, "S9", 9))
                elif v == 10:
                    self.cards.append(Card(s, v, "S10", 10))

            self.cards.append(Card(s, "J", 11, 11))
            self.cards.append(Card(s, "Q", 12, 12))
            self.cards.append(Card(s, "K", 13, 13))

    def get_card_value(self, index):
        return self.cards[index].get_value()

    def get_card_image(self, index):
        return self.cards[index].get_image()

    def get_card_true_value(self, index):
        return self.cards[index].get_true_value()

    def get_ai_value(self, index):
        return self.cards[index].get_ai_value()

    def shuffle(self):
        for x in range(len(self.cards) - 1, 0, -1):
            r = random.randint(0, x)
            self.cards[x], self.cards[r] = self.cards[r], self.cards[x]


DECK = Deck()
DECK.shuffle()


def playing(hand, public, main_pile):
    vision = [0] * 35
    for x in range(len(hand)):
        vision[x] = DECK.get_card_true_value(hand[x])
    for x in range(len(public)):
        vision[x + 30] = DECK.get_card_true_value(public[x])
    if len(main_pile) >= 2:
        for x in range(2):
            vision[x + 33] = DECK.get_card_true_value(main_pile[len(main_pile) - (x + 1)])
    elif len(main_pile) >= 1:
        vision[33] = DECK.get_card_true_value(main_pile[len(main_pile) - 1])
    possible_card = []
    special_card = []
    if vision[33] == "S9":
        if str(vision[34]) in "S":
            main_man = vision[34][1]
        else:
            main_man = vision[34]
    else:
        main_man = vision[33]

    if len(hand) > 0:
        if main_man == "S5":
            for x in range(len(hand)):
                if vision[x][0] == "S":
                    special_card.append(vision[x])
                else:
                    if int(vision[x]) <= int(main_man[1]):
                        possible_card.append(vision[x])
        else:
            if len(main_pile) == 0 or "S" in str(main_man):
                for x in range(len(hand)):
                    if vision[x][0] == "S":
                        special_card.append(vision[x])
                    else:
                        possible_card.append(int(vision[x]))
            else:
                for x in range(len(hand)):
                    if vision[x][0] == "S":
                        special_card.append(vision[x])
                    else:
                        if int(vision[x]) >= int(main_man):
                            possible_card.append(int(vision[x]))
    else:
        if main_man == "S5":
            for x in range(len(public)):
                if vision[x + 30][0] == "S":
                    special_card.append(vision[x + 30])
                else:
                    if int(vision[x + 30]) <= int(main_man[1]):
                        possible_card.append(vision[x + 30])
        else:
            if len(main_pile) == 0 or "S" in str(main_man):
                for x in range(len(public)):
                    if str(vision[x + 30])[0] == "S":
                        special_card.append(vision[x + 30])
                    else:
                        possible_card.append(int(vision[x + 30]))
            else:
                for x in range(len(public)):
                    if str(vision[x + 30])[0] == "S":
                        special_card.append(vision[x + 30])
                    else:
                        if int(vision[x + 30]) >= int(main_man):
                            possible_card.append(int(vision[x + 30]))
    about_to_play = ""
    if len(possible_card) > 0:
        about_to_play = min(possible_card)
    elif len(special_card) > 0:
        for x in range(len(special_card)):
            if special_card[x] == "S9":
                about_to_play = special_card[x]
            if special_card[x] == "S5":
                about_to_play = special_card[x]
            if special_card[x] == "S2":
                about_to_play = special_card[x]
            if special_card[x] == "S10":
                about_to_play = special_card
    if about_to_play == "":
        if len(hand) > 0:
            out = 0
        else:
            for x in range(3):
                if vision[x + 30] != 0:
                    possible_card.append(possible_card.append(int(vision[x + 30])))
            out = min(possible_card)
    else:
        if isinstance(about_to_play, list):
            out = vision.index(str(about_to_play[0]))
        else:
            out = vision.index(str(about_to_play))

    if len(hand) == 0:
        out -= 30

    return out


def change_turn(turn):
    if turn == 1:
        turn = 2
    elif turn == 2:
        turn = 1
    return turn


def draw_public(win, public, x, y, offset):
    for i in range(len(public)):
        win.blit(DECK.get_card_image(public[i]), (x, y))
        x += offset


def draw_hand(win, hand, x, y, offset, add):
    for i in range(len(hand)):
        win.blit(DECK.get_card_image(hand[i]), (x, y))
        if add:
            x += offset
        else:
            x -= offset


class Drawing:
    def __init__(self):
        self.public1_x = 400
        self.public1_y = 500
        self.public1_offset = 150

        self.public2_x = 400
        self.public2_y = 150
        self.public2_offset = 150

        self.main_pile_x = 550
        self.main_pile_y = 325

        self.discard_x = 250
        self.discard_y = 325

        self.back_x = 650
        self.back_y = 325

        self.hand1_x = 1100
        self.hand1_y = 700
        self.hand1_offset = 100
        self.hand1_add = False

        self.hand2_x = 0
        self.hand2_y = -50
        self.hand2_offset = 100
        self.hand2_add = True

    def draw_main_pile(self, win, main_pile):
        if len(main_pile) != 0:
            win.blit(DECK.get_card_image(main_pile[len(main_pile) - 1]), (self.main_pile_x, self.main_pile_y))

    def draw_back(self, win, index):
        if index < 52:
            win.blit(CARD_BACK, (self.back_x, self.back_y))

    def draw_discard(self, win, discard):
        if len(discard) != 0:
            win.blit(DECK.get_card_image(discard[len(discard) - 1]), (self.discard_x, self.discard_y))

    def draw_all(self, win, public1, public2, hand1, hand2, main_pile, discard, index):
        win.blit(BG_IMG, (0, 0))

        draw_hand(win, hand1, self.hand1_x, self.hand1_y, self.hand1_offset, self.hand1_add)
        draw_hand(win, hand2, self.hand2_x, self.hand2_y, self.hand2_offset, self.hand2_add)

        draw_public(win, public1, self.public1_x, self.public1_y, self.public1_offset)
        draw_public(win, public2, self.public2_x, self.public2_y, self.public2_offset)

        self.draw_main_pile(win, main_pile)
        self.draw_discard(win, discard)
        self.draw_back(win, index)


def get_recents(main_pile, most_recent, second_most_recent, third_most_recent, fourth_most_recent):
    if len(main_pile) > 0:
        most_recent = DECK.get_card_true_value(main_pile[len(main_pile) - 1])
    if len(main_pile) > 1:
        second_most_recent = DECK.get_card_true_value(main_pile[len(main_pile) - 2])
    if len(main_pile) > 2:
        third_most_recent = DECK.get_card_true_value(main_pile[len(main_pile) - 3])
    if len(main_pile) > 3:
        fourth_most_recent = DECK.get_card_true_value(main_pile[len(main_pile) - 4])
    return most_recent, second_most_recent, third_most_recent, fourth_most_recent


def played_special(most_recent, main_pile, discard, turn, add, dang):
    if most_recent == "S10":
        for x in range(len(main_pile)):
            discard.append(main_pile[x])
            add = x
            dang = DECK.get_card_true_value(main_pile[x])
        main_pile = []
    else:
        turn = change_turn(turn)
    return main_pile, turn, add, dang


def played_on_special(most_recent, second_most_recent, third_most_recent, hand, main_pile, turn, add, dang, appe):
    if second_most_recent == "S2":
        change_turn(turn)
    elif second_most_recent == "S5":
        if int(most_recent) > 5:
            for x in range(len(main_pile)):
                appe.append(main_pile[x])
                add = x
                dang = DECK.get_card_true_value(main_pile[x])
            main_pile = []
        else:
            turn = change_turn(turn)
    elif second_most_recent == "S9":
        if "S" in str(third_most_recent):
            if int(most_recent) < int(third_most_recent[1]):
                for x in range(len(main_pile)):
                    appe.append(main_pile[x])
                    add = x
                    dang = DECK.get_card_true_value(main_pile[x])
                main_pile = []
            else:
                turn = change_turn(turn)
        elif int(most_recent) < int(third_most_recent):
            for x in range(len(main_pile)):
                appe.append(main_pile[x])
                add = x
                dang = DECK.get_card_true_value(main_pile[x])
            main_pile = []
        else:
            turn = change_turn(turn)
    return main_pile, turn, hand, add, dang, appe


def play(main_pile, hand, discard, turn, add, dang, appe):
    most_recent = 0
    second_most_recent = 0
    third_most_recent = 0
    fourth_most_recent = 0
    most_recent, second_most_recent, third_most_recent, fourth_most_recent = get_recents(main_pile, most_recent,
                                                                                         second_most_recent,
                                                                                         third_most_recent,
                                                                                         fourth_most_recent)
    if most_recent == second_most_recent and most_recent == third_most_recent and most_recent == fourth_most_recent:
        for x in range(len(main_pile)):
            discard.append(main_pile[x])
        main_pile = []
    elif "S" in most_recent:
        main_pile, turn, add, dang = played_special(most_recent, main_pile, discard, turn, add, dang)
    elif "S" in str(second_most_recent):
        main_pile, turn, hand, add, dang, appe = played_on_special(most_recent, second_most_recent,
                                                                   third_most_recent, hand, main_pile, turn, add, dang,
                                                                   appe)
    elif int(most_recent) < int(second_most_recent):
        for x in range(len(main_pile)):
            appe.append(main_pile[x])
            add = x
            dang = DECK.get_card_true_value(main_pile[x])
        main_pile = []
    else:
        turn = change_turn(turn)
    return main_pile, turn, add, dang, appe


def main():
    runtime = 0
    while runtime != 1:
        print(runtime)
        DECK.shuffle()

        public1 = [0, 1, 2]
        public2 = [3, 4, 5]
        hand1 = [6, 7, 8]
        hand2 = [9, 10, 11]
        main_pile = [12]
        index = 13
        discard = []
        turn = 1
        run = True
        dec = 0
        draw = Drawing()
        winner = ""
        starting_hand1 = []
        starting_hand2 = []
        biggest_add = 0
        most_played1 = ""
        most_played2 = ""
        most_dangerous = ""
        for x in range(3):
            starting_hand1.append(DECK.get_card_true_value(hand1[x]))
            starting_hand2.append(DECK.get_card_true_value(hand2[x]))
        played1 = []
        played2 = []
        dang = ""
        dang_list = []
        sec = time.time()
        while run:
            """if time.time() - sec > 15:
                runtime -= 1
                run = False"""
            try:
                appe = []
                add = 0
                if len(hand1) == 0 and len(public1) == 0:
                    winner = 1
                    run = False
                if len(hand2) == 0 and len(public2) == 0:
                    winner = 2
                    run = False
                if len(hand1) >= 30:
                    winner = 2
                    run = False
                if len(hand2) >= 30:
                    winner = 1
                    run = False

                win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                draw.draw_all(win, public1, public2, hand1, hand2, main_pile, discard, index)
                pygame.display.update()
                time.sleep(0.5)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                        quit()
                if turn == 1:
                    output1 = playing(hand1, public1, main_pile)
                    played1.append(DECK.get_card_true_value(output1))
                    if len(hand1) != 0:
                        main_pile.append(hand1[output1])
                        hand1.remove(hand1[output1])
                        if index < 52 and len(hand1) <= 2:
                            hand1.append(index)
                            index += 1
                        main_pile, turn, add, dang, appe = play(main_pile, hand1, discard, turn, add, dang, appe)
                        for x in range(len(appe)):
                            hand1.append(appe[x])
                    else:
                        main_pile.append(public1[output1])
                        public1.remove(public1[output1])
                        main_pile, turn, add, dang, appe = play(main_pile, public1, discard, turn, add, dang, appe)
                        for x in range(len(appe)):
                            hand1.append(appe[x])
                elif turn == 2:
                    output2 = playing(hand2, public2, main_pile)
                    played2.append(DECK.get_card_true_value(output2))
                    if len(hand2) != 0:
                        main_pile.append(hand2[output2])
                        hand2.remove(hand2[output2])
                        if index < 52 and len(hand2) <= 2:
                            hand2.append(index)
                            index += 2
                        main_pile, turn, add, dang, appe = play(main_pile, hand2, discard, turn, add, dang, appe)
                        for x in range(len(appe)):
                            hand2.append(appe[x])
                    else:
                        main_pile.append(public2[output2])
                        public2.remove(public2[output2])
                        main_pile, turn, add, dang, appe = play(main_pile, public2, discard, turn, add, dang, appe)
                        for x in range(len(appe)):
                            hand2.append(appe[x])
                if add > biggest_add:
                    biggest_add = add
                dang_list.append(dang)
            except :
                runtime -= 1
                print("Fail")
                run = False
        runtime += 1

        if len(played1) != 0 and len(played2) != 0 and winner != "":
            most_played1 = max(set(played1), key=played1.count)
            most_played2 = max(set(played2), key=played2.count)
            most_dangerous = max(set(dang_list), key=dang_list.count)
            global DATA
            DATA = DATA.append(
                {"Winner": winner, "Starting Hand Player 1.1": starting_hand1[0],
                 "Starting Hand Player 1.2": starting_hand1[1],
                 "Starting Hand Player 1.3": starting_hand1[2], "Starting Hand Player 2.1": starting_hand2[0],
                 "Starting Hand Player 2.2": starting_hand2[1], "Starting Hand Player 2.3": starting_hand2[2],
                 "Biggest Add": biggest_add, "Most Played Card Player 1": most_played1,
                 "Most Played Card Player 2": most_played2, "Most Dangerous Card": most_dangerous},
                ignore_index=True)


main()
#export = DATA.to_csv(r'C:\Users\Ísak\Desktop\export_dataframe.csv', index = None, header=True)
