from Project.WoW.WoWhead.setup import WoWHead_addons 

bd_list = ['WoWHead']

def init_bd(bd_list: list, addons: dict) -> dict:
    bd = {}
    addons_list = list(addons.items())[0]

    for bd_ in bd_list:
        bd[bd_] = []
        for addon in addons:
            bd[bd_].append({addons_list[0]: addons_list[1]})

    return bd

wow_bd = init_bd(bd_list, WoWHead_addons)