from ui import Shop_Dialog, Shop_Card

class Theme:
    def __init__(theme,name,cost,front,back,dictionary): #Initialising attributes for theme objects
        theme.name = name
        theme.cost = cost
        theme.front_img = front
        theme.back_img = back
        theme.asset_dict = dictionary

class Shop:
    def __init__(shop): #Initialising attributes for shop class
        shop.inventory = []
        shop.equipped = 'Classic' #Sets default theme
        shop.unlocked_inventory = ['Classic'] #Sets default unlocked inventory
        shop.coin_count = 0

    def set_all_themes(shop):
        themeslst = ['Classic','Blue_Classic','Dark-Red','Light-Red','Faded']
        themes = shop.inventory
        #Initialises all theme objects including mapping each image to the themes asset dictonary and adds it to the shop inventory
        themes.append(Theme(themeslst[0], 0, 'assets/img/theme1/king_of_clubs2.png', 'assets/img/theme1/card_back_red.png',{
    # Hearts
    "AH": "MobilePlayingCardApp/assets/img/theme1/ace_of_hearts.png",
    "2H": "MobilePlayingCardApp/assets/img/theme1/2_of_hearts.png",
    "3H": "MobilePlayingCardApp/assets/img/theme1/3_of_hearts.png",
    "4H": "MobilePlayingCardApp/assets/img/theme1/4_of_hearts.png",
    "5H": "MobilePlayingCardApp/assets/img/theme1/5_of_hearts.png",
    "6H": "MobilePlayingCardApp/assets/img/theme1/6_of_hearts.png",
    "7H": "MobilePlayingCardApp/assets/img/theme1/7_of_hearts.png",
    "8H": "MobilePlayingCardApp/assets/img/theme1/8_of_hearts.png",
    "9H": "MobilePlayingCardApp/assets/img/theme1/9_of_hearts.png",
    "1H": "MobilePlayingCardApp/assets/img/theme1/10_of_hearts.png",
    "JH": "MobilePlayingCardApp/assets/img/theme1/jack_of_hearts.png",
    "QH": "MobilePlayingCardApp/assets/img/theme1/queen_of_hearts.png",
    "KH": "MobilePlayingCardApp/assets/img/theme1/king_of_hearts.png",

    # Diamonds
    "AD": "MobilePlayingCardApp/assets/img/theme1/ace_of_diamonds.png",
    "2D": "MobilePlayingCardApp/assets/img/theme1/2_of_diamonds.png",
    "3D": "MobilePlayingCardApp/assets/img/theme1/3_of_diamonds.png",
    "4D": "MobilePlayingCardApp/assets/img/theme1/4_of_diamonds.png",
    "5D": "MobilePlayingCardApp/assets/img/theme1/5_of_diamonds.png",
    "6D": "MobilePlayingCardApp/assets/img/theme1/6_of_diamonds.png",
    "7D": "MobilePlayingCardApp/assets/img/theme1/7_of_diamonds.png",
    "8D": "MobilePlayingCardApp/assets/img/theme1/8_of_diamonds.png",
    "9D": "MobilePlayingCardApp/assets/img/theme1/9_of_diamonds.png",
    "1D": "MobilePlayingCardApp/assets/img/theme1/10_of_diamonds.png",
    "JD": "MobilePlayingCardApp/assets/img/theme1/jack_of_diamonds.png",
    "QD": "MobilePlayingCardApp/assets/img/theme1/queen_of_diamonds.png",
    "KD": "MobilePlayingCardApp/assets/img/theme1/king_of_diamonds.png",

    # Clubs
    "AC": "MobilePlayingCardApp/assets/img/theme1/ace_of_clubs.png",
    "2C": "MobilePlayingCardApp/assets/img/theme1/2_of_clubs.png",
    "3C": "MobilePlayingCardApp/assets/img/theme1/3_of_clubs.png",
    "4C": "MobilePlayingCardApp/assets/img/theme1/4_of_clubs.png",
    "5C": "MobilePlayingCardApp/assets/img/theme1/5_of_clubs.png",
    "6C": "MobilePlayingCardApp/assets/img/theme1/6_of_clubs.png",
    "7C": "MobilePlayingCardApp/assets/img/theme1/7_of_clubs.png",
    "8C": "MobilePlayingCardApp/assets/img/theme1/8_of_clubs.png",
    "9C": "MobilePlayingCardApp/assets/img/theme1/9_of_clubs.png",
    "1C": "MobilePlayingCardApp/assets/img/theme1/10_of_clubs.png",
    "JC": "MobilePlayingCardApp/assets/img/theme1/jack_of_clubs.png",
    "QC": "MobilePlayingCardApp/assets/img/theme1/queen_of_clubs.png",
    "KC": "MobilePlayingCardApp/assets/img/theme1/king_of_clubs.png",

    # Spades
    "AS": "MobilePlayingCardApp/assets/img/theme1/ace_of_spades.png",
    "2S": "MobilePlayingCardApp/assets/img/theme1/2_of_spades.png",
    "3S": "MobilePlayingCardApp/assets/img/theme1/3_of_spades.png",
    "4S": "MobilePlayingCardApp/assets/img/theme1/4_of_spades.png",
    "5S": "MobilePlayingCardApp/assets/img/theme1/5_of_spades.png",
    "6S": "MobilePlayingCardApp/assets/img/theme1/6_of_spades.png",
    "7S": "MobilePlayingCardApp/assets/img/theme1/7_of_spades.png",
    "8S": "MobilePlayingCardApp/assets/img/theme1/8_of_spades.png",
    "9S": "MobilePlayingCardApp/assets/img/theme1/9_of_spades.png",
    "1S": "MobilePlayingCardApp/assets/img/theme1/10_of_spades.png",
    "JS": "MobilePlayingCardApp/assets/img/theme1/jack_of_spades.png",
    "QS": "MobilePlayingCardApp/assets/img/theme1/queen_of_spades.png",
    "KS": "MobilePlayingCardApp/assets/img/theme1/king_of_spades.png",

    #Jokers
    "RJ": "MobilePlayingCardApp/assets/img/theme1/red_joker.png",
    "BJ": "MobilePlayingCardApp/assets/img/theme1/black_joker.png",
}))
        themes.append(Theme(themeslst[1], 50,'assets/img/theme2/Spades 13.png','assets/img/theme2/Back Blue 1.png',{
    # Hearts
    "AH": "MobilePlayingCardApp/assets/img/theme2/Hearts 1.png",
    "2H": "MobilePlayingCardApp/assets/img/theme2/Hearts 2.png",
    "3H": "MobilePlayingCardApp/assets/img/theme2/Hearts 3.png",
    "4H": "MobilePlayingCardApp/assets/img/theme2/Hearts 4.png",
    "5H": "MobilePlayingCardApp/assets/img/theme2/Hearts 5.png",
    "6H": "MobilePlayingCardApp/assets/img/theme2/Hearts 6.png",
    "7H": "MobilePlayingCardApp/assets/img/theme2/Hearts 7.png",
    "8H": "MobilePlayingCardApp/assets/img/theme2/Hearts 8.png",
    "9H": "MobilePlayingCardApp/assets/img/theme2/Hearts 9.png",
    "1H": "MobilePlayingCardApp/assets/img/theme2/Hearts 10.png",
    "JH": "MobilePlayingCardApp/assets/img/theme2/Hearts 11.png",
    "QH": "MobilePlayingCardApp/assets/img/theme2/Hearts 12.png",
    "KH": "MobilePlayingCardApp/assets/img/theme2/Hearts 13.png",

    # Diamond
    "AD": "MobilePlayingCardApp/assets/img/theme2/Diamond 1.png",
    "2D": "MobilePlayingCardApp/assets/img/theme2/Diamond 2.png",
    "3D": "MobilePlayingCardApp/assets/img/theme2/Diamond 3.png",
    "4D": "MobilePlayingCardApp/assets/img/theme2/Diamond 4.png",
    "5D": "MobilePlayingCardApp/assets/img/theme2/Diamond 5.png",
    "6D": "MobilePlayingCardApp/assets/img/theme2/Diamond 6.png",
    "7D": "MobilePlayingCardApp/assets/img/theme2/Diamond 7.png",
    "8D": "MobilePlayingCardApp/assets/img/theme2/Diamond 8.png",
    "9D": "MobilePlayingCardApp/assets/img/theme2/Diamond 9.png",
    "1D": "MobilePlayingCardApp/assets/img/theme2/Diamond 10.png",
    "JD": "MobilePlayingCardApp/assets/img/theme2/Diamond 11.png",
    "QD": "MobilePlayingCardApp/assets/img/theme2/Diamond 12.png",
    "KD": "MobilePlayingCardApp/assets/img/theme2/Diamond 13.png",

    # Club
    "AC": "MobilePlayingCardApp/assets/img/theme2/Clubs 1.png",
    "2C": "MobilePlayingCardApp/assets/img/theme2/Clubs 2.png",
    "3C": "MobilePlayingCardApp/assets/img/theme2/Clubs 3.png",
    "4C": "MobilePlayingCardApp/assets/img/theme2/Clubs 4.png",
    "5C": "MobilePlayingCardApp/assets/img/theme2/Clubs 5.png",
    "6C": "MobilePlayingCardApp/assets/img/theme2/Clubs 6.png",
    "7C": "MobilePlayingCardApp/assets/img/theme2/Clubs 7.png",
    "8C": "MobilePlayingCardApp/assets/img/theme2/Clubs 8.png",
    "9C": "MobilePlayingCardApp/assets/img/theme2/Clubs 9.png",
    "1C": "MobilePlayingCardApp/assets/img/theme2/Clubs 10.png",
    "JC": "MobilePlayingCardApp/assets/img/theme2/Clubs 11.png",
    "QC": "MobilePlayingCardApp/assets/img/theme2/Clubs 12.png",
    "KC": "MobilePlayingCardApp/assets/img/theme2/Clubs 13.png",

    # Spades
    "AS": "MobilePlayingCardApp/assets/img/theme2/Spades 1.png",
    "2S": "MobilePlayingCardApp/assets/img/theme2/Spades 2.png",
    "3S": "MobilePlayingCardApp/assets/img/theme2/Spades 3.png",
    "4S": "MobilePlayingCardApp/assets/img/theme2/Spades 4.png",
    "5S": "MobilePlayingCardApp/assets/img/theme2/Spades 5.png",
    "6S": "MobilePlayingCardApp/assets/img/theme2/Spades 6.png",
    "7S": "MobilePlayingCardApp/assets/img/theme2/Spades 7.png",
    "8S": "MobilePlayingCardApp/assets/img/theme2/Spades 8.png",
    "9S": "MobilePlayingCardApp/assets/img/theme2/Spades 9.png",
    "1S": "MobilePlayingCardApp/assets/img/theme2/Spades 10.png",
    "JS": "MobilePlayingCardApp/assets/img/theme2/Spades 11.png",
    "QS": "MobilePlayingCardApp/assets/img/theme2/Spades 12.png",
    "KS": "MobilePlayingCardApp/assets/img/theme2/Spades 13.png",

    #Jokers
    "RJ": "MobilePlayingCardApp/assets/img/theme2/Joker Red.png",
    "BJ": "MobilePlayingCardApp/assets/img/theme2/Joker Black.png",
}))
        themes.append(Theme(themeslst[2],100,'assets/img/theme3/ClubsQueen.png','assets/img/theme3/BackGrey1.png',{
    # Hearts
    "AH": "MobilePlayingCardApp/assets/img/theme3/HeartsA.png",
    "2H": "MobilePlayingCardApp/assets/img/theme3/Hearts2.png",
    "3H": "MobilePlayingCardApp/assets/img/theme3/Hearts3.png",
    "4H": "MobilePlayingCardApp/assets/img/theme3/Hearts4.png",
    "5H": "MobilePlayingCardApp/assets/img/theme3/Hearts5.png",
    "6H": "MobilePlayingCardApp/assets/img/theme3/Hearts6.png",
    "7H": "MobilePlayingCardApp/assets/img/theme3/Hearts7.png",
    "8H": "MobilePlayingCardApp/assets/img/theme3/Hearts8.png",
    "9H": "MobilePlayingCardApp/assets/img/theme3/Hearts9.png",
    "1H": "MobilePlayingCardApp/assets/img/theme3/Hearts10.png",
    "JH": "MobilePlayingCardApp/assets/img/theme3/HeartsJack.png",
    "QH": "MobilePlayingCardApp/assets/img/theme3/HeartsQueen.png",
    "KH": "MobilePlayingCardApp/assets/img/theme3/HeartsKing.png",

    # Diamonds
    "AD": "MobilePlayingCardApp/assets/img/theme3/DiamondsA.png",
    "2D": "MobilePlayingCardApp/assets/img/theme3/Diamonds2.png",
    "3D": "MobilePlayingCardApp/assets/img/theme3/Diamonds3.png",
    "4D": "MobilePlayingCardApp/assets/img/theme3/Diamonds4.png",
    "5D": "MobilePlayingCardApp/assets/img/theme3/Diamonds5.png",
    "6D": "MobilePlayingCardApp/assets/img/theme3/Diamonds6.png",
    "7D": "MobilePlayingCardApp/assets/img/theme3/Diamonds7.png",
    "8D": "MobilePlayingCardApp/assets/img/theme3/Diamonds8.png",
    "9D": "MobilePlayingCardApp/assets/img/theme3/Diamonds9.png",
    "1D": "MobilePlayingCardApp/assets/img/theme3/Diamonds10.png",
    "JD": "MobilePlayingCardApp/assets/img/theme3/DiamondsJack.png",
    "QD": "MobilePlayingCardApp/assets/img/theme3/DiamondsQueen.png",
    "KD": "MobilePlayingCardApp/assets/img/theme3/DiamondsKing.png",

    # Clubs
    "AC": "MobilePlayingCardApp/assets/img/theme3/ClubsA.png",
    "2C": "MobilePlayingCardApp/assets/img/theme3/Clubs2.png",
    "3C": "MobilePlayingCardApp/assets/img/theme3/Clubs3.png",
    "4C": "MobilePlayingCardApp/assets/img/theme3/Clubs4.png",
    "5C": "MobilePlayingCardApp/assets/img/theme3/Clubs5.png",
    "6C": "MobilePlayingCardApp/assets/img/theme3/Clubs6.png",
    "7C": "MobilePlayingCardApp/assets/img/theme3/Clubs7.png",
    "8C": "MobilePlayingCardApp/assets/img/theme3/Clubs8.png",
    "9C": "MobilePlayingCardApp/assets/img/theme3/Clubs9.png",
    "1C": "MobilePlayingCardApp/assets/img/theme3/Clubs10.png",
    "JC": "MobilePlayingCardApp/assets/img/theme3/ClubsJack.png",
    "QC": "MobilePlayingCardApp/assets/img/theme3/ClubsQueen.png",
    "KC": "MobilePlayingCardApp/assets/img/theme3/ClubsKing.png",

    # Spades
    "AS": "MobilePlayingCardApp/assets/img/theme3/SpadesA.png",
    "2S": "MobilePlayingCardApp/assets/img/theme3/Spades2.png",
    "3S": "MobilePlayingCardApp/assets/img/theme3/Spades3.png",
    "4S": "MobilePlayingCardApp/assets/img/theme3/Spades4.png",
    "5S": "MobilePlayingCardApp/assets/img/theme3/Spades5.png",
    "6S": "MobilePlayingCardApp/assets/img/theme3/Spades6.png",
    "7S": "MobilePlayingCardApp/assets/img/theme3/Spades7.png",
    "8S": "MobilePlayingCardApp/assets/img/theme3/Spades8.png",
    "9S": "MobilePlayingCardApp/assets/img/theme3/Spades9.png",
    "1S": "MobilePlayingCardApp/assets/img/theme3/Spades10.png",
    "JS": "MobilePlayingCardApp/assets/img/theme3/SpadesJack.png",
    "QS": "MobilePlayingCardApp/assets/img/theme3/SpadesQueen.png",
    "KS": "MobilePlayingCardApp/assets/img/theme3/SpadesKing.png",

    # Jokers
    "RJ": "MobilePlayingCardApp/assets/img/theme2/Joker Red.png",
    "BJ": "MobilePlayingCardApp/assets/img/theme2/Joker Black.png",
}))
        themes.append(Theme(themeslst[3],100,'assets/img/theme4/ClubsJack.png','assets/img/theme4/Back Red 2.png',{
    # Hearts
    "AH": "MobilePlayingCardApp/assets/img/theme4/HeartsA.png",
    "2H": "MobilePlayingCardApp/assets/img/theme4/Hearts2.png",
    "3H": "MobilePlayingCardApp/assets/img/theme4/Hearts3.png",
    "4H": "MobilePlayingCardApp/assets/img/theme4/Hearts4.png",
    "5H": "MobilePlayingCardApp/assets/img/theme4/Hearts5.png",
    "6H": "MobilePlayingCardApp/assets/img/theme4/Hearts6.png",
    "7H": "MobilePlayingCardApp/assets/img/theme4/Hearts7.png",
    "8H": "MobilePlayingCardApp/assets/img/theme4/Hearts8.png",
    "9H": "MobilePlayingCardApp/assets/img/theme4/Hearts9.png",
    "1H": "MobilePlayingCardApp/assets/img/theme4/Hearts10.png",
    "JH": "MobilePlayingCardApp/assets/img/theme4/HeartsJack.png",
    "QH": "MobilePlayingCardApp/assets/img/theme4/HeartsQueen.png",
    "KH": "MobilePlayingCardApp/assets/img/theme4/HeartsKing.png",

    # Diamonds
    "AD": "MobilePlayingCardApp/assets/img/theme4/DiamondsA.png",
    "2D": "MobilePlayingCardApp/assets/img/theme4/Diamonds2.png",
    "3D": "MobilePlayingCardApp/assets/img/theme4/Diamonds3.png",
    "4D": "MobilePlayingCardApp/assets/img/theme4/Diamonds4.png",
    "5D": "MobilePlayingCardApp/assets/img/theme4/Diamonds5.png",
    "6D": "MobilePlayingCardApp/assets/img/theme4/Diamonds6.png",
    "7D": "MobilePlayingCardApp/assets/img/theme4/Diamonds7.png",
    "8D": "MobilePlayingCardApp/assets/img/theme4/Diamonds8.png",
    "9D": "MobilePlayingCardApp/assets/img/theme4/Diamonds9.png",
    "1D": "MobilePlayingCardApp/assets/img/theme4/Diamonds10.png",
    "JD": "MobilePlayingCardApp/assets/img/theme4/DiamondsJack.png",
    "QD": "MobilePlayingCardApp/assets/img/theme4/DiamondsQueen.png",
    "KD": "MobilePlayingCardApp/assets/img/theme4/DiamondsKing.png",

    # Clubs
    "AC": "MobilePlayingCardApp/assets/img/theme4/ClubsA.png",
    "2C": "MobilePlayingCardApp/assets/img/theme4/Clubs2.png",
    "3C": "MobilePlayingCardApp/assets/img/theme4/Clubs3.png",
    "4C": "MobilePlayingCardApp/assets/img/theme4/Clubs4.png",
    "5C": "MobilePlayingCardApp/assets/img/theme4/Clubs5.png",
    "6C": "MobilePlayingCardApp/assets/img/theme4/Clubs6.png",
    "7C": "MobilePlayingCardApp/assets/img/theme4/Clubs7.png",
    "8C": "MobilePlayingCardApp/assets/img/theme4/Clubs8.png",
    "9C": "MobilePlayingCardApp/assets/img/theme4/Clubs9.png",
    "1C": "MobilePlayingCardApp/assets/img/theme4/Clubs10.png",
    "JC": "MobilePlayingCardApp/assets/img/theme4/ClubsJack.png",
    "QC": "MobilePlayingCardApp/assets/img/theme4/ClubsQueen.png",
    "KC": "MobilePlayingCardApp/assets/img/theme4/ClubsKing.png",

    # Spades
    "AS": "MobilePlayingCardApp/assets/img/theme4/SpadesA.png",
    "2S": "MobilePlayingCardApp/assets/img/theme4/Spades2.png",
    "3S": "MobilePlayingCardApp/assets/img/theme4/Spades3.png",
    "4S": "MobilePlayingCardApp/assets/img/theme4/Spades4.png",
    "5S": "MobilePlayingCardApp/assets/img/theme4/Spades5.png",
    "6S": "MobilePlayingCardApp/assets/img/theme4/Spades6.png",
    "7S": "MobilePlayingCardApp/assets/img/theme4/Spades7.png",
    "8S": "MobilePlayingCardApp/assets/img/theme4/Spades8.png",
    "9S": "MobilePlayingCardApp/assets/img/theme4/Spades9.png",
    "1S": "MobilePlayingCardApp/assets/img/theme4/Spades10.png",
    "JS": "MobilePlayingCardApp/assets/img/theme4/SpadesJack.png",
    "QS": "MobilePlayingCardApp/assets/img/theme4/SpadesQueen.png",
    "KS": "MobilePlayingCardApp/assets/img/theme4/SpadesKing.png",

    # Jokers
    "RJ": "MobilePlayingCardApp/assets/img/theme2/Joker Red.png",
    "BJ": "MobilePlayingCardApp/assets/img/theme2/Joker Black.png",
}))
        themes.append(Theme(themeslst[4],300,'assets/img/theme5/Hearts/Joker.png','assets/img/theme5/CardBackBlue.png',{
          # Hearts
    "AH": "MobilePlayingCardApp/assets/img/theme5/Hearts/Ace.png",
    "2H": "MobilePlayingCardApp/assets/img/theme5/Hearts/2.png",
    "3H": "MobilePlayingCardApp/assets/img/theme5/Hearts/3.png",
    "4H": "MobilePlayingCardApp/assets/img/theme5/Hearts/4.png",
    "5H": "MobilePlayingCardApp/assets/img/theme5/Hearts/5.png",
    "6H": "MobilePlayingCardApp/assets/img/theme5/Hearts/6.png",
    "7H": "MobilePlayingCardApp/assets/img/theme5/Hearts/7.png",
    "8H": "MobilePlayingCardApp/assets/img/theme5/Hearts/8.png",
    "9H": "MobilePlayingCardApp/assets/img/theme5/Hearts/9.png",
    "1H": "MobilePlayingCardApp/assets/img/theme5/Hearts/10.png",
    "JH": "MobilePlayingCardApp/assets/img/theme5/Hearts/Jack.png",
    "QH": "MobilePlayingCardApp/assets/img/theme5/Hearts/Queen.png",
    "KH": "MobilePlayingCardApp/assets/img/theme5/Hearts/King.png",

    # Diamonds
    "AD": "MobilePlayingCardApp/assets/img/theme5/Diamonds/Ace.png",
    "2D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/2.png",
    "3D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/3.png",
    "4D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/4.png",
    "5D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/5.png",
    "6D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/6.png",
    "7D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/7.png",
    "8D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/8.png",
    "9D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/9.png",
    "1D": "MobilePlayingCardApp/assets/img/theme5/Diamonds/10.png",
    "JD": "MobilePlayingCardApp/assets/img/theme5/Diamonds/Jack.png",
    "QD": "MobilePlayingCardApp/assets/img/theme5/Diamonds/Queen.png",
    "KD": "MobilePlayingCardApp/assets/img/theme5/Diamonds/King.png",

    # Clubs
    "AC": "MobilePlayingCardApp/assets/img/theme5/Clubs/Ace.png",
    "2C": "MobilePlayingCardApp/assets/img/theme5/Clubs/2.png",
    "3C": "MobilePlayingCardApp/assets/img/theme5/Clubs/3.png",
    "4C": "MobilePlayingCardApp/assets/img/theme5/Clubs/4.png",
    "5C": "MobilePlayingCardApp/assets/img/theme5/Clubs/5.png",
    "6C": "MobilePlayingCardApp/assets/img/theme5/Clubs/6.png",
    "7C": "MobilePlayingCardApp/assets/img/theme5/Clubs/7.png",
    "8C": "MobilePlayingCardApp/assets/img/theme5/Clubs/8.png",
    "9C": "MobilePlayingCardApp/assets/img/theme5/Clubs/9.png",
    "1C": "MobilePlayingCardApp/assets/img/theme5/Clubs/10.png",
    "JC": "MobilePlayingCardApp/assets/img/theme5/Clubs/Jack.png",
    "QC": "MobilePlayingCardApp/assets/img/theme5/Clubs/Queen.png",
    "KC": "MobilePlayingCardApp/assets/img/theme5/Clubs/King.png",

    # Spades
    "AS": "MobilePlayingCardApp/assets/img/theme4/Spades/Ace.png",
    "2S": "MobilePlayingCardApp/assets/img/theme4/Spades/2.png",
    "3S": "MobilePlayingCardApp/assets/img/theme4/Spades/3.png",
    "4S": "MobilePlayingCardApp/assets/img/theme4/Spades/4.png",
    "5S": "MobilePlayingCardApp/assets/img/theme4/Spades/5.png",
    "6S": "MobilePlayingCardApp/assets/img/theme4/Spades/6.png",
    "7S": "MobilePlayingCardApp/assets/img/theme4/Spades/7.png",
    "8S": "MobilePlayingCardApp/assets/img/theme4/Spades/8.png",
    "9S": "MobilePlayingCardApp/assets/img/theme4/Spades/9.png",
    "1S": "MobilePlayingCardApp/assets/img/theme4/Spades/10.png",
    "JS": "MobilePlayingCardApp/assets/img/theme4/Spades/Jack.png",
    "QS": "MobilePlayingCardApp/assets/img/theme4/Spades/Queen.png",
    "KS": "MobilePlayingCardApp/assets/img/theme4/Spades/King.png",

    # Jokers
    "RJ": "MobilePlayingCardApp/assets/img/theme5/Hearts/Joker.png",
    "BJ": "MobilePlayingCardApp/assets/img/theme5/Clubs/Joker.png",  
        }))
        
    def get_theme(shop,theme_name):
        for theme in shop.inventory: #Iterates through all the themes available
            if theme_name == theme.name: #Returns required theme once found
                return theme

    def update(shop,app):
        shop.filling_shop_inventory(app) #Updates the Shop UI
        app.save.quick_save(app) #Saves the minor changes to the shop

    def equip_theme(shop,theme,app):
        if theme in shop.unlocked_inventory: #Checks the theme is in the player's inventory
            shop.equipped = theme #Equips the chosen theme
            shop.update(app) #Updates the shop UI and saves equipped theme
    
    def buy_theme(shop,theme_name,app):
        theme = shop.get_theme(theme_name) #Returns the theme object
        if theme_name not in shop.unlocked_inventory: #Checks if theme is not already in the player's inventory 
            if theme.cost <= shop.coin_count: #Checks if the player has enough coins to buy the
                shop.unlocked_inventory.append(theme.name) #Adds theme to player's inventory 
                shop.coin_count -= theme.cost #Removes cost of the theme from the player's coin count
                shop.update(app) #Updates the shop UI and saves equipped theme
            else: #Displays a pop-up which tells the player how many coins they have versus the cost of the theme
                Dialog = Shop_Dialog(theme.cost,shop.coin_count)
                Dialog.open()

    def filling_shop_inventory(shop,app):
        grid = app.get_widget("grid","MDShop") #Returns the grid within the shop display
        grid.clear_widgets() #Clears the shop grid
        for theme_ in shop.inventory: #Iterates through the shop inventory
            display = Shop_Card(theme_) #Creates an UI object which displays the choosen theme and an interactable button to buy/equip the theme
            grid.add_widget(display) #Adds UI object to the grid