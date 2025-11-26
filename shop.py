class Theme:
    def __init__(theme,name,cost,front,back):
        theme.name = name
        theme.cost = cost
        theme.front_img = front
        theme.back_img = back

themeslst = ['Classic']

def set_all_themes():
    for theme in themeslst:
        globals()[theme] = Theme(theme, 0, 'assets/img/theme1/king_of_clubs2.png', 'assets/img/theme1/card_back_red.png')