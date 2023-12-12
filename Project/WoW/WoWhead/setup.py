from Project.WoW.WoWhead.WoWHead import WoWHead

addons = ['wotlk']

WoWHead_addons = {}

for addon in addons:
    WoWHead_addons[addon] = WoWHead(addon=addon, test=[6948, 'Hearthstone'])