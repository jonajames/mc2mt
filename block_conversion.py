
enabled_mods = [
#    "quartz",
#    "nether",
]

air = ("air",15,0)
unknown_blocks = []
def convertBlock(block):
    prefix,name = block['name'].split(":")
    if name == air: return air

    if name in default_table:
        return getFromTable(default_table,name,block)

    if name in ["granite","diorite","granite","andesite"]:
        return ("default:stone",0,0)

    if "_ore" in name:
        return ("default:stone_with_gold",255,0)

    stairname = name
    if "_slab" in stairname:
        for term,translation in stairs_translation_array: stairname = stairname.replace(term,translation)
        if "slab_"+stairname in stairs_valid_array: return ("stairs:slab_"+stairname,15,type2facedir(block))
    if "_stairs" in stairname:
        for term,translation in stairs_translation_array: stairname = stairname.replace(term,translation)
        stairname = "stair_"+shape2stair(block)+stairname
        if stairname in stairs_valid_array: return ("stairs:"+stairname,15,stair2facedir(block))

    if "white_bed" == name:
        if block["part"] == "foot": return ("beds:bed_bottom",0,facing2facedir(block))
        else: return air

    if "_door" in name:
        doorname = name + (block["open"] == "false" and "_a" or "_b")
        if doorname in door_table: return getFromTable(door_table,doorname,block)

    if "_stained_glass_pane" in name: return ("xpanes:pane_flat",15,cardinal2facedir(block))
    if "_stained_glass" in name: return ("default:glass",15,0)
            
    if "quartz" in enabled_mods:
        if name in quartz_table: return getFromTable(quartz_table,name,block)
            
    # Unknown Block
    if block not in unknown_blocks:
        unknown_blocks.append(block)
        print("Unknown Block",block)
    return air

# param conversion
def getFromTable(table,name,block):
    param0,param1,param2 = table[name]
    if callable(param2): return (param0,param1,param2(block))
    return param0,param1,param2

def cardinal2facedir(block):
    return block['north'] and 4 or block['south'] and 8 or block['east'] and 12 or block['west'] and 16

def type2facedir(block):
    return {"bottom":0,"top":20}[block["type"]]

def facing2facedir(block):
    return {"north":0,"east":1,"south":2,"west":3}[block["facing"]]

def facing2wallmounted(block):
    return {"north":1,"east":2,"south":3,"west":4}[block["facing"]]

def stair2facedir(block):
    return facing2facedir(block) + {"top":0,"bottom":20}[block["half"]]

def shape2stair(block):
    return {"straight":"","outer_right":"outer_","outer_left":"outer_","inner_right":"inner_","inner_left":"inner_"}[block["shape"]]

def level2flowingliquid(block):
    return int(block["level"])
     
############
#  TABLES  #
############

# format is:
# "minecraft_name" : ("minetest:param0",param1,param2),
# param0 is itemstring
# param1 is usually lighting
#        0 for full solid blocks
#        15 for non-full/transparent blocks
#        255 for light-emitting blocks
# param2 depends on paramtype

