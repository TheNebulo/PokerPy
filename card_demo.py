import cards_manager, os

deck = cards_manager.Deck()

while True:
    if os.name == 'nt': os.system("cls")
    else: os.system("clear")
    hand = deck.select_random_cards(7)
    hand_eval = cards_manager.rank_hand(hand)
    
    print("Card Manager Demo\n")
    
    print(f"Starting hand: {hand}\n")
    
    print("Best case scenario:")
    print(f"Combo: {hand_eval['best']['combo']}")
    print(f"Hand: {hand_eval['best']['hand']}")
    print(f"Highest Card: {hand_eval['best']['highest_card']}")
    print(f"Hand Value: {hand_eval['best']['value']}")
    print(f"Combo Ranking: {cards_manager.get_combo_ranking(hand_eval['best']['combo'])}\n")
    
    print("Worst case scenario:")
    print(f"Combo: {hand_eval['worst']['combo']}")
    print(f"Hand: {hand_eval['worst']['hand']}")
    print(f"Highest Card: {hand_eval['worst']['highest_card']}")
    print(f"Hand Value: {hand_eval['worst']['value']}")
    print(f"Combo Ranking: {cards_manager.get_combo_ranking(hand_eval['worst']['combo'])}\n")

    input("Press enter to continue: ")