"""
Valid Game States for Testing
Each state is set up so that:
- turn = 1 (Player 1's next move)
- Has an obvious best move
- Includes early, mid, and end game scenarios
"""

# ============================================================================
# memory GAME STATES
# ============================================================================

memory_early_game = {
    'name': "memory",
    
    'deck': [
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
        "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"
    ],
    
    'shuffled_deck': [],
    
    'hands': [
        ["8H", "9C"],     # Player 0 has 2 cards (1 match)
        ["7D", "JS"]      # Player 1 has 2 cards (1 match)
    ],
    
    'first_selected_card': ('y','x','card'),
    'second_selected_card': ('y','x','card'),
    'selected_first_card': False,
    
    # 9×6 board - Player 1 can see two matching cards (7H and 7C)
    'card_array': [
        ['',    '',    '9H',  '9C',  '',    'KS'],
        ['1D',  'QS',  '6H',  '',    'KD',  'JC'],
        ['3S',  '7S',  '',    'AD',  '8C',  '9S'],
        ['5S',  '1H',  'AS',  'RJ',  '8S',  ''],
        ['BJ',  '4H',  '',    'QH',  '3D',  'AC'],
        ['JD',  '',    '7H',  '4D',  'KC',  ''],
        ['QC',  '',    'AH',  '5H',  '5D',  ''],
        ['6S',  'JH',  '3C',  '7D',  '',    '6D'],
        ['6C',  '4C',  '2C',  '',    '9D',  '7C']  # 7C at (8,5)
    ],
    
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (-1, ""),
    'winner': None,
    
    'history': [
        # Player 0 revealed two non-matching cards
        ('pick', 0, (0,2,'9H')),
        ('pick', 0, (0,3,'9C')),
        ('Missed', 0, (0,2,'9H'), (0,3,'9C'))
    ]
}

memory_mid_game = {
    'name': "memory",
    
    'deck': [
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
        "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"
    ],
    
    'shuffled_deck': [],
    
    'hands': [
        ["8H", "9C", "BJ", "RJ"],  # Player 0 has 4 cards (2 joker pair!)
        ["7D", "JS", "QC"]         # Player 1 has 3 cards
    ],
    
    'first_selected_card': ('y','x','card'),
    'second_selected_card': ('y','x','card'),
    'selected_first_card': False,
    
    # 9×6 board - Player 1 can match two black jokers (red suits)
    'card_array': [
        ['QH',  '',    'JH',  '9H',  '',    'KS'],
        ['KD',  '1D',  '6H',  '',    '2D',  'JC'],
        ['3S',  '7S',  '',    'AD',  '8C',  '9S'],
        ['5S',  '1H',  'AS',  'BJ',  '8S',  ''],
        ['RJ',  '4H',  '',    'QC',  '3D',  'AC'],
        ['JD',  '',    '7H',  '4D',  'KC',  ''],
        ['AC',  '',    'AH',  '5H',  '5D',  ''],
        ['6S',  '1S',  '3C',  '7D',  '',    '6D'],
        ['6C',  '4C',  '2C',  '',    '9D',  '3H']
    ],
    
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (-1, ""),
    'winner': None,
    
    'history': [
        ('pick', 0, (0,0,'QH')),
        ('pick', 0, (0,2,'JH')),
        ('Missed', 0, (0,0,'QH'), (0,2,'JH')),
        ('pick', 1, (2,2,'QD')),
        ('pick', 1, (5,2,'7H')),
        ('Missed', 1, (2,2,'QD'), (5,2,'7H'))
    ]
}

memory_end_game = {
    'name': "memory",
    
    'deck': [
        "AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
        "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
        "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
        "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"
    ],
    
    'shuffled_deck': [],
    
    'hands': [
        ["8H", "9C", "BJ", "RJ", "KS", "QH", "JH", "9H"],  # Player 0 has 8
        ["7D", "JS", "QC", "AD", "8C", "9S", "7S", "3S"]   # Player 1 has 8
    ],
    
    'first_selected_card': ('y','x','card'),
    'second_selected_card': ('y','x','card'),
    'selected_first_card': False,
    
    # 9×6 board - Only 4 cards left, Player 1 can match 2D and 3D (same rank)
    'card_array': [
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '2D',   '4D',  '2C',  ''],
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '',    '',    '',    ''],
        ['',    '',    '',    '',    '',    '']
    ],
    
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (-1, ""),
    'winner': None,
    
    'history': [
        # Many previous moves establishing card positions
        ('pick', 0, (0,0,'QH')),
        ('pick', 0, (0,2,'JH')),
        ('Missed', 0, (0,0,'QH'), (0,2,'JH')),
        ('pick', 1, (5,2,'2D')),
        ('pick', 1, (5,3,'4D')),
        ('Missed', 1, (5,2,'2D'), (5,3,'4D'))
    ]
}