default_table = {
    "":("ignore",15,0),
    "air":("air",15,0),
    "cave_air":("air",15,0),
    "":("beds:bed_bottom",0,0),
    "":("beds:bed_top",0,0),
    "":("beds:fancy_bed_bottom",0,0),
    "":("beds:fancy_bed_top",0,0),
    "":("bones:bones",0,0),
    "":("butterflies:butterfly_red",0,0),
    "":("butterflies:butterfly_violet",0,0),
    "":("butterflies:butterfly_white",0,0),
    "":("butterflies:hidden_butterfly_red",0,0),
    "":("butterflies:hidden_butterfly_violet",0,0),
    "":("butterflies:hidden_butterfly_white",0,0),
    "":("carts:brakerail",0,0),
    "":("carts:powerrail",0,0),
    "rail":("carts:rail",15,0),
    "":("default:acacia_bush_leaves",0,0),
    "":("default:acacia_bush_sapling",0,0),
    "":("default:acacia_bush_stem",0,0),
    "acacia_leaves":("default:acacia_leaves",0,0),
    "acacia_sapling":("default:acacia_sapling",0,0),
    "acacia_log":("default:acacia_tree",0,0),
    "acacia_planks":("default:acacia_wood",0,0),
    "apple":("default:apple",15,0),
    "pumpkin":("default:apple",15,0),
    "":("default:apple_mark",0,0),
    "birch_leaves":("default:aspen_leaves",15,0),
    "birch_sapling":("default:aspen_sapling",15,0),
    "birch_log":("default:aspen_tree",0,0),
    "birch_planks":("default:aspen_wood",0,0),
    "":("default:blueberry_bush_leaves",0,0),
    "":("default:blueberry_bush_leaves_with_berries",0,0),
    "":("default:blueberry_bush_sapling",0,0),
    "bookshelf":("default:bookshelf",0,0),
    "bricks":("default:brick",0,0),
    "":("default:bronzeblock",0,0),
    "":("default:bush_leaves",0,0),
    "":("default:bush_sapling",0,0),
    "":("default:bush_stem",0,0),
    "cactus":("default:cactus",0,0),
    "":("default:cave_ice",0,0),
    "chest":("default:chest",0,0),
    "":("default:chest_locked",0,0),
    "":("default:chest_locked_open",0,0),
    "":("default:chest_open",0,0),
    "clay":("default:clay",0,0),
    "":("default:cloud",0,0),
    "":("default:coalblock",0,0),
    "cobblestone":("default:cobble",0,0),
    "end_stone_bricks":("default:copperblock",0,0),
    "end_stone":("default:copperblock",0,0),
    "bubble_coral_block":("default:coral_brown",0,0),
    "tube_coral_block":("default:coral_cyan",0,0),
    "horn_coral_block":("default:coral_green",0,0),
    "fire_coral_block":("default:coral_orange",0,0),
    "brain_coral_block":("default:coral_pink",0,0),
    "dead_bubble_coral_block":("default:coral_skeleton",0,0),
    "dead_tube_coral_block":("default:coral_skeleton",0,0),
    "dead_horn_coral_block":("default:coral_skeleton",0,0),
    "dead_fire_coral_block":("default:coral_skeleton",0,0),
    "dead_brain_coral_block":("default:coral_skeleton",0,0),
    "":("default:desert_cobble",0,0),
    "":("default:desert_sand",0,0),
    "":("default:desert_sandstone",0,0),
    "smooth_sandstone":("default:desert_sandstone_block",0,0),
    "":("default:desert_sandstone_brick",0,0),
    "":("default:desert_stone",0,0),
    "":("default:desert_stone_block",0,0),
    "":("default:desert_stonebrick",0,0),
    "":("default:diamondblock",0,0),
    "dirt":("default:dirt",0,0),
    "":("default:dirt_with_coniferous_litter",0,0),
    "":("default:dirt_with_dry_grass",0,0),
    "grass_block":("default:dirt_with_grass",0,0),
    "":("default:dirt_with_grass_footsteps",0,0),
    "":("default:dirt_with_rainforest_litter",0,0),
    "":("default:dirt_with_snow",0,0),
    "":("default:dry_dirt",0,0),
    "":("default:dry_dirt_with_dry_grass",0,0),
    "":("default:dry_grass_1",0,0),
    "":("default:dry_grass_2",0,0),
    "":("default:dry_grass_3",0,0),
    "":("default:dry_grass_4",0,0),
    "":("default:dry_grass_5",0,0),
    "":("default:dry_shrub",0,0),
    "":("default:emergent_jungle_sapling",0,0),
    "acacia_fence":("default:fence_acacia_wood",0,0),
    "birch_fence":("default:fence_aspen_wood",0,0),
    "jungle_fence":("default:fence_junglewood",0,0),
    "spruce_fence":("default:fence_pine_wood",0,0),
    "":("default:fence_rail_acacia_wood",0,0),
    "":("default:fence_rail_aspen_wood",0,0),
    "":("default:fence_rail_junglewood",0,0),
    "":("default:fence_rail_pine_wood",0,0),
    "":("default:fence_rail_wood",0,0),
    "oak_fence":("default:fence_wood",0,0),
    #"":("default:fern_1",0,0),
    "fern":("default:fern_2",15,0),
    "large_fern":("default:fern_3",15,0),
    "":("default:furnace",0,0),
    "":("default:furnace_active",0,0),
    "glass":("default:glass",15,0),
    "":("default:goldblock",0,0),
    #"":("default:grass_1",15,0),
    #"":("default:grass_2",15,0),
    "grass":("default:grass_3",15,0),
    #"":("default:grass_4",15,0),
    #"":("default:grass_5",15,0),
    "gravel":("default:gravel",0,0),
    "ice":("default:ice",0,0),
    "tall_grass":("default:junglegrass",15,0),
    "jungle_leaves":("default:jungleleaves",15,0),
    "jungle_sapling":("default:junglesapling",15,0),
    "jungle_log":("default:jungletree",0,0),
    "jungle_planks":("default:junglewood",0,0),
    "":("default:ladder_steel",0,0),
    "":("default:ladder_wood",0,0),
    "":("default:large_cactus_seedling",0,0),
    "":("default:lava_flowing",0,0),
    "lava":("default:lava_source",255,level2flowingliquid),
    "oak_leaves":("default:leaves",15,0),
    "":("default:marram_grass_1",0,0),
    "":("default:marram_grass_2",0,0),
    "":("default:marram_grass_3",0,0),
    "":("default:mese",0,0),
    "":("default:mese_post_light",0,0),
    "":("default:meselamp",0,0),
    "mossy_stone_bricks":("default:mossycobble",0,0),
    "obsidian":("default:obsidian",0,0),
    "":("default:obsidian_block",0,0),
    "":("default:obsidian_glass",0,0),
    "":("default:obsidianbrick",0,0),
    "sugar_cane":("default:papyrus",15,0),
    "":("default:permafrost",0,0),
    "":("default:permafrost_with_moss",0,0),
    "":("default:permafrost_with_stones",0,0),
    "":("default:pine_bush_needles",0,0),
    "":("default:pine_bush_sapling",0,0),
    "":("default:pine_bush_stem",0,0),
    "spruce_leaves":("default:pine_needles",15,0),
    "spruce_sapling":("default:pine_sapling",15,0),
    "spruce_log":("default:pine_tree",0,0),
    "spruce_planks":("default:pine_wood",0,0),
    "":("default:river_water_flowing",15,level2flowingliquid),
    "":("default:river_water_source",15,level2flowingliquid),
    "sand":("default:sand",0,0),
    "":("default:sand_with_kelp",0,0),
    "sandstone":("default:sandstone",0,0),
    "chiseled_sandstone":("default:sandstone_block",0,0),
    "cut_sandstone":("default:sandstone_block",0,0),
    "smooth_sandstone":("default:sandstone_block",0,0),
    "":("default:sandstonebrick",0,0),
    "oak_sapling":("default:sapling",0,0),
    "":("default:sign_wall_steel",0,0),
    "sign":("default:sign_wall_wood",0,facing2wallmounted),
    "":("default:silver_sand",0,0),
    "diorite":("default:silver_sandstone",0,0),
    "polished_diorite":("default:silver_sandstone_block",0,0),
    "":("default:silver_sandstone_brick",0,0),
    "snow":("default:snow",0,0),
    "snow_block":("default:snowblock",0,0),
    "iron_block":("default:steelblock",0,0),
    "stone":("default:stone",0,0),
    "polished_andesite":("default:stone_block",0,0),
    "smooth_stone":("default:stone_block",0,0),
    "coal_ore":("default:stone_with_coal",0,0),
    "copper_ore":("default:stone_with_copper",0,0),
    "diamond_ore":("default:stone_with_diamond",0,0),
    "gold_ore":("default:stone_with_gold",0,0),
    "iron_ore":("default:stone_with_iron",0,0),
    "redstone_ore":("default:stone_with_mese",0,0),
    "tin_ore":("default:stone_with_tin",0,0),
    "stone_bricks":("default:stonebrick",0,0),
    "cracked_stone_bricks":("default:stonebrick",0,0),
    "":("default:tinblock",0,0),
    "torch":("default:torch",255,facing2wallmounted),
    #"":("default:torch_ceiling",0,0),
    "wall_torch":("default:torch_wall",255,facing2wallmounted),
    "oak_log":("default:tree",0,0),
    #"":("default:water_flowing",15,level2flowingliquid),
    "water":("default:water_source",15,level2flowingliquid),
    "oak_planks":("default:wood",0,0),
    "":("farming:cotton_1",0,0),
    "":("farming:cotton_2",0,0),
    "":("farming:cotton_3",0,0),
    "":("farming:cotton_4",0,0),
    "":("farming:cotton_5",0,0),
    "":("farming:cotton_6",0,0),
    "":("farming:cotton_7",0,0),
    "":("farming:cotton_8",0,0),
    "":("farming:desert_sand_soil",0,0),
    "":("farming:desert_sand_soil_wet",0,0),
    "":("farming:dry_soil",0,0),
    "":("farming:dry_soil_wet",0,0),
    "":("farming:seed_cotton",0,0),
    "":("farming:seed_wheat",0,0),
    "":("farming:soil",0,0),
    "":("farming:soil_wet",0,0),
    "":("farming:straw",0,0),
    #"":("farming:wheat_1",0,0),
    #"":("farming:wheat_2",0,0),
    #"":("farming:wheat_3",0,0),
    #"":("farming:wheat_4",0,0),
    #"":("farming:wheat_5",0,0),
    #"":("farming:wheat_6",0,0),
    #"":("farming:wheat_7",0,0),
    "cornflower":("farming:wheat_8",0,0),
    "":("fire:basic_flame",0,0),
    "":("fire:permanent_flame",0,0),
    "":("fireflies:firefly",0,0),
    "":("fireflies:firefly_bottle",0,0),
    "":("fireflies:hidden_firefly",0,0),
    "":("flowers:chrysanthemum_green",15,0),
    "azure_bluet":("flowers:dandelion_white",15,0),
    "oxeye_daisy":("flowers:dandelion_white",15,0),
    "dandelion":("flowers:dandelion_yellow",15,0),
    "blue_orchid":("flowers:geranium",15,0),
    "brown_mushroom":("flowers:mushroom_brown",15,0),
    "red_mushroom":("flowers:mushroom_red",15,0),
    "poppy":("flowers:rose",15,0),
    "orange_tulip":("flowers:tulip",15,0),
    "red_tulip":("flowers:tulip_black",15,0),
    "white_tulip":("flowers:tulip",15,0),
    "pink_tulip":("flowers:tulip_black",15,0),
    "allium":("flowers:viola",15,0),
    "":("flowers:waterlily",15,0),
    "":("flowers:waterlily_waving",15,0),
    "":("tnt:boom",0,0),
    "":("tnt:gunpowder",0,0),
    "":("tnt:gunpowder_burning",0,0),
    "":("tnt:tnt",0,0),
    "":("tnt:tnt_burning",0,0),
    "":("vessels:drinking_glass",0,0),
    "":("vessels:glass_bottle",0,0),
    "":("vessels:shelf",0,0),
    "":("vessels:steel_bottle",0,0),
    "stone_brick_wall":("walls:cobble",15,0),
    "":("walls:desertcobble",0,0),
    "":("walls:mossycobble",0,0),
    "":("wool:black",0,0),
    "":("wool:blue",0,0),
    "":("wool:brown",0,0),
    "":("wool:cyan",0,0),
    "":("wool:dark_green",0,0),
    "":("wool:dark_grey",0,0),
    "":("wool:green",0,0),
    "":("wool:grey",0,0),
    "":("wool:magenta",0,0),
    "":("wool:orange",0,0),
    "":("wool:pink",0,0),
    "":("wool:red",0,0),
    "":("wool:violet",0,0),
    "":("wool:white",0,0),
    "":("wool:yellow",0,0),
    "":("xpanes:bar",0,0),
    "iron_bars":("xpanes:bar_flat",15,cardinal2facedir),
    "":("xpanes:door_steel_bar_a",0,0),
    "":("xpanes:door_steel_bar_b",0,0),
    "":("xpanes:obsidian_pane",0,0),
    "":("xpanes:obsidian_pane_flat",0,0),
    "":("xpanes:pane",0,0),
    "glass_pane":("xpanes:pane_flat",15,cardinal2facedir),
    "":("xpanes:trapdoor_steel_bar",0,0),
    "":("xpanes:trapdoor_steel_bar_open",0,0),
}

