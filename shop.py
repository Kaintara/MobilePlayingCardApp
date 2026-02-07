from ui import Shop_Dialog, Shop_Card

class Theme:
    def __init__(theme,name,cost,front,back,dictionary):
        theme.name = name
        theme.cost = cost
        theme.front_img = front
        theme.back_img = back
        theme.asset_dict = dictionary

class Shop:
    def __init__(shop):
        shop.inventory = []
        shop.equipped = 'Classic'
        shop.unlocked_inventory = ['Classic']
        shop.coin_count = 0

    def set_all_themes(shop):
        themeslst = ['Classic','Blue_Classic','Dark-Red']
        themes = shop.inventory
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
        themes.append(Theme(themeslst[1], 10,'assets/img/theme2/Spades 13.png','assets/img/theme2/Back Blue 1.png',{
    # Hearts (plural)
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

    # Diamond (singular — your requirement)
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

    # Clubs (plural)
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

    # Spades (plural)
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
        themes.append(Theme(themeslst[2],50,''))
        #themes.append(Theme(''))
    def get_theme(shop,theme_name):
        for theme in shop.inventory:
            if theme_name == theme.name:
                return theme

    def update(shop,app):
        shop.filling_shop_inventory(app)
        app.save.quick_save(app)
        print("Shop has been updated!")

    def equip_theme(shop,theme,app):
        if theme in shop.unlocked_inventory:
            shop.equipped = theme
            shop.update(app)
    
    def buy_theme(shop,theme_name,app):
        theme = shop.get_theme(theme_name)
        if theme_name not in shop.unlocked_inventory:
            if theme.cost <= shop.coin_count:
                shop.unlocked_inventory.append(theme.name)
                shop.coin_count -= theme.cost
                shop.update(app)
            else:
                Dialog = Shop_Dialog(theme.cost,shop.coin_count)
                Dialog.open()

    def filling_shop_inventory(shop,app):
        grid = app.get_widget("grid","MDShop")
        grid.clear_widgets()
        for theme_ in shop.inventory:
            display = Shop_Card(theme_)
            grid.add_widget(display)

'''
ShopTest = Shop()
ShopTest.set_all_themes()
print(ShopTest.inventory[0].name,ShopTest.inventory[1].name)
ShopTest.equip_theme('Blue_Classic')
print(ShopTest.equipped)
ShopTest.equipped = 'Blue_Classic'
ShopTest.equip_theme('Classic')
print(ShopTest.equipped)
print(ShopTest.get_theme('Classic').cost)
'''