# ============================================================================
# rummy GAME STATES
# ============================================================================

rummy_early_game = {
    'name': 'rummy',
    'deck': ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
             "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
             "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
             "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
    
    'shuffled_deck': [
        '7H','3C','KD','9S','5H','2C','4D','JC','8D','QS','6S','AH','9C',
        '8H','KH','4H','3H','JH','5C','6C','7C','4C','1H','QH'
    ],
    
    'value_map': {'A':1,'K':13,'Q':12,'J':11,'1':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2},
    
    'hands': [
        # PLAYER 0 (about to draw: has 7 cards)
        ['4H','5H','7H','2D','2S','8C','KD'],
        
        # PLAYER 1 (in discard phase: has 8 cards - obvious best move: draw from deck!)
        ['3H','3S','3D','6C','9H','QH','1S','KC']
    ],
    
    'discard_pile': ['5C','4C','7D'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0,'Easy'),
    'winner': None,
    
    'history': [
        (1,'KC','discard'),
        (0,'7D','draw'),
        (0,'7D','discard'),
    ]
}

rummy_mid_game = {
    'name': 'rummy',
    'deck': ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
             "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
             "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
             "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
    
    'shuffled_deck': ['4C','AD','8D','AS','7C','KC','2S','7D','QH','3C','5S','AC','6H'],
    
    'value_map': {'A':1,'K':13,'Q':12,'J':11,'1':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2},
    
    'hands': [
        # PLAYER 0 (about to draw: has 7 cards)
        ['4H','5H','4D','2D','2S','8C','4C'],
        
        # PLAYER 1 (in discard phase: has 8 cards - obvious best move: discard QH!)
        ['3H','3S','6D','6C','9H','QS','1S','KS']
    ],
    
    'discard_pile': ['5C','7D','2C'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0,'Easy'),
    'winner': None,
    
    'history': [
        (1,'KC','discard'),
        (0,'7D','draw'),
        (0,'7D','discard'),
        (1,'2C','draw'),
        (0,'4C','draw'),
    ]
}

rummy_end_game = {
    'name': 'rummy',
    'deck': ["AD","2D","3D","4D","5D","6D","7D","8D","9D","1D","JD","QD","KD",
             "AS","2S","3S","4S","5S","6S","7S","8S","9S","1S","JS","QS","KS",
             "AC","2C","3C","4C","5C","6C","7C","8C","9C","1C","JC","QC","KC",
             "AH","2H","3H","4H","5H","6H","7H","8H","9H","1H","JH","QH","KH"],
    
    'shuffled_deck': [],
    
    'value_map': {'A':1,'K':13,'Q':12,'J':11,'1':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2},
    
    'hands': [
        # PLAYER 0 (about to win with perfect run: A-2-3 of hearts, 4-5-6 of hearts)
        ['AH','2H','3H','4H','5H','6H'],
        
        # PLAYER 1 (in discard phase: has 8 cards - obvious best move: discard anything!)
        ['3D','3S','6D','6C','9H','QH','1S','KC']
    ],
    
    'discard_pile': ['5C','7D','2C'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0,'Easy'),
    'winner': None,
    
    'history': [
        (1,'KC','discard'),
        (0,'7D','draw'),
        (0,'AH','discard'),
        (1,'2C','draw'),
        (0,'2H','draw'),
        (1,'QH','discard'),
        (0,'3H','draw'),
        (1,'1S','discard'),
    ]
}


# ============================================================================
# threes GAME STATES
# ============================================================================

