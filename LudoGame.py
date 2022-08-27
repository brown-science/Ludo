# Author: John Brown
# GitHub username: brown_science
# Date 8/2/2022
# Description: Text-based implementation of the game Ludo. The user passes a list of at least 2 player positions:
# A, B, C, or D. As well as a list of tuples which represent turns that a player at a given position takes. e.g.
# ('A', 6) would move the player 6 spaces. See the README for the game rules


class Player:
    """
    Contains information about the player, the position of their tokens, the state of the player (playing or done), and
    information about the Ludo board. The LudoGame class will invoke this class when LudoGame.Play_game is called
    """
    def __init__(self, letter, info=None, p_step_count=-1, q_step_count=-1):
        """
        Players are defined by their position/letter, this tells us where the player starts on the board. The Player
        objects also keep track of how many steps each of their tokens have taken, p_step_count and q_step_count.
        Player objects additionally contain a dictionary of information about their tokens: token current positions and
        the start and end position for the tokens, as well as the 'state' of a player: whether they are currently playing
        or if they've completed the game
        """
        self._info = info
        self._letter = letter
        self._p_step_count = p_step_count
        self._q_step_count = q_step_count

        if letter == "A":
            A_info = {'start': 1, 'end': 50, 'p_pos': -1, 'q_pos': -1, 'state': 'playing'}
            self._info = {self._letter : A_info}

        if letter == "B":
            B_info = {'start': 15, 'end': 8, 'p_pos': -1, 'q_pos': -1, 'state': 'playing'}
            self._info = {self._letter : B_info}

        if letter == "C":
            C_info = {'start': 29, 'end': 22, 'p_pos': -1, 'q_pos': -1, 'state': 'playing'}
            self._info = {self._letter: C_info}

        if letter == "D":
            D_info = {'start': 43, 'end': 36, 'p_pos': -1, 'q_pos': -1, 'state': 'playing'}
            self._info = {self._letter : D_info}

    def get_player_letter(self):
        """Returns a player's letter/position"""
        return self._letter

    def get_player_info(self):
        """Returns the player info"""
        return self._info

    def get_start(self):
        """Returns the start position given a players letter"""
        player_info = self._info[self._letter]
        return player_info.get('start')

    def get_end(self):
        """Returns the end position given a players letter"""
        player_info = self._info[self._letter]
        return player_info.get('end')

    def get_completed(self):
        """Returns True if the player has finished the game, otherwise False"""
        state = self._info[self._letter].get('state')
        return state == 'done'

    def get_token_p_step_count(self):
        """Returns the total steps token p has moved"""
        return self._p_step_count

    def get_token_q_step_count(self):
        """Returns the total steps token q has moved"""
        return self._q_step_count

    def update_step_count(self, token, num):
        """
        Updates the step count for a player's token, used in the move_token method of the LudoGame class
        token refers to either token p or q, num is the nuber of steps taken, method is used by LudoGame.move_token
        """
        token = str(token)
        if token == 'p': self._p_step_count += num
        if token == 'q': self._q_step_count += num

    def set_step_count(self, token, num):
        """
        manually sets the step count, used for the bounce back mechanism in LudoGame.move_token
        token refers to either token p or q, num is set to step count fo the token passed
        """
        if token == 'p': self._p_step_count = num
        if token == 'q': self._q_step_count = num

    def get_space_name(self, token_steps):
        """
        Takes the total steps taken by a token as a param, returns
        the space that token is on 'H' refers to home yard pos, 'R'
        refers to the ready to go pos
        """

        if token_steps == -1:
            return 'H'
        if token_steps == 0:
            return 'R'

        if self._letter == 'A':
            if 0 < token_steps <= 50:
                board = list(range(0, 51))
                return str(board[token_steps])

            if token_steps > 50:
                row = ['', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'E']
                token_steps -= 50
                return str(row[token_steps])

        if self._letter == 'B':
            if 0 < token_steps <= 50:
                board = list(range(15, 57))
                board.extend([1, 2, 3, 4, 5, 6, 7, 8])
                board.insert(0, 0)
                return str(board[token_steps])

            if token_steps > 50:
                row = ['', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'E']
                token_steps -= 50
                return str(row[token_steps])

        if self._letter == 'C':
            if 0 < token_steps <= 50:
                board = list(range(29, 57))
                board.extend(range(1,29))
                board.insert(0, 0)
                return str(board[token_steps])

            if token_steps > 50:
                row = ['', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'E']
                token_steps -= 50
                return str(row[token_steps])

        if self._letter == 'D':
            if 0 < token_steps <= 50:
                board = list(range(43, 57))
                board.extend(range(1, 44))
                board.insert(0, 0)
                return str(board[token_steps])

            if token_steps > 50:
                row = ['', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'E']
                token_steps -= 50
                return str(row[token_steps])