stairs_translation_array = [
    ("_slab" , ""),
    ("_stairs" , ""),
    ("oak" , "wood"),
    ("spruce" , "pine"),
    ("birch" , "aspen"),
    ("jungle" , "junglewood"),
    ("dark_" , ""),
    ("pietrified_" , ""),
    ("cobblestone" , "cobble"),
    ("red" , "desert"),
    ("purpur" , "gold"),
    ("prismarine" , "ice"),
    ("ice_brick" , "ice"),
    ("smooth" , "block"),
    ("cut" , "block"),
    ("polished", "block"),
    ("mossy_" , "mossy"),
    ("mossystone_brick" , "mossycobble"),
    ("end_stone_brick" , "copperblock"),
    ("granite" , "desert_cobble"),
    ("adensite" , "stone"),
    ("diorite" , "silver_sandstone"),
    ("stone_brick" , "stonebrick")
]

stairs_valid_array = [
    "slab_acacia_wood",
    "slab_aspen_wood",
    "slab_brick",
    "slab_bronzeblock",
    "slab_cobble",
    "slab_copperblock",
    "slab_desert_cobble",
    "slab_desert_sandstone",
    "slab_desert_sandstone_block",
    "slab_desert_sandstone_brick",
    "slab_desert_stone",
    "slab_desert_stone_block",
    "slab_desert_stonebrick",
    "slab_glass",
    "slab_goldblock",
    "slab_ice",
    "slab_junglewood",
    "slab_mossycobble",
    "slab_obsidian",
    "slab_obsidian_block",
    "slab_obsidian_glass",
    "slab_obsidianbrick",
    "slab_pine_wood",
    "slab_sandstone",
    "slab_sandstone_block",
    "slab_sandstonebrick",
    "slab_silver_sandstone",
    "slab_silver_sandstone_block",
    "slab_silver_sandstone_brick",
    "slab_snowblock",
    "slab_steelblock",
    "slab_stone",
    "slab_stone_block",
    "slab_stonebrick",
    "slab_straw",
    "slab_tinblock",
    "slab_wood",
    
    "stair_acacia_wood",
    "stair_aspen_wood",
    "stair_brick",
    "stair_bronzeblock",
    "stair_cobble",
    "stair_copperblock",
    "stair_desert_cobble",
    "stair_desert_sandstone",
    "stair_desert_sandstone_block",
    "stair_desert_sandstone_brick",
    "stair_desert_stone",
    "stair_desert_stone_block",
    "stair_desert_stonebrick",
    "stair_glass",
    "stair_goldblock",
    "stair_ice",
    "stair_junglewood",
    "stair_mossycobble",
    "stair_obsidian",
    "stair_obsidian_block",
    "stair_obsidian_glass",
    "stair_obsidianbrick",
    "stair_pine_wood",
    "stair_sandstone",
    "stair_sandstone_block",
    "stair_sandstonebrick",
    "stair_silver_sandstone",
    "stair_silver_sandstone_block",
    "stair_silver_sandstone_brick",
    "stair_snowblock",
    "stair_steelblock",
    "stair_stone",
    "stair_stone_block",
    "stair_stonebrick",
    "stair_straw",
    "stair_tinblock",
    "stair_wood",
    
    "stair_inner_acacia_wood",
    "stair_inner_aspen_wood",
    "stair_inner_brick",
    "stair_inner_bronzeblock",
    "stair_inner_cobble",
    "stair_inner_copperblock",
    "stair_inner_desert_cobble",
    "stair_inner_desert_sandstone",
    "stair_inner_desert_sandstone_block",
    "stair_inner_desert_sandstone_brick",
    "stair_inner_desert_stone",
    "stair_inner_desert_stone_block",
    "stair_inner_desert_stonebrick",
    "stair_inner_glass",
    "stair_inner_goldblock",
    "stair_inner_ice",
    "stair_inner_junglewood",
    "stair_inner_mossycobble",
    "stair_inner_obsidian",
    "stair_inner_obsidian_block",
    "stair_inner_obsidian_glass",
    "stair_inner_obsidianbrick",
    "stair_inner_pine_wood",
    "stair_inner_sandstone",
    "stair_inner_sandstone_block",
    "stair_inner_sandstonebrick",
    "stair_inner_silver_sandstone",
    "stair_inner_silver_sandstone_block",
    "stair_inner_silver_sandstone_brick",
    "stair_inner_snowblock",
    "stair_inner_steelblock",
    "stair_inner_stone",
    "stair_inner_stone_block",
    "stair_inner_stonebrick",
    "stair_inner_straw",
    "stair_inner_tinblock",
    "stair_inner_wood",
    
    "stair_outer_acacia_wood",
    "stair_outer_aspen_wood",
    "stair_outer_brick",
    "stair_outer_bronzeblock",
    "stair_outer_cobble",
    "stair_outer_copperblock",
    "stair_outer_desert_cobble",
    "stair_outer_desert_sandstone",
    "stair_outer_desert_sandstone_block",
    "stair_outer_desert_sandstone_brick",
    "stair_outer_desert_stone",
    "stair_outer_desert_stone_block",
    "stair_outer_desert_stonebrick",
    "stair_outer_glass",
    "stair_outer_goldblock",
    "stair_outer_ice",
    "stair_outer_junglewood",
    "stair_outer_mossycobble",
    "stair_outer_obsidian",
    "stair_outer_obsidian_block",
    "stair_outer_obsidian_glass",
    "stair_outer_obsidianbrick",
    "stair_outer_pine_wood",
    "stair_outer_sandstone",
    "stair_outer_sandstone_block",
    "stair_outer_sandstonebrick",
    "stair_outer_silver_sandstone",
    "stair_outer_silver_sandstone_block",
    "stair_outer_silver_sandstone_brick",
    "stair_outer_snowblock",
    "stair_outer_steelblock",
    "stair_outer_stone",
    "stair_outer_stone_block",
    "stair_outer_stonebrick",
    "stair_outer_straw",
    "stair_outer_tinblock",
    "stair_outer_wood",
]

