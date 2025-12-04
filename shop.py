from ui import Shop_Dialog

class Theme:
    def __init__(theme,name,cost,front,back):
        theme.name = name
        theme.cost = cost
        theme.front_img = front
        theme.back_img = back

class Shop:
    def __init__(shop):
        shop.inventory = []
        shop.equipped = 'Classic'
        shop.unlocked_inventory = ['Classic']
        shop.coin_count = 0

    def set_all_themes(shop):
        themeslst = ['Classic','Blue_Classic']
        themes = shop.inventory
        themes.append(Theme(themeslst[0], 0, 'assets/img/theme1/king_of_clubs2.png', 'assets/img/theme1/card_back_red.png'))
        themes.append(Theme(themeslst[1], 10,'assets/img/theme2/Spades 13.png','assets/img/theme2/Back Blue 1.png'))

    def get_theme(shop,theme_name):
        for theme in shop.inventory:
            if theme_name == theme.name:
                return theme

    def update(shop):
        print("Shop has been updated!")

    def equip_theme(shop,theme):
        if theme in shop.unlocked_inventory:
            shop.equipped = theme
            shop.update()
    
    def buy_theme(shop,theme):
        if theme.name not in shop.unlocked_inventory:
            if theme.cost <= shop.coin_count:
                shop.unlocked_inventory.append(theme.name)
                shop.coin_count -= theme.cost
                shop.update()
            else:
                pass
                Dialog = Shop_Dialog(theme.cost,shop.coin_count)
                Dialog.open()

ShopTest = Shop()
ShopTest.set_all_themes()
print(ShopTest.inventory[0].name,ShopTest.inventory[1].name)
ShopTest.equip_theme('Blue_Classic')
print(ShopTest.equipped)
ShopTest.equipped = 'Blue_Classic'
ShopTest.equip_theme('Classic')
print(ShopTest.equipped)
print(ShopTest.get_theme('Classic').cost)