threes_early_game = {
    'name': 'threes',
    'deck': ['AD', '2D', '7S', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD',
             'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS',
             'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC',
             'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH'],
    
    'shuffled_deck': ['4C', 'AD', '8D', '8H', '7C', 'KC', '2S', '7D', 'QH', '3C', '5S', 
                      'AC', '6H', '8C', '5H', '4D', '1C', '9D', '1S', 'QS', 'KD', 'QD', '6D', '5D'],
    
    'rank_order': {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15},
    
    'hands': [
        ['7H', 'JS', 'KH'],      # Player 0
        ['1D', '3D', 'AS']       # Player 1 - obvious move: play 1D (highest card)
    ],
    
    'discard_pile': [],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0, 'Easy'),
    'winner': None,
    
    'bottom_hands': [
        ['2C', '3H', '8S'],      # Player 0
        ['1H', '2D', 'AH']       # Player 1
    ],
    
    'top_hands': [
        ['5C', '6C', '6S'],      # Player 0
        ['JH', '4S', '3S']       # Player 1
    ],
    
    'another': False,
    'played_cards': ['2H'],      # Initial 2 (anything beats 2)
    
    'history': [
        (0, '2H', 'play')        # Player 0 started with 2
    ]
}

threes_mid_game = {
    'name': 'threes',
    'deck': ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD',
             'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS',
             'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC',
             'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH'],
    
    'shuffled_deck': ['QD', '6D', '5D', 'JC', '9C', '3D', '4H', '9H', 'JD'],
    
    'rank_order': {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15},
    
    'hands': [
        ['7H', '8H', '9H'],      # Player 0
        ['6C', '7C', '8C']       # Player 1 - obvious move: play 8C (matches top card 8S)
    ],
    
    'discard_pile': ['2H', '3C', '4D'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0, 'Easy'),
    'winner': None,
    
    'bottom_hands': [
        ['2C', '3H', '4S'],      # Player 0
        ['1H', '2D', 'AH']       # Player 1
    ],
    
    'top_hands': [
        ['5C', '6S', '9S'],      # Player 0
        ['JH', '4S', '3S']       # Player 1
    ],
    
    'another': False,
    'played_cards': ['5S', '6S', '7S'],  # Run of 5-6-7-8 (top card is 8S)
    
    'history': [
        (0, '5S', 'play'),
        (1, '6S', 'play'),
        (0, '7S', 'play'),
    ]
}

threes_end_game = {
    'name': 'threes',
    'deck': ['AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '1D', 'JD', 'QD', 'KD',
             'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '1S', 'JS', 'QS', 'KS',
             'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '1C', 'JC', 'QC', 'KC',
             'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '1H', 'JH', 'QH', 'KH'],
    
    'shuffled_deck': [],
    
    'rank_order': {'A': 14,'K': 13,'Q': 12,'J': 11,'1': 16,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 15},
    
    'hands': [
        ['7H', '8H'],            # Player 0 - low hand count
        ['6C']                   # Player 1 - obvious move: play 6C (matches top card, and only has 1 card left!)
    ],
    
    'discard_pile': ['2H', '3C', '4D', '5S', '7D', '8D'],
    'selected_card': '',
    'turn': 1,
    'time_elapsed': 0,
    'difficulty': (0, 'Easy'),
    'winner': None,
    
    'bottom_hands': [
        ['2C', '3H'],            # Player 0
        ['1H']                   # Player 1
    ],
    
    'top_hands': [
        ['5C'],                  # Player 0
        []                       # Player 1 (empty)
    ],
    
    'another': False,
    'played_cards': ['3D', '4D', '5D', '6D'],  # Run of 3-4-5-6 (top card is 6D)
    
    'history': [
        (0, '3D', 'play'),
        (1, '4D', 'play'),
        (0, '5D', 'play'),
        (1, '6D', 'play'),
        (0, ['3D', '4D', '5D', '6D'], 'pickup'),
        (1, '1H', 'play'),
        (0, '7H', 'play'),
    ]
}


if __name__ == "__main__":
    print("Game states created successfully!")
    print("\nMemory Game States:")
    print("- memory_early_game: Player 1 can match 7H and 7C")
    print("- memory_mid_game: Player 1 can match BJ and RJ (jokers)")
    print("- memory_end_game: Only 4 cards left, Player 1 can match 2D and 2C")
    
    print("\nRummy Game States:")
    print("- rummy_early_game: Player 1 has 8 cards (3H, 3S, 3D) - obvious discard")
    print("- rummy_mid_game: Player 1 has 8 cards with set ready")
    print("- rummy_end_game: Player 1 must discard before Player 0 wins with run")
    
    print("\nThrees Game States:")
    print("- threes_early_game: Player 1 should play 1D (highest, must beat 2H)")
    print("- threes_mid_game: Player 1 should play 8C (matches 8S in sequence)")
    print("- threes_end_game: Player 1 has 1 card left, should play 6C (matches 6D)")

