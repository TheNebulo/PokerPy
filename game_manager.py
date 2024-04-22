import cards_manager

class Player:
    def __init__(self, name: str, starting_balance: int, script_path: str):
        self.name = name
        self.starting_balance = starting_balance
        self.script = __import__(script_path)
        
class BettingRound:
    def __init__(self, round_count: int):
        self.round_count = round_count

class Game:
    def __init__(self, players: Player, buy_in_cost: int):
        self.players = players
        self.buy_in_cost = buy_in_cost
        self.deck = cards_manager.Deck()
        self.deck.shuffle_cards()
        self.betting_rounds = [BettingRound(i) for i in range(1, 5)]