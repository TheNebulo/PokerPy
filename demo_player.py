def on_confirm_buy_in(balance, hand, opponents, buy_in_cost):
    # Simple logic: Buy in if the buy-in cost is less than 50% of balance
    if balance >= buy_in_cost * 2:
        return True
    else:
        return False

def on_betting_round(round, balance, current_bet, hand, board_cards, opponents, check_value, raise_count, pot):
    return "check"

def error_fold(message):
    # Simple print message upon folding due to an error
    print(f"Folding due to error: {message}")