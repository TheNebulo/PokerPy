"""Module containing utility functions for managing cards, decks, and ranking hands (including possibilites)."""

import random, math
from copy import deepcopy
from collections import Counter
from itertools import combinations

class Card:
    """Represents a single playing card with suit and value."""
    suits = {1: 'Spades', 2: 'Hearts', 3: 'Diamonds', 4: 'Clubs'}
    values = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace', **{v: str(v) for v in range(2, 11)}}

    def __init__(self, suit: int, value: int) -> None:
        """
        Initializes a card with the specified suit and value.
        
        Args:
            suit (int): The suit of the card, must be between 1 and 4. Spades = 1, Hearts = 2, Diamonds = 3, Clubs = 4
            value (int): The value of the card, must be between 2 and 14 (inclusive). Jack -> Ace = 11 -> 14
        
        Raises:
            ValueError: If suit or value are out of the valid range.
        """
        if suit not in range(1, 5): raise ValueError("Suit is not in range of 1-4.")
        if value not in range(2, 15): raise ValueError("Value is not in range of 2-14.")
        self.suit = suit
        self.value = value

    def __repr__(self) -> str:
        return f'{Card.values[self.value]} of {Card.suits[self.suit]}'
    
    def __eq__(self, other) -> bool:
        return self.suit == other.suit and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.suit, self.value))

class Deck:
    """Represents a deck of playing cards composed of Card objects."""
    
    def __init__(self) -> None:
        """Initializes a new deck of playing cards. The deck will automatically be ordered as per suit and value."""
        self.cards: list[Card] = []
        self.original_ordered_cards: list[Card] = []
        self.is_ordered: bool = True
        self.reset_deck()
        
    def __len__(self) -> int:
        return len(self.cards)
        
    def reset_deck(self) -> None:
        """Resets the deck to the initial state with all 52 cards in order - mimicking a new deck."""
        self.cards = []
        
        for suit in range(1,5):
            for value in range (2,15):
                self.cards.append(Card(suit, value))

        self.original_ordered_cards = deepcopy(self.cards)
        self.is_ordered = True
        
    def order_cards(self) -> None:
        """Orders the cards in the deck back to their original ordered state."""
        self.cards = deepcopy(self.original_ordered_cards)
        self.is_ordered = True

    def shuffle_cards(self) -> None:
        """Shuffles the deck randomly."""
        random.shuffle(self.cards)
        self.is_ordered = False
        
    def remove_cards(self, *args: Card) -> None:
        """
        Removes specified cards from the deck.
        
        Args:
            args (Card): An unpacked list of Card objects to be removed from the deck.
        """
        for card in args: 
            if card in self.cards: self.cards.remove(card)
            
    def append_cards(self, *args: Card) -> None:
        """
        Adds specified cards to the deck if they are not already present.
        
        Args:
            args (Card): An unpacked list of Card objects to be added to the deck.
        """
        for card in args: 
            if card not in self.cards: self.cards.append(card)
        
    def select_random_cards(self, amount: int, remove_cards: bool = None) -> list[Card]:
        """
        Selects a random set of cards from the deck.

        Args:
            amount (int): Number of cards to select.
            remove_cards (bool, optional): If True, the selected cards are removed from the deck. Defaults to True.
        
        Raises:
            ValueError: If the requested amount is invalid (less than 1 or more than the number of cards available).
        
        Returns:
            list[Card]: A list of randomly selected Card objects.
        """
        self.should_remove_cards = True if remove_cards is None else remove_cards
        if amount < 1 or amount > len(self.cards): raise ValueError("Invalid amount of cards to select.")
        cards = random.sample(self.cards, amount)
        if self.should_remove_cards == True: self.remove_cards(*cards)
        return cards
    
    def draw_cards(self, amount: int, remove_cards: bool = None) -> list[Card]:
        """
        Draws a set amount of cards from the top of the deck.

        Args:
            amount (int): Number of cards to select.
            remove_cards (bool, optional): If True, the selected cards are removed from the deck. Defaults to True.
        
        Raises:
            ValueError: If the requested amount is invalid (less than 1 or more than the number of cards available).
        
        Returns:
            list[Card]: A list of randomly selected Card objects.
        """
        self.should_remove_cards = True if remove_cards is None else remove_cards
        if amount < 1 or amount > len(self.cards): raise ValueError("Invalid amount of cards to select.")
        cards = self.cards[:amount]
        if self.should_remove_cards == True: self.remove_cards(*cards)
        return cards
        
def _complete_hands(existing_cards: list[Card]) -> list[list[Card]]:
    """
    Generates all possible complete poker hands based on the given cards.

    Args:
        existing_cards (list[Card]): List of cards that are already part of the hand.

    Returns:
        list[list[Card]]: A list of possible hands.
    """
    if len(existing_cards) < 5:
        all_cards = set(Deck().cards)
        existing_set = set(existing_cards)
        remaining_cards = list(all_cards - existing_set)
        needed_cards = 5 - len(existing_cards)
        return [existing_cards + list(combo) for combo in combinations(remaining_cards, needed_cards)]
    elif len(existing_cards) > 5:
        return [list(combo) for combo in combinations(existing_cards, 5)]
    else:
        return [list(existing_cards)]
    
def _evaluate_combo(cards: list[Card]) -> tuple[str, int, int]:
    """
    Evaluates a five-card hand to determine the poker hand it constitutes and calculates its score.
    
    Args:
        cards (list[Card]): A list of exactly 5 Card objects representing a poker hand.
        
    Raises:
        ValueError: If the provided list of cards is not 5 cards in length.
        
    Returns:
        tuple: A tuple containing the recognized hand type, the high card or relevant card values, and the hand's numeric score.
    """
    if len(cards) != 5:
        raise ValueError("Invalid number of cards: there must be exactly 5 cards.")
    
    def calculate_hand_score(base_score: int) -> int:
        card_values = sorted((card.value for card in cards), reverse=True)
        score = base_score
        for i, value in enumerate(card_values):
            score += value * (10 ** (4 - i))
        return score

    def is_flush() -> bool:
        return len(set(card.suit for card in cards)) == 1

    def is_straight() -> bool:
        values = sorted(card.value for card in cards)
        return all(values[i] + 1 == values[i + 1] for i in range(4)) or set(values) == {2, 3, 4, 5, 14}

    def highest_card() -> int:
        return max(card.value for card in cards)

    value_counts = Counter(card.value for card in cards)

    base_scores = {
        "royal flush": 10**6,
        "straight flush": 8*10**5,
        "four of a kind": 7*10**5,
        "full house": 6*10**5,
        "flush": 5*10**5,
        "straight": 4*10**5,
        "three of a kind": 3*10**5,
        "two pair": 2*10**5,
        "one pair": 10**5,
        "high card": 100
    }

    if is_straight() and is_flush():
        if highest_card() == 14 and 10 in value_counts:
            return ("royal flush", highest_card(), calculate_hand_score(base_scores["royal flush"]))
        
        return ("straight flush", highest_card(), calculate_hand_score(base_scores["straight flush"]))

    if 4 in value_counts.values():
        return "four of a kind", highest_card(), calculate_hand_score(base_scores["four of a kind"])

    if 3 in value_counts.values() and 2 in value_counts.values():
        return "full house", highest_card(), calculate_hand_score(base_scores["full house"])

    if is_flush():
        return "flush", highest_card(), calculate_hand_score(base_scores["flush"])

    if is_straight():
        return "straight", highest_card(), calculate_hand_score(base_scores["straight"])

    if 3 in value_counts.values():
        return "three of a kind", highest_card(), calculate_hand_score(base_scores["three of a kind"])

    if list(value_counts.values()).count(2) > 1:
        return "two pair", highest_card(), calculate_hand_score(base_scores["two pair"])

    if 2 in value_counts.values():
        return "one pair", highest_card(), calculate_hand_score(base_scores["one pair"])

    return "high card", highest_card(), calculate_hand_score(base_scores["high card"])

def rank_hand(hand: list[Card]) -> tuple[dict[str, any], dict[str, any]]:
    """
    Ranks a poker hand in its best and worst form by considering all possible hand completions, providing information on the hand combination name, the hands themselves, the highest card, and the hand's value respectively.

    Args:
        hand (list[Card]): The list of Card objects representing the current hand.
        
    Raises:
        ValueError: If the list of cards is empty or duplicate cards appear.

    Returns:
        tuple: Two dictionaries containing the best and worst case scenarios (in that respective order), which contain keys 'combo_name', 'hands', 'highest_card' and 'value'.
    """
    if len(hand) < 1: raise ValueError("The length of the hand must be above 1.")
    if len(set(hand)) != len(hand): raise ValueError("The hand must contain only unique cards.")
    
    best_case_scenario = {"combo_name" : None, "hands" : [], "highest_card": None, "value" : -1}
    worst_case_scenario = {"combo_name" : None, "hands" : [], "highest_card": None, "value" : math.inf}
    possible_hands = _complete_hands(hand)
    
    for possible_hand in possible_hands:
        result = _evaluate_combo(possible_hand)
            
        if result[2] == best_case_scenario["value"]:
            best_case_scenario["hands"].append(possible_hand)
        elif result[2] > best_case_scenario["value"]:
            best_case_scenario = {"combo_name" : result[0], "hands" : [possible_hand], "highest_card": result[1], "value" : result[2]}
        
        if result[2] == worst_case_scenario["value"]:
            worst_case_scenario["hands"].append(possible_hand)
        if result[2] < worst_case_scenario["value"]:
            worst_case_scenario = {"combo_name" : result[0], "hands" : [possible_hand], "highest_card": result[1], "value" : result[2]}
    
    return best_case_scenario, worst_case_scenario

def get_combo_ranking(hand_name: str) -> int:
    """
    Returns the ranking of a hand combination by it's name.
    
    Args:
        hand_name (str): The name of the hand combination. Case insensitive.
        
    Raises:
        ValueError: If the requested combination name does not exist.
        
    Returns:
        int: An integer representing the position of the hand combination in the ranking.
    """
    rankings = ["royal flush", "straight flush", "four of a kind", "full house", "flush", "straight", "three of a kind", "two pair", "one pair", "high card"]
    try:
        return rankings.index(hand_name.lower()) + 1
    except:
        raise ValueError("Hand combination name does not exist.")
    
def compare_hands(*hands: list[Card]) -> list[int]:
    """
    Compares any amount of hands and returns a list replacing a hand with it's position in the hand ranking.
    
    Args: 
        hands (list[Card]): An unpacked list of hands (lists containing Card objects) to be compared.
        
    Returns:
        list[int]: A list containing the positions of hands in the ranking, placed in the same order as the argument list. 
    """
    hand_values = [rank_hand(hand)[0]['value'] for hand in hands]
    indexed_values = list(enumerate(hand_values))
    indexed_values.sort(key=lambda x: x[1], reverse=True)
    position = last_val = 0
    for original_position, value in indexed_values:
        if value != last_val: position += 1
        hand_values[original_position] = position
    return hand_values