class LudoGame:
    """
    Creates an instance of a Ludo game, the game can be played when the LudoGame object's play_game method is
    called and given a list of player positions and turns
    """
    def __init__(self, player_list=None):
        """Creates and stores a list of players"""
        self._player_list = player_list
        if player_list is None: self._player_list = []

    def get_player_by_position(self, player_letter):
        """
        Takes the player letter string as an argument, returns
        the player object associated with that letter
        """

        letter_list = []
        for player in self._player_list:
            letter_list.append(player.get_player_letter())

        for player in self._player_list:
            if player_letter in letter_list and player.get_player_letter() == player_letter:
                return player
        return "Player not found!"

    def move_token(self, player, token_name, steps, kick=None, kick_token=None):
        """
        Moves player tokens, this method handles kicking opponent player tokens as well
        :param player: Player object
        :param token_name: 'p' or 'q'
        :param steps: number of steps the token should move, determined by the current turn tuple
        :param kick: is not Not iff an opposing token can be kicked
        :param kick_token: specifies which token should be kicked
        """

        player_letter = player.get_player_letter()
        player_info = player.get_player_info()[player_letter]
        if token_name == 'p': token_idx = 'p_pos'
        if token_name == 'q': token_idx = 'q_pos'

        if player_info[token_idx] == -1:
            player.update_step_count(token_name, 1)

#Kicks opponents
        elif type(kick) == dict:
            if kick.get('p', None) is not None:
                opp_info = kick['p']
                opp_token = kick_token
            if kick.get('q', None) is not None:
                opp_info = kick['q']
                opp_token = kick_token
            opp_letter = list(opp_info)[0]
            opp = self.get_player_by_position(opp_letter)
            kick_pos = opp_info[opp_letter]
            if opp_token == 'p':
                opp.get_player_info()[opp_letter]['p_pos'] = -1
                opp.set_step_count('p', -1)
            if opp_token == 'q':
                opp.get_player_info()[opp_letter]['q_pos'] = -1
                opp.set_step_count('q', -1)
            player.update_step_count(token_name, steps)

            for extra_opp in self._player_list:
                if extra_opp == player:
                    pass
                else:
                    extra_opp_letter = extra_opp.get_player_letter()
                    e_opp_info = extra_opp.get_player_info()[extra_opp_letter]
                    if e_opp_info['p_pos'] == kick_pos:
                        e_opp_info['p_pos'] = -1
                        extra_opp.set_step_count('p', -1)
                    if e_opp_info['q_pos'] == kick_pos:
                        e_opp_info['q_pos'] = -1
                        extra_opp.set_step_count('q', -1)




# 2 elif statements move token around board, not home row
        elif player.get_token_p_step_count() < 51 and token_name == 'p':
            player.update_step_count(token_name, steps)

        elif player.get_token_q_step_count() < 51 and token_name == 'q':
            player.update_step_count(token_name, steps)