door_table = {
    "":("doors:door_glass_a",15,facing2facedir),
    "":("doors:door_glass_b",15,facing2facedir),
    "":("doors:door_obsidian_glass_a",15,facing2facedir),
    "":("doors:door_obsidian_glass_b",15,facing2facedir),
    "iron_door_a":("doors:door_steel_a",15,facing2facedir),
    "iron_foor_b":("doors:door_steel_b",15,facing2facedir),
    "oak_door_a":("doors:door_wood_a",15,facing2facedir),
    "oak_door_b":("doors:door_wood_b",15,facing2facedir),
    "":("doors:gate_acacia_wood_closed",15,facing2facedir),
    "":("doors:gate_acacia_wood_open",15,facing2facedir),
    "":("doors:gate_aspen_wood_closed",15,facing2facedir),
    "":("doors:gate_aspen_wood_open",15,facing2facedir),
    "":("doors:gate_junglewood_closed",15,facing2facedir),
    "":("doors:gate_junglewood_open",15,facing2facedir),
    "":("doors:gate_pine_wood_closed",15,facing2facedir),
    "":("doors:gate_pine_wood_open",15,facing2facedir),
    "":("doors:gate_wood_closed",15,facing2facedir),
    "":("doors:gate_wood_open",15,facing2facedir),
    "":("doors:hidden",15,facing2facedir),
    "":("doors:trapdoor",15,facing2facedir),
    "":("doors:trapdoor_open",15,facing2facedir),
    "":("doors:trapdoor_steel",15,facing2facedir),
    "":("doors:trapdoor_steel_open",15,facing2facedir),
}

quartz_table = {
    "quartz_block" : ("quartz:block",0,0)
}


if __name__ == '__main__':
    print("Reading unknown blocks from stdin and testing conversion")
    lines = []
    converted = []
    while not lines or lines[-1]:
        try: lines.append(input())
        except EOFError: break
    for line in lines:
        if line[:14] != "Unknown Block ": continue
        block = eval(line[14:])
        param0,param1,param2 = convertBlock(block)
        if param0 != "air":
            print(f"Converted Block ({param0},{param1:02X},{param2:02X})")


