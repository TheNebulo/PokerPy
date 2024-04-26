import game_manager, os


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
    print(f"Board cards: {game.board_cards}")
    print(f"Pot Size: {game.pot}\n")
    
    if result[1][0] != 1: continue

    for i, info in enumerate(result):
        pos = info[0]
        player = info[1]
        print(f"Position #{pos}: {player.name}")
        print(f"Hand: {player.hand}\n")
        
    input("Press enter to continue: ")