# Moves token through the home row
        elif player.get_token_p_step_count() > 50 and token_name == 'p':
            if player.get_token_p_step_count() + steps <= 57:
                player.update_step_count(token_name, steps)

            elif player.get_token_p_step_count() + steps > 57:
                steps_over = (player.get_token_p_step_count() + steps) - 57
                new_pos = 57 - steps_over
                player.set_step_count(token_name, new_pos)

        elif player.get_token_q_step_count() > 50 and token_name == 'q':
            if player.get_token_q_step_count() + steps <= 57:
                player.update_step_count(token_name, steps)

        elif player.get_token_q_step_count() + steps > 57:
            steps_over = (player.get_token_q_step_count() + steps) - 57
            new_pos = 57 - steps_over
            player.set_step_count(token_name, new_pos)

    def play_game(self, players, turns_list, opp_pos=None):
        """
        Method used for playing the game, it contains a decision-making algorithm which prioritizes player moves
        according to the priorities listed in the README
        :param players: List of players min:2 max:4  A, B, C, or D
        :param turns_list: list of tuples w/ player letter/position and number of steps to take. e.g. ('A', 6)
        :param opp_pos: Turns into a list of opponent positions, updates every turn
        """
        if opp_pos is None: opp_pos = []
# Generates player objects and self._player_list
        list_len = len(players) - 1
        itr = 0
        for player in players:
            if itr <= list_len and players[itr] == 'A':
                player_A = Player('A')
                self._player_list.append(player_A)
                itr += 1

            if itr <= list_len and players[itr] == 'B':
                player_B = Player('B')
                self._player_list.append(player_B)
                itr += 1

            if itr <= list_len and players[itr] == 'C':
                player_C = Player('C')
                self._player_list.append(player_C)
                itr += 1

            if itr <= list_len and players[itr] == 'D':
                player_D = Player('D')
                self._player_list.append(player_D)
                itr += 1

# Handles turns
        for turn in turns_list:
            player_letter = turn[0]
            player = self.get_player_by_position(player_letter)
            player_info = player.get_player_info().get(player_letter)

# Initializes opponent positions, used for kicking opponents
            p_opp_pos = {}
            q_opp_pos = {}
            p_temp = {}
            q_temp = {}
            p_overlap_opp = {}
            q_overlap_opp = {}
            for opp in self._player_list:
                if opp.get_player_letter() == player_letter:
                    pass
                else:
                    opp_letter = opp.get_player_letter()
                    opp_info = opp.get_player_info().get(opp_letter)
                    p_opp_pos[opp_letter] = opp_info.get('p_pos')
                    q_opp_pos[opp_letter] = opp_info.get('q_pos')

        # p_overlap_opp is not empty iff player can kick an opponents' p token
            for pair in p_opp_pos:
                if type(player_info['p_pos']) == int and player_info['p_pos'] > 0 and player_info['p_pos'] + turn[1] == p_opp_pos[pair]:
                    p_temp[pair] = p_opp_pos[pair]
                    p_overlap_opp['p'] = p_temp
                if player_info['p_pos'] == 0 and (player_info['start'] -1) + turn[1] == p_opp_pos[pair]:
                    p_temp[pair] = p_opp_pos[pair]
                    p_overlap_opp['p'] = p_temp
                if type(player_info['q_pos']) == int and player_info['q_pos'] > 0 and player_info['q_pos'] + turn[1] == p_opp_pos[pair]:
                    p_temp[pair] = p_opp_pos[pair]
                    p_overlap_opp['q'] = p_temp
                if player_info['q_pos'] == 0 and (player_info['start'] -1) + turn[1] == p_opp_pos[pair]:
                    p_temp[pair] = p_opp_pos[pair]
                    p_overlap_opp['q'] = p_temp


        # q_overlap_opp is not empty iff player can kick an opponents' q token
            for pair in q_opp_pos:
                if type(player_info['p_pos']) == int and player_info['p_pos'] + turn[1] == q_opp_pos[pair]:
                    q_temp[pair] = q_opp_pos[pair]
                    q_overlap_opp['p'] = q_temp
                if player_info['p_pos'] == 0 and (player_info['start'] - 1) + turn[1] == q_opp_pos[pair]:
                    q_temp[pair] = q_opp_pos[pair]
                    q_overlap_opp['p'] = q_temp
                if type(player_info['q_pos']) == int and player_info['q_pos'] + turn[1] == q_opp_pos[pair]:
                    q_temp[pair] = q_opp_pos[pair]
                    q_overlap_opp['q'] = q_temp
                if player_info['q_pos'] == 0 and (player_info['start'] -1) + turn[1] == q_opp_pos[pair]:
                    q_temp[pair] = q_opp_pos[pair]
                    q_overlap_opp['q'] = q_temp

