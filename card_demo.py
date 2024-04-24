import cards_manager, os

deck = cards_manager.Deck()
deck.shuffle_cards()

while True:
    if os.name == 'nt': os.system("cls")
    else: os.system("clear")
    hand = deck.select_random_cards(2)
    best_case_scenario, worst_case_scenario = cards_manager.rank_hand(hand)
    
    print("Card Manager Demo\n")
    
    print(f"Starting hand: {hand}\n")
    
    print("Best case scenario:")
    print(f"Combo: {best_case_scenario['combo_name']}")
    print(f"Possible Hand Combinations: {best_case_scenario['hands']}")
    print(f"Highest Card: {best_case_scenario['highest_card']}")
    print(f"Hand Value: {best_case_scenario['value']}")
    print(f"Combo Ranking: {cards_manager.get_combo_ranking(best_case_scenario['combo_name'])}\n")
    
    print("Worst case scenario:")
    print(f"Combo: {worst_case_scenario['combo_name']}")
    print(f"Possible Hand Combinations: {worst_case_scenario['hands']}")
    print(f"Highest Card: {worst_case_scenario['highest_card']}")
    print(f"Hand Value: {worst_case_scenario['value']}")
    print(f"Combo Ranking: {cards_manager.get_combo_ranking(worst_case_scenario['combo_name'])}\n")

    input("Press enter to continue: ")