import game_manager, os, cards_manager

loops = 0
while True:
    loops += 1
    os.system("cls")
    
    players = [
        game_manager.Player("Player 1", 1000, "demo_player"),
        game_manager.Player("Player 2", 1000, "demo_player"),
        game_manager.Player("Player 3", 1000, "demo_player"),
        game_manager.Player("Player 4", 1000, "demo_player")
    ]

    game = game_manager.Game(players, 1)

    result = game.run_game()
    
    print(f"Loops: {loops}")
    print(f"Round: {game.round_count}")
    print(f"Board cards: {game.board_cards}")
    print(f"Pot Size: {game.pot}\n")

    if isinstance(result, game_manager.Player):
            continue
            print(f"Position #1: {result.name}")
            print(f"Hand: {result.hand}\n")
    else:
        for i, info in enumerate(result):
            pos = info[0]
            player = info[1]
            print(f"Position #{pos}: {player.name}")
            print(f"Hand: {player.hand}")
            print(f"Combo: {cards_manager.rank_hand(player.hand + game.board_cards)[0]['combo_name']}\n")
            
    print("Folded/Non-bought-in Players:\n")
            
    for player in game.players:
        if player.folded and not player.bought_in:
            print(f"Name: {player.name} (Not Bought In)")
            print(f"Hand: {player.hand}")
            print(f"Combo: {cards_manager.rank_hand(player.hand + game.board_cards)[0]['combo_name']}\n")
        elif player.folded:
            print(f"Name: {player.name} (Folded)")
            print(f"Hand: {player.hand}")
            print(f"Combo: {cards_manager.rank_hand(player.hand + game.board_cards)[0]['combo_name']}\n")
        
    input("Press enter to continue: ")