# Simple decision-making algorithm for moving tokens
        # Priority 1: move token out of home yard
            if turn[1] == 6 and player_info.get('p_pos') == -1:
                self.move_token(player, 'p', turn[1])
                player_info['p_pos'] = 0
                continue
            if turn[1] == 6 and player_info.get('p_pos') != -1 and player_info.get('q_pos') == -1:
                self.move_token(player, 'q', turn[1])
                player_info['q_pos'] = 0
                continue

            if player_info['p_pos'] == 0 and len(p_overlap_opp) == 0:
                if len(q_overlap_opp) == 0:
                    self.move_token(player, 'p', turn[1])
                    player_info['p_pos'] = int(player.get_space_name(turn[1]))
                    continue

            if player_info['q_pos'] == 0 and len(q_overlap_opp) == 0:
                if len(p_overlap_opp) == 0:
                    self.move_token(player, 'q', turn[1])
                    player_info['q_pos'] = int(player.get_space_name(turn[1]))
                    continue


            if 0 <= player.get_token_p_step_count() < 57 or 0 <= player.get_token_q_step_count() < 57:

# Priority 2: move token to end space if possible
                if player.get_token_p_step_count() + turn[1] == 57:
                    self.move_token(player, 'p', turn[1])
                    player_info['p_pos'] = player.get_space_name(player.get_token_p_step_count())
                    if player_info['p_pos'] == 'E' and player_info['q_pos'] == 'E':
                        player_info['state'] = 'done'
                    continue
                if player.get_token_q_step_count() + turn[1] == 57:
                    self.move_token(player, 'q', turn[1])
                    player_info['q_pos'] = player.get_space_name(player.get_token_q_step_count())
                    if player_info['p_pos'] == 'E' and player_info['q_pos'] == 'E':
                        player_info['state'] = 'done'
                    continue

# Priority 3: If an opponent's token can be kicked back to their home base, do it
            # If player can kick an opponents' p token
                if len(p_overlap_opp) != 0:
                    same_spot = False
                    token = list(p_overlap_opp)[0]
                    if token == 'p': other_token = 'q'
                    if token == 'q': other_token = 'p'
                    if player_info['p_pos'] == player_info['q_pos'] != -1 or 0 and player.get_token_p_step_count() < 51: same_spot = True
                    kick = p_overlap_opp
                    self.move_token(player, token, turn[1], kick, 'p')

                    player_info['p_pos'] = int(player.get_space_name(player.get_token_p_step_count()))
                    if same_spot is True:
                        self.move_token(player, other_token, turn[1])
                        player_info['q_pos'] = int(player.get_space_name(player.get_token_q_step_count()))
                        same_spot = False
                    continue


            # If player can kick opponents' q token
                if len(q_overlap_opp) != 0:
                    same_spot = False
                    token = list(q_overlap_opp)[0]
                    if token == 'p': other_token = 'q'
                    if token == 'q': other_token = 'p'
                    if player_info['p_pos'] == player_info['q_pos'] != -1 or 0 and player.get_token_p_step_count() < 51: same_spot = True
                    kick = q_overlap_opp
                    self.move_token(player, token, turn[1], kick, 'q')
                    player_info['q_pos'] = player.get_space_name(player.get_token_q_step_count())
                    if same_spot is True:
                        self.move_token(player, other_token, turn[1])
                        player_info['p_pos'] = player.get_space_name(player.get_token_p_step_count())
                        same_spot = False
                    continue

# Priority 4: Move the token furthest from the finishing square
                if player.get_token_p_step_count() > player.get_token_q_step_count() and player_info.get('q_pos') != -1 and player.get_token_q_step_count() < 57:
                    if player_info['q_pos'] != 'E': self.move_token(player, 'q', turn[1])
                    if 0 < player.get_token_q_step_count() < 51:
                        player_info['q_pos'] = int(player.get_space_name(player.get_token_q_step_count()))
                    if player.get_token_q_step_count() > 50 or player.get_token_q_step_count() <= 0:
                        player_info['q_pos'] = player.get_space_name(player.get_token_q_step_count())
                    continue
                if player.get_token_p_step_count() < player.get_token_q_step_count() and player.get_token_p_step_count() < 57:
                    if player_info['p_pos'] != 'E': self.move_token(player, 'p', turn[1])
                    if 0 < player.get_token_p_step_count() < 51:
                        player_info['p_pos'] = int(player.get_space_name(player.get_token_p_step_count()))
                    if player.get_token_p_step_count() > 50 or player.get_token_p_step_count() <= 0:
                        player_info['p_pos'] = player.get_space_name(player.get_token_p_step_count())

                    continue
                if player_info.get('p_pos') == player_info.get('q_pos') and player_info.get('q_pos') > 0:
                    if player_info['p_pos'] and player_info['q_pos'] != 'E':
                        self.move_token(player, 'p', turn[1])
                        self.move_token(player, 'q', turn[1])
                        if 0 < player.get_token_p_step_count() < 51:
                            player_info['p_pos'] = int(player.get_space_name(player.get_token_p_step_count()))
                            player_info['q_pos'] = int(player.get_space_name(player.get_token_p_step_count()))
                        if player.get_token_p_step_count() > 50 or player.get_token_p_step_count() <= 0:
                            player_info['p_pos'] = player.get_space_name(player.get_token_p_step_count())
                            player_info['q_pos'] = player.get_space_name(player.get_token_p_step_count())
                else:
                    if player.get_token_p_step_count() < 57 and player_info['p_pos'] != 'E':
                        self.move_token(player, 'p', turn[1])
                        if 0 < player.get_token_p_step_count() < 51:
                            player_info['p_pos'] = int(player.get_space_name(player.get_token_p_step_count()))
                        if player.get_token_p_step_count() > 50 or player.get_token_p_step_count() <= 0:
                            player_info['p_pos'] = player.get_space_name(player.get_token_p_step_count())



# This code runs if one piece is still in the home yard
            else:
                if player.get_token_p_step_count() < 57 and player_info['p_pos'] != 'E':
                    self.move_token(player, 'p', turn[1])
                    if 0 < player.get_token_p_step_count() < 51:
                        player_info['p_pos'] = int(player.get_space_name(player.get_token_p_step_count()))
                    if player.get_token_p_step_count() > 50 or player.get_token_p_step_count() <= 0:
                        player_info['p_pos'] = player.get_space_name(player.get_token_p_step_count())

# Returns the state of the board after all turns have passed
        pos_list = []
        for element in self._player_list:
            pos_list.append(str(element.get_space_name(element.get_token_p_step_count())))
            pos_list.append(str(element.get_space_name(element.get_token_q_step_count())))
        return pos_list


                                 ############################## TEST CASES ####################################


# # Case 0
# players = ['A', 'B']
# turns = [('A', 6), ('A', 4), ('A', 5), ('A', 4), ('B', 6), ('B', 4), ('B', 1), ('B', 2), ('A', 6), ('A', 4), ('A', 6), ('A', 3), ('A', 5), ('A', 1), ('A', 5), ('A', 4)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# player_A = game.get_player_by_position('A')
# C0_T1 = player_A.get_completed()
# C0_T2 = player_A.get_token_p_step_count()
# C0_T3 =current_tokens_space
# player_B = game.get_player_by_position('B')
# C0_T4 = player_B.get_space_name(55)
# C0_T3_list = ['28','28', '21', 'H']
#
# if C0_T1 is False and C0_T2 == 28 and C0_T3 == C0_T3_list and C0_T4 == 'B5':
#     print("Case 0: PASS")
# else: print("FAILED Case 0")
#
#
#
# # Case 1
# players = ['A','B','C','D']
# turns = [('A', 6),('A', 1),('B', 6),('B', 2),('C', 6),('C', 3),('D', 6),('D', 4)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C1 = current_tokens_space
# C1_list = ['1', 'H', '16', 'H', '31', 'H', '46', 'H']
#
# if C1 == C1_list:
#     print("Case 1: PASS")
# else: print("FAILED Case 1")
#
# # Case 2:
# players = ['A','B']
# turns = [('B', 6),('B', 4),('B', 5),('B', 4),('B', 4),('B', 3),('B', 4),('B', 5),('B', 4),('B', 4),('B', 5),('B', 4),('B', 1),('B', 4),('B', 5),('B', 5),('B', 5)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C2 = current_tokens_space
# C2_list = ['H', 'H', 'B6', 'H']
#
# if C2 == C2_list:
#     print("Case 2: PASS")
# else: print("FAILED Case 2")
#
# # Case 3:
# players = ['A','B']
# turns = [('A', 6),('A', 3),('A', 6),('A', 3),('A', 6),('A', 5),('A', 4),('A', 6),('A', 4)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C3 = current_tokens_space
# C3_list = ['28', '28', 'H', 'H']
#
# if C3 == C3_list:
#     print("Case 3: PASS")
# else: print("FAILED Case 3")
#
# # Case 4:
# players = ['A','C']
# turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 5),('A', 6),('A', 4),('A', 6),('A', 4),('A', 6),('A', 6),('A', 6),('A', 4),('A', 6),('A', 6),('C', 6),('C', 4)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C4 = current_tokens_space
# C4_list = ['33', 'H', '32', 'H']
#
# if C4 == C4_list:
#     print("Case 4: PASS")
# else: print("FAILED Case 4")
#
# #Case 5:
# players = ['A','B']
# turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 5),('A', 6),('A', 4),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 6),('A', 4),('A', 6),('A', 3),('A', 6),('B', 6),('A', 6)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# player_A = game.get_player_by_position('A')
# C5 = current_tokens_space
# C5_T2 = player_A.get_completed()
# C5_list = ['E', 'E', 'R', 'H']
#
# if C5 == C5_list and C5_T2 is True:
#     print("Case 5: PASS")
# else: print("FAILED Case 5")
#
# # Case 6:
# players = ['A','B']
# turns = [('A', 6),('A', 2),('A', 2),('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('B', 6),('B', 3),('A', 6),('A', 3)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C6 = current_tokens_space
# C6_list = ['3', 'H', '17', 'H']
#
# if C6 == C6_list:
#     print("Case 6: PASS")
# else: print("FAILED Case 6")
#
# # Case 7:
# players = ['A','B']
# turns = [('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('A', 4),('A', 5),('A', 4),('A', 5),('A', 5),('A', 3),('A', 5),('A', 3),('A', 6)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C7 = current_tokens_space
# C7_list = ['A1', 'R', 'H', 'H']
#
# if C7 == C7_list:
#     print("Case 7: PASS")
# else: print("FAILED Case 7")
#
# # Case 8:
# players = ['A','B']
# turns = [('A', 6),('A', 4),('A', 5),('A', 4),('A', 4),('A', 4),('A', 5),('A', 4),('A', 5),('A', 5),('A', 3),('A', 5),('A', 5),('A', 6),('A', 5),('A', 5),('A', 3),('B', 6),('B', 3),('A', 4)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C8 = current_tokens_space
# C8_list = ['E', '13', '17', 'H']
#
# if C8 == C8_list:
#     print("Case 8: PASS")
# else: print("FAILED Case 8")
#
# # Case 9:
# players = ['A','B']
# turns = [('A', 6),('A', 4),('A', 4),('A', 4),('A', 6),('A', 5),('A', 3),('B', 6),('B', 2),('A', 2),('A', 4)]
# game = LudoGame()
# current_tokens_space = game.play_game(players, turns)
# C9 = current_tokens_space
# C9_list = ['16', '10', 'H', 'H']
#
# if C9 == C9_list:
#     print("Case 9: PASS")
# else: print("FAILED Case 9")




