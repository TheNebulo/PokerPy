import cards_manager, importlib
from copy import deepcopy

class Player:
    def __init__(self, name: str, starting_balance: int, script_path: str):
        self.name = name
        self.balance = starting_balance
        self.current_bet = 0
        self.bought_in = False
        self.folded = False
        self.hand = None
        self.script = __import__(script_path)

class Game:
    def __init__(self, players: list[Player], buy_in_cost: int):
        self.players = players
        self.non_folded_player_count = len(players)
        self.buy_in_cost = buy_in_cost
        self.pot = 0
        self.deck = cards_manager.Deck()
        self.deck.shuffle_cards()
        self.board_cards = []
        self.round_count = 0
        self.raise_count = 0
        self.current_check_value = 0
        self.game_ended = False
        self.winner = None
        
        for player in self.players:
            player.hand = self.deck.draw_cards(2)
                
    def run_game(self):
        self.buy_in_round()
        
        for r in range(1, 4):
            if not self.game_ended:
                self.round(r)
                
        return self.winner
    
    def buy_in_round(self):
        for player in self.players:
            
            opponent_states = []
            
            for op in self.players:
                if op != player:
                    opponent_states.append({"name": op.name, "balance": op.balance, "bought_in" : op.bought_in, "folded": op.folded})
            
            try:
                response = player.script.on_confirm_buy_in(
                    balance = player.balance,
                    hand = player.hand,
                    opponents = opponent_states,
                    buy_in_cost = self.buy_in_cost
                )
            except Exception as e:
                player.folded = True
                self.non_folded_player_count -= 1
                try: player.script.error_fold(f"Buy in function failed to execute because: {e}")
                except: pass
                continue              
            
            if response == True:
                if player.balance >= self.buy_in_cost:
                    player.balance -= self.buy_in_cost
                    self.pot += self.buy_in_cost
                else:
                    player.folded = True
                    self.non_folded_player_count -= 1
                    try: player.script.error_fold("Not enough balance for attempted buy in.")
                    except: pass
            else:
                player.folded = True
                self.non_folded_player_count -= 1
                if response != False: 
                    try: player.script.error_fold("No valid response provided for buy in.")
                    except: pass
            
    def round(self, betting_round: int):
        self.round_count = betting_round
        self.current_check_value = 0
        self.raise_count = 0
        last_raiser = None
        
        if betting_round == 1:
            self.board_cards += self.deck.draw_cards(3)
        else:
            self.board_cards += self.deck.draw_cards(1)

        while True:
            active = False
            for player in self.players:
                if player.folded:
                    continue

                if last_raiser == player or sum(1 for p in self.players if not p.folded) == 1:
                    break

                opponent_states = []
            
                for op in self.players:
                    if op != player:
                        opponent_states.append({"name": op.name, "balance": op.balance, "current_bet": op.current_bet, "folded": op.folded})

                try:
                    response = player.script.on_betting_round(
                        round=self.round_count,
                        balance=player.balance,
                        current_bet=player.current_bet,
                        hand=player.hand,
                        board_cards=self.board_cards,
                        opponents=opponent_states,
                        check_value=self.current_check_value,
                        raise_count=self.raise_count,
                        pot=self.pot
                    )
                except Exception as e:
                    player.folded = True
                    self.non_folded_player_count -= 1
                    continue 
                
                if response == "check":
                    if player.current_bet != self.current_check_value:
                        player.folded = True
                        self.non_folded_player_count -= 1
                        try: player.script.error_fold(f"Attempted to check while not matching the current check value.")
                        except: pass
                if response == "match":
                    if player.current_bet == self.current_check_value:
                        print(f"Player {player.name} attempted to match while already being at check value. Checking instead.")
                    elif player.balance < (self.current_check_value - player.current_bet):
                        try: player.script.error_fold(f"Attempted to match while not having enough balance.")
                        except: pass
                    else:
                        remainder = self.current_check_value - player.current_bet
                        player.balance -= remainder
                        player.current_bet = self.current_check_value
                if isinstance(response, int):
                    if response < 1:
                        player.folded = True
                        self.non_folded_player_count -= 1
                        try: player.script.error_fold("Cannot raise with a value that is 0 or below.")
                        except: pass 
                    elif player.balance < response:
                        player.folded = True
                        self.non_folded_player_count -= 1
                        try: player.script.error_fold("Not enough balance for attempted raise.")
                        except: pass
                    else:
                        player.balance -= response
                        player.current_bet += response
                        active = True
                        self.raise_count += 1
                        last_raiser = player
                        self.current_check_value = player.current_bet
                if response == "fold":
                    player.folded = True
                    self.non_folded_player_count -= 1
        
            if not active:
                break

        for player in self.players:
            self.pot += player.current_bet
            player.current_bet = 0

        if betting_round == 3 or sum(1 for p in self.players if not p.folded) == 1:
            self.calc_winner()
                
    def calc_winner(self):
        self.game_ended = True
        valid_players = []
        valid_hands = []
        
        if self.non_folded_player_count != 1:
            for player in self.players:
                if not player.folded: 
                    valid_players.append(player)
                    valid_hands.append(player.hand + self.board_cards)
            result = cards_manager.compare_hands(*valid_hands)
            self.winner = [(pos, valid_players[index]) for index, pos in enumerate(result)]
            self.winner.sort(key=lambda x: x[0])
        else:
            for player in self.players:
                if not player.folded:
                    self.winner = player