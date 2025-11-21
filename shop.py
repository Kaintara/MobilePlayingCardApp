class Theme:
    def __init__(theme,name,cost,front,back):
        theme.name = name
        theme.cost = cost
        theme.front_img = front
        theme.back_img = back

class Shop:
    def __init__(shop):
        shop.inventory = []
        shop.equipped = 'Default'
        shop.unlocked_inventory = []
        shop.coin_count = 0

    def update(shop):
        print("Shop has been updated!")

    def equip_theme(shop,theme):
        if theme.name in shop.unlocked_inventory:
            shop.equipped = theme.name
            shop.update()
    
    def buy_theme(shop,theme):
        if theme.name not in shop.unlocked_inventory:
            if theme.cost <= shop.coin_count:
                shop.unlocked_inventory.append(theme.name)
                shop.coin_count -= theme.cost
                shop.update()
            else:
                pass
                #Dialog = Shop_Dialog(theme.cost)
                #Dialog.open()


