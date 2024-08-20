import cards_manager

def on_confirm_buy_in(balance, hand, opponents, buy_in_cost):
    if balance >= buy_in_cost * 2:
        return True
    else:
        return False

def on_betting_round(round, balance, current_bet, hand, board_cards, opponents, check_value, raise_count, pot):
    best_case, worst_case =  cards_manager.rank_hand(hand + board_cards)

    worst_rank = cards_manager.get_combo_ranking(worst_case["combo_name"])
    
    if worst_rank < 10:
        if check_value != current_bet:
            return "match"
        else:
            return "check"
    else:
        return "fold"

def error_fold(message):
    # Simple print message upon folding due to an error
    print(f"Folding due to error: {message}")