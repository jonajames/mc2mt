
enabled_mods = [
    "quartz",
]


default_table = {
    "air" : ("air",15,0),
    "cave_air" : ("air",15,0),
    "dirt" : ("default:dirt",15,0),
    "clay" : ("default:clay",15,0),
    "sand" : ("default:sand",15,0),
    "sandstone" : ("default:sandstone",15,0),
    "stone" : ("default:stone",15,0),
    "gravel" : ("default:gravel",15,0),
    "cactus" : ("default:cactus",15,0),
    "grass" : ("default:grass",15,0),
    "grass_block" : ("default:dirt_with_grass",15,0),
    "obsidian" : ("default:obsidian_block",15,0),
    "kelp_plant" : ("default:sand_with_kelp",15,0),
    "redstone_ore" : ("default:stone_with_mese",15,0),
    "coal_ore" : ("default:coal_ore",15,0),
    "iron_ore" : ("default:iron_ore",15,0),
    "copper_ore" : ("default:copper_ore",15,0),
    "tin_ore" : ("default:tin_ore",15,0),
    "gold_ore" : ("default:gold_ore",15,0),
    "diamond_ore" : ("default:diamond_ore",15,0),
    "bricks" : ("default:brick",15,0),
    "bookshelf" : ("default:bookshelf",15,0),
    "oak_planks" : ("default:wood",15,0),
    "birch_planks" : ("default:pine_wood",15,0),
    #   "name" : ("default:name",15,0),
}

default_materials = {
    "oak" : "wood",
    "birch" : "pine",
}

quartz_table = {
    "quartz_block" : ("quartz:block",15,0)
}

unknown_blocks = []
def convertBlock(block):
    prefix,name = block['name'].split(":")

    if name in default_table:
        return default_table[name]

    if name in ["diorite","granite","andesite"]:
        return ("default:stone",15,0)

    if "_ore" in name:
        return ("default:stone_with_gold",15,0)

    if "stair" in name:
        return ("stair:wood",15,stair2facedir(block))

    if "glass_pane" in name:
        return ("xpanes:pane_flat",15,cardinal2facedir(block))

    if "quartz" in enabled_mods and name in quartz_table:
        return quartz_table[name]
        
    # Unknown Block
    if block not in unknown_blocks:
        unknown_blocks.append(block)
        print("Unknown Block",block)
    return ("air",15,0)


def cardinal2facedir(block):
    return block['north'] and 4 or block['south'] and 8 or block['east'] and 12 or block['west'] and 16

def stair2facedir(block):
    half = {"top":0,"bottom":20}
    facing = {"north":0,"east":1,"south":2,"west":3}
    return half[block["half"]] + facing[block["facing"]]

