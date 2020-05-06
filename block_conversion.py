
enable_guessing = True
enabled_mods = [
    "xdecor",
    "quartz",
    "nether",
#    "bedrock",
    "stained_glass",
    "carpet",
    "mesecons",
#    "hardenedclay",
]

unknown_blocks = []
def convertBlock(block):
    prefix,name = block['name'].split(":")
    if name == "air": return ("air",15,0)

    # Enabled Mods
    if "stained_glass" in enabled_mods:
        if "_stained_glass_pane" in name: return ("xpanes:pane_flat",15,cardinal2facedir(block))
        if "_stained_glass" in name: return ("default:glass",15,0)
            
    if "quartz" in enabled_mods:
        if name in quartz_table: return getFromTable(quartz_table,name,block)

    if "nether" in enabled_mods:
        if name in nether_table: return getFromTable(nether_table,name,block)

    if "hardenedclay" in enabled_mods:
        if name in hardenedclay_table: return getFromTable(hardenedclay_table,name,block)

    if "bedrock" in enabled_mods:
        if name == "bedrock": return ("bedrock:bedrock",0,0)

    if "carpet" in enabled_mods:
        if name in carpet_table: return getFromTable(carpet_table,name,block)

    if "mesecons" in enabled_mods:
        if name in mesecons_table: return getFromTable(mesecons_table,name,block)

    if "xdecor" in enabled_mods:
        if name in xdecor_table: return getFromTable(xdecor_table,name,block)

    # Special cases
    if name in materials_table:
        return ("default:"+materials_table[name],0,0)
    
    if "_stairs" == name[-7:]:
        if name[:-7] in materials_table:
            return ("stairs:stair_"+shape2stair(block)+materials_table[name[:-7]],15,stair2facedir(block))

    if "_slab" == name[-5:]:
         if name[:-5] in materials_table:
             return ("stairs:slab_"+materials_table[name[:-5]],15,type2facedir(block))

    if "_bed" == name[-4:]:
        if block["part"] == "foot": return ("beds:bed_bottom",0,facing2facedir(block))
        else: return ("air",15,0)
 
    if "_door" in name:
        if name == "iron_door" : return getFromTable(door_table,"iron_door"+open2ab(block),block)
        return getFromTable(door_table,"oak_door"+open2ab(block),block)

    if "_trapdoor" in name:
        if name == "iron_trapdoor" : return getFromTable(door_table,"iron_trapdoor"+open2ab(block),block)
        return  getFromTable(door_table,"oak_trapdoor"+open2ab(block),block)
    
    # Default conversions
    if name in default_table:
        return getFromTable(default_table,name,block)

    for key in guessing_table:
        if key in "^"+name+"^":
            return getFromTable(guessing_table,key,block)
            
    # Unknown Block
    if block not in unknown_blocks:
        unknown_blocks.append(block)
        print("Unknown Block",block)
    return ("air",15,0)

# param conversion
def getFromTable(table,name,block):
    param0,param1,param2 = table[name]
    if callable(param2): return (param0,param1,param2(block))
    return param0,param1,param2
        
def cardinal2facedir(block):
    return block['north'] and 4 or block['south'] and 8 or block['east'] and 12 or block['west'] and 16

def type2facedir(block):
    return {"bottom":0,"top":20,"double":0}[block["type"]]

def facing2facedir(block):
    return {"north":1,"east":2,"south":3,"west":4}[block["facing"]]

def facing2wallmounted(block):
    return {"north":1,"east":2,"south":3,"west":4}[block["facing"]]

def stair2facedir(block):
    return {"north":0,"east":1,"south":2,"west":3}[block["facing"]] + {"top":0,"bottom":20}[block["half"]]

def shape2stair(block):
    return {"straight":"","outer_right":"outer_","outer_left":"outer_","inner_right":"inner_","inner_left":"inner_"}[block["shape"]]

def level2flowingliquid(block):
    return int(block["level"])

def open2ab(block):
    return block["open"] == "false" and "_a" or "_b"
     
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
    "prismarine_bricks" : ("default:ice",0,0),
    "mushroom_stem" : ("default:tree",0,0),
    "brown_mushroom_block" : ("default:leaves",0,0),
    "red_mushroom_block" : ("default:leaves",0,0),
    "dried_kelp_block" : ("default:acaia_bush_leaves",15,0),
    "wheat" : ("farming:straw",0,0),
    "sweet_berry_bush" : ("default:blueberry_bush_leaves_with_berries",15,0),
    "carrots" : ("default:apple",15,0),
    "oak_sign" : ("default:sign_wall_wood",15,1),
    "spruce_sign" : ("default:sign_wall_wood",15,1),
    "birch_sign" : ("default:sign_wall_wood",15,1),
    "jungle_sign" : ("default:sign_wall_wood",15,1),
    "acacia_sign" : ("default:sign_wall_wood",15,1),
    "dark_oak_sign" : ("default:sign_wall_wood",15,1),
    "acacia_fence":("default:fence_acacia_wood",0,0),
    "acacia_fence_gate":("doors:gate_acacia_wood_closed",0,2),
    "acacia_leaves":("default:acacia_leaves",0,0),
    "acacia_log":("default:acacia_tree",0,0),
    "acacia_planks":("default:acacia_wood",0,0),
    "acacia_sapling":("default:acacia_sapling",0,0),
    "acacia_slab":("stairs:slab_acacia_wood",0,0),
    "acacia_stairs":("stairs:stair_acacia_wood",0,1),
    "activator_rail":("carts:brakerail",0,0),
    "air":("air",15,0),
    "peony":("flowers:viola",15,0),
    "lilac":("flowers:viola",15,0),
    "allium":("flowers:viola",15,0),
    "andesite":("default:stone",0,0),
    "andesite_wall":("walls:cobble",15,0),
    "apple":("default:apple",15,0),
    "azure_bluet":("flowers:dandelion_white",15,0),
    "beacon":("default:obsidian_glass",0,0),
    "bedrock":("default:obsidian",0,0),
    "birch_fence":("default:fence_aspen_wood",0,0),
    "birch_fence_gate":("doors:gate_aspen_wood_closed",0,2),
    "birch_leaves":("default:aspen_leaves",0,0),
    "birch_log":("default:aspen_tree",0,0),
    "birch_planks":("default:aspen_wood",0,0),
    "birch_sapling":("default:aspen_sapling",15,0),
    "birch_slab":("stairs:slab_aspen_wood",0,0),
    "birch_stairs":("stairs:stair_aspen_wood",0,1),
    "black_concrete":("wool:black",0,0),
    "black_terracotta":("wool:black",0,0),
    "black_glazed_terracotta":("wool:black",0,0),
    "black_wool":("wool:black",0,0),
    "blue_concrete":("wool:blue",0,0),
    "blue_ice":("default:ice",0,0),   
    "blue_orchid":("flowers:geranium",15,0),
    "blue_terracotta":("wool:blue",0,0),
    "blue_glazed_terracotta":("wool:blue",0,0),
    "blue_wool":("wool:blue",0,0),
    "bookshelf":("default:bookshelf",0,0),
    "brain_coral_block":("default:coral_pink",0,0),
    "brick_slab":("stairs:slab_brick",0,0),
    "brick_stairs":("stairs:stair_brick",0,1),
    "brick_wall":("walls:desertcobble",15,0),
    "bricks":("default:brick",0,0),
    "brown_concrete":("wool:brown",0,0),
    "brown_mushroom":("flowers:mushroom_brown",15,0),
    "brown_terracotta":("wool:brown",0,0),
    "brown_glazed_terracotta":("wool:brown",0,0),
    "brown_wool":("wool:brown",0,0),
    "bubble_coral_block":("default:coral_brown",0,0),
    "cactus":("default:cactus",0,0),
    "cave_air":("air",15,0),
    "chest":("default:chest",15,facing2facedir),
    "trapped_chest":("default:chest",15,facing2facedir),
    "chinseled_red_sandstone":("default:desert_stone_block",0,0),
    "chiseled_red_sandstone":("default:desert_stone",0,0),
    "chiseled_sandstone":("default:sandstone_block",0,0),
    "clay":("default:clay",0,0),
    "coal_block":("default:coalblock",0,0),
    "coal_ore":("default:stone_with_coal",0,0),
    "cobblestone":("default:cobble",0,0),
    "cobblestone_slab":("stairs:slab_cobble",0,0),
    "cobblestone_stairs":("stairs:stair_cobble",0,1),
    "cobblestone_wall":("walls:cobble",15,0),
    "copper_ore":("default:stone_with_copper",0,0),
    "cornflower":("farming:wheat_8",0,0),
    "cracked_stone_bricks":("default:stonebrick",0,0),
    "cut_red_sandstone":("default:desert_stone_block",0,0),
    "cut_sandstone":("default:sandstone_block",0,0),
    "cyan_concrete":("wool:cyan",0,0),
    "cyan_terracotta":("wool:cyan",0,0),
    "cyan_glazed_terracotta":("wool:cyan",0,0),    
    "cyan_wool":("wool:cyan",0,0),
    "dandelion":("flowers:dandelion_yellow",15,0),
    "dark_concrete":("wool:dark_grey",0,0),
    "dark_oak_fence":("default:fence_wood",0,0),
    "dark_oak_fence_gate":("doors:gate_wood_closed",0,2),
    "dark_oak_leaves":("default:leaves",15,0),
    "dark_oak_log":("default:tree",0,0),
    "dark_oak_planks":("default:wood",0,0),
    "dark_oak_sapling":("default:sapling",0,0),
    "dark_oak_slab":("stairs:slab_wood",0,0),
    "dark_oak_stairs":("stairs:stair_wood",0,1),
    "dark_sapling":("default:sapling",0,0),
    "dark_terracotta":("wool:dark_grey",0,0),
    "dark_glazed_terracotta":("wool:dark_grey",0,0),    
    "dark_wool":("wool:dark_grey",0,0),
    "dead_brain_coral_block":("default:coral_skeleton",0,0),
    "dead_bubble_coral_block":("default:coral_skeleton",0,0),
    "dead_bush":("default:dry_shrub",0,0),
    "dead_fire_coral_block":("default:coral_skeleton",0,0),
    "dead_horn_coral_block":("default:coral_skeleton",0,0),
    "dead_tube_coral_block":("default:coral_skeleton",0,0),
    "detector_rail":("carts:rail",0,0),
    "diamond_block":("default:diamondblock",0,0),
    "diamond_ore":("default:stone_with_diamond",0,0),
    "diorite":("default:silver_sandstone",0,0),
    "dirt":("default:dirt",0,0),
    "emerald_ore":("default:stone",0,0),
    "end_stone":("default:copperblock",0,0),
    "end_stone_bricks":("default:copperblock",0,0),
    "farmland":("farming:soil",0,0),
    "fern":("default:fern_2",15,0),
    "fire":("fire:basic_flame",0,0),
    "fire_coral_block":("default:coral_orange",0,0),
    "glass":("default:glass",15,0),
    "glass_pane":("xpanes:pane_flat",15,cardinal2facedir),
    "gold_block":("default:goldblock",0,0),
    "gold_ore":("default:stone_with_gold",0,0),
    "granite":("default:stone",0,0),
    "grass":("default:grass_3",15,0),
    "grass_block":("default:dirt_with_grass",0,0),
    "grass_path":("default:dirt_with_grass_footsteps",0,0),
    "gravel":("default:gravel",0,0),
    "slime_block":("wool:green",0,0),
    "green_concrete":("wool:green",0,0),
    "green_terracotta":("wool:green",0,0),
    "green_glazed_terracotta":("wool:green",0,0),    
    "green_wool":("wool:green",0,0),
    "grey_concrete":("wool:grey",0,0),
    "grey_terracotta":("wool:grey",0,0),
    "grey_glazed_terracotta":("wool:grey",0,0),    
    "grey_wool":("wool:grey",0,0),
    "hay_block":("farming:straw",0,0),
    "tall_seagrass":("default:coral_green",0,0),
    "horn_coral_block":("default:coral_green",0,0),
    "ice":("default:ice",0,0),
    "infested_chiseled_stone_bricks":("default:cobble",0,0),
    "infested_cobblestone":("default:cobble",0,0),
    "infested_cracked_stone_bricks":("default:cobble",0,0),
    "infested_mossy_stone_bricks":("default:mossycobble",0,0),
    "infested_stone":("default:mossycobble",0,0),
    "infested_stone_bricks":("default:mossycobble",0,0),
    "iron_bars":("xpanes:bar",15,cardinal2facedir),
    "iron_block":("default:steelblock",0,0),
    "iron_ore":("default:stone_with_iron",0,0),
    "iron_trapdoor":("doors:trapdoor_steel",0,2),
    "jungle_fence":("default:fence_junglewood",0,0),
    "jungle_fence_gate":("doors:gate_junglewood_closed",0,2),
    "jungle_leaves":("default:jungleleaves",15,0),
    "jungle_log":("default:jungletree",0,0),
    "jungle_planks":("default:junglewood",0,0),
    "jungle_sapling":("default:junglesapling",15,0),
    "jungle_slab":("stairs:slab_junglewood",0,0),
    "jungle_stairs":("stairs:stair_junglewood",0,1),
    "lapis_block":("default:diamondblock",0,0),
    "lapis_ore":("default:stone_with_diamond",0,0),
    "large_fern":("default:fern_3",15,0),
    "lava":("default:lava_source",255,level2flowingliquid),
    'light_blue_terracotta':("wool:blue",0,0),
    'light_blue_glazed_terracotta':("wool:blue",0,0),    
    "light_blue_wool":("wool:blue",0,0),
    "light_gray_wool":("wool:grey",0,0),
    "lily_of_the_valley":("flowers:dandelion_white",15,0),
    "lily_pad":("flowers:waterlily",0,0),
    "lime_wool":("wool:green",0,0), 
    "magenta_concrete":("wool:magenta",0,0),
    "magenta_terracotta":("wool:magenta",0,0),
    "magenta_glazed_terracotta":("wool:magenta",0,0),    
    "magenta_wool":("wool:magenta",0,0),
    "gray_wool":("wool:dark_grey",0,0),
    "melon":("default:apple",0,0),
    "mossy_cobblestone":("default:mossycobble",0,0),
    "mossy_cobblestone_wall":("walls:mossycobble",0,0),
    "mossy_stone_bricks":("default:mossycobble",0,0),
    "mycelium":("default:dirt_with_grass",0,0),
    "nether_brick_fence":("default:fence_wood",0,0),
    "nether_brick_slab":("stairs:slab_stonebrick",0,0),
    "oak_door":("doors:door_wood_b_1",0,2),
    "oak_fence":("default:fence_wood",0,0),
    "oak_fence_gate":("doors:gate_wood_closed",0,2),
    "oak_leaves":("default:leaves",15,0),
    "oak_log":("default:tree",0,0),
    "oak_planks":("default:wood",0,0),
    "oak_slab":("stairs:slab_wood",0,0),
    "oak_stairs":("stairs:stair_wood",0,1),
    "oak_sapling":("default:sapling",0,0),
    "oak_trapdoor":("doors:trapdoor",0,2),
    "obsidian":("default:obsidian",0,0),
    "orange_concrete":("wool:orange",0,0),
    "orange_terracotta":("wool:orange",0,0),
    "orange_glazed_terracotta":("wool:orange",0,0),    
    "orange_tulip":("flowers:tulip",15,0),
    "orange_wool":("wool:orange",0,0),
    "oxeye_daisy":("flowers:dandelion_white",15,0),
    "packed_ice":("default:ice",0,0),
    "pink_concrete":("wool:pink",0,0),
    "pink_terracotta":("wool:pink",0,0),
    "pink_glazed_terracotta":("wool:pink",0,0),    
    "pink_tulip":("flowers:tulip",15,0),
    "pink_wool":("wool:pink",0,0),
    "podzol":("farming:soil",0,0),
    "polished_andesite":("default:stone_block",0,0),
    "polished_diorite":("default:silver_sandstone_block",0,0),
    "rose_bush":("flowers:rose",15,0),
    "poppy":("flowers:rose",15,0),
    "powered_rail":("carts:powerrail",0,0),
    "pumpkin":("default:apple",15,0),
    "purpur_block":("wool:violet",0,0),
    "purpur_pillar":("wool:violet",0,0),
    "purple_concrete":("wool:violet",0,0),
    "purple_terracotta":("wool:violet",0,0),
    "purple_glazed_terracotta":("wool:violet",0,0),    
    "purple_wool":("wool:violet",0,0),
    "quartz_slab":("stairs:slab_stonebrick",0,0),
    "quartz_stairs":("stairs:stair_quartzblock",0,1),
    "rail":("carts:rail",15,0),
    "magma_block":("wool:red",0,0),
    "red_concrete":("wool:red",0,0),
    "red_mushroom":("flowers:mushroom_red",15,0),
    "red_sand":("default:desert_sand",0,0),
    "red_sandstone":("default:desert_stone",0,0),
    "red_sandstone_slab":("stairs:slab_desert_stone",0,0),
    "red_sandstone_stairs":("stairs:stair_desert_stone",0,1),
    "red_sandstone_wall":("walls:desertcobble",15,0),
    "red_terracotta":("wool:red",0,0),
    "red_glazed_terracotta":("wool:red",0,0),    
    "red_tulip":("flowers:rose",0,0),
    "red_tulip":("flowers:tulip_black",15,0),
    "red_wool":("wool:red",0,0),
    "redstone_block":("default:mese",0,0),
    "redstone_ore":("default:stone_with_mese",0,0),
    "sand":("default:sand",0,0),
    "sandstone":("default:sandstone",0,0),
    "sandstone_slab":("stairs:slab_sandstone",0,0),
    "sandstone_stairs":("stairs:stair_sandstone",0,1),
    "sign":("default:sign_wall_wood",15,facing2wallmounted),
    "smooth_red_sandstone":("default:desert_stone_block",0,0),
    "smooth_sandstone":("default:sandstone_block",0,0),
    "smooth_stone":("default:stone_block",0,0),
    "snow":("default:snow",0,0),
    "snow_block":("default:snowblock",0,0),
    "soul_sand":("nether:sand",0,0),
    "sponge":("default:nyancat_rainbow",0,0),
    "spruce_fence":("default:fence_pine_wood",0,0),
    "spruce_fence_gate":("doors:gate_pine_wood_closed",0,2),
    "spruce_leaves":("default:pine_needles",15,0),
    "spruce_log":("default:pine_tree",0,0),
    "spruce_planks":("default:pine_wood",0,0),
    "spruce_sapling":("default:pine_sapling",15,0),
    "spruce_slab":("stairs:slab_pine_wood",0,0),
    "spruce_stairs":("stairs:stair_pine_wood",0,1),
    "spruce_wall_sign":("default:sign_wall_wood",15,facing2wallmounted),
    "stone":("default:stone",0,0),
    "stone_brick_slab":("stairs:slab_stonebrick",0,0),
    "stone_brick_stairs":("stairs:stair_stonebrick",0,1),
    "stone_brick_wall":("walls:cobble",15,0),
    "stone_bricks":("default:stonebrick",0,0),
    "stone_slab":("stairs:slab_wood",0,0),
    "sugar_cane":("default:papyrus",15,0),
    "sunflower":("flowers:rose",15,0),
    "tall_grass":("default:junglegrass",15,0),
    "tin_ore":("default:stone_with_tin",0,0),
    "tnt":("tnt:tnt",0,0),
    "redstone_torch":("default:torch",255,1),
    "torch":("default:torch",255,1),
    "tube_coral_block":("default:coral_cyan",0,0),
    "wall_torch":("default:torch_wall",255,facing2wallmounted),
    "bubble_column":("default:water_source",15,7),
    "water":("default:water_source",15,level2flowingliquid),
    "white_concrete":("wool:white",0,0),
    "white_stained_glass_pane":("xpanes:pane",0,0),
    "white_terracotta":("wool:white",0,0),
    "white_glazed_terracotta":("wool:white",0,0),
    "white_tulip":("flowers:dandelion_white",15,0),
    "white_wool":("wool:white",0,0),
    "yellow_concrete":("wool:yellow",0,0),
    "yellow_terracotta":("wool:yellow",0,0),
    "yellow_glazed_terracotta":("wool:yellow",0,0),
    "yellow_wool":("wool:yellow",0,0),
    "":("ignore",15,0),
    "end_rod":("default:mese_post_light",0,0),
    "furnace":("default:furnace",0,facing2facedir),
    "blast_furnace":("default:furnace",0,facing2facedir),
    "ladder":("default:ladder_wood",0,facing2wallmounted),
    "sea_lantern":("default:obsidian_glass",15,0),
    "bone_block":("bones:bones",0,0),
}

door_table = {

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
    "oak_trapdoor_a":("doors:trapdoor",15,facing2facedir),
    "oak_trapdoor_b":("doors:trapdoor_open",15,facing2facedir),
    "iron_trapdoor_a":("doors:trapdoor_steel",15,facing2facedir),
    "iron_trapdoor_b":("doors:trapdoor_steel_open",15,facing2facedir),
}

hardenedclay_table = {
    "blue_terracotta":("hardenedclay:hardened_clay_blue",0,0),
    "black_terracotta":("hardenedclay:hardened_clay_black",0,0),
    "brown_terracotta":("hardenedclay:hardened_clay_brown",0,0),
    "cyan_terracotta":("hardenedclay:hardened_clay_cyan",0,0),
    "gray_terracotta":("hardenedclay:hardened_clay_gray",0,0),
    "green_terracotta":("hardenedclay:hardened_clay_green",0,0),
    "light_blue_terracotta":("hardenedclay:hardened_clay_light_blue",0,0),
    "light_gray_terracotta":("hardenedclay:hardened_clay_light_gray",0,0),
    "magenta_terracotta":("hardenedclay:hardened_clay_magenta",0,0),
    "lime_terracotta":("hardenedclay:hardened_clay_lime",0,0),
    "orange_terracotta":("hardenedclay:hardened_clay_orange",0,0),
    "pink_terracotta":("hardenedclay:hardened_clay_pink",0,0),
    "purple_terracotta":("hardenedclay:hardened_clay_purple",0,0),
    "red_terracotta":("hardenedclay:hardened_clay_red",0,0),
    "yellow_terracotta":("hardenedclay:hardened_clay_yellow",0,0),
    "white_terracotta":("hardenedclay:hardened_clay_white",0,0),
    "blue_glazed_terracotta":("hardenedclay:hardened_clay_blue",0,0),
    "black_glazed_terracotta":("hardenedclay:hardened_clay_black",0,0),
    "brown_glazed_terracotta":("hardenedclay:hardened_clay_brown",0,0),
    "cyan_glazed_terracotta":("hardenedclay:hardened_clay_cyan",0,0),
    "gray_glazed_terracotta":("hardenedclay:hardened_clay_gray",0,0),
    "green_glazed_terracotta":("hardenedclay:hardened_clay_green",0,0),
    "light_glazed_blue_terracotta":("hardenedclay:hardened_clay_light_blue",0,0),
    "light_glazed_gray_terracotta":("hardenedclay:hardened_clay_light_gray",0,0),
    "magenta_glazed_terracotta":("hardenedclay:hardened_clay_magenta",0,0),
    "lime_glazed_terracotta":("hardenedclay:hardened_clay_lime",0,0),
    "orange_glazed_terracotta":("hardenedclay:hardened_clay_orange",0,0),
    "pink_glazed_terracotta":("hardenedclay:hardened_clay_pink",0,0),
    "purple_glazed_terracotta":("hardenedclay:hardened_clay_purple",0,0),
    "red_glazed_terracotta":("hardenedclay:hardened_clay_red",0,0),
    "yellow_glazed_terracotta":("hardenedclay:hardened_clay_yellow",0,0),
    "white_glazed_terracotta":("hardenedclay:hardened_clay_white",0,0),
}

quartz_table = {
    "nether_quartz_ore":("quartz:quartz_ore",0,0),
    "quartz_block" : ("quartz:block",0,0),
    "smooth_quartz" : ("quartz:block",0,0),
    "chiseled_quartz_block" :("quartz:chiseled",0,0),
    "quartz_pillar" : ("quartz:pillar",0,0),
    "quartz_slab" : ("stairs:slab_quartzstair",15,type2facedir),
    "quartz_stairs" : ("stairs:stair_quartzstair",15,stair2facedir),
    "smooth_quartz_stairs" : ("stairs:stair_quartzblock",15,stair2facedir),
    "smooth_quartz_slab" : ("stairs:slab_quartzblock",15,type2facedir),
}

nether_table = {
    "nether_brick_slab" : ("stairs:slab_nether_brick",15,type2facedir),
    "netherrack" : ("nether:rack",0,0),
    "nether_bricks" : ("nether:brick",0,0),
    "nether_brick_fence" : ("nether:fence_nether_brick",0,0),
    "nether_brick_stairs" : ("stairs:stair_nether_brick",0,stair2facedir),
    "glowstone":("nether:glowstone",0,0),
    "nether_quartz_ore" : ("nether:glowstone",0,0),
    "nether_wart_block" : ("nether:sand",0,0),
    "red_nether_bricks" : ("nether:rack_cube",0,0),
    "nether_brick" : ("nether:brick_cube",0,0),
    "nether_portal" : ("nether:portal",15,12),
    "end_portal" : ("nether:portal",15,12),
    "nether_brick_wall" : ("brick_panel",0,0),
    "red_nether_brick_wall" : ("rack_panel",0,0),
    "red_nether_brick_stairs" : ("stairs:stair_nether_brick",0,stair2facedir),
    "red_nether_brick_slab" : ("stairs:slab_nether_brick",15,type2facedir),
}

mesecons_table = {
    "stone_button":("mesecons_button:button_off",0,8),
    "command_block":("mesecons_commandblock:commandblock_off",0,0),
    "daylight_detector":("mesecons_solarpanel:solar_panel_off",0,1),
    "lever":("mesecons_walllever:wall_lever_off",0,15),
    "note_block":("mesecons_noteblock:noteblock",0,0),
    "oak_button":("mesecons_button:button_off",0,8),
    "oak_pressure_plate":("mesecons_pressureplates:pressure_plate_wood_off",0,0),
    "spruce_button":("mesecons_button:button_off",0,8),
    "spruce_pressure_plate":("mesecons_pressureplates:pressure_plate_wood_off",0,0),
    "birch_button":("mesecons_button:button_off",0,8),
    "birch_pressure_plate":("mesecons_pressureplates:pressure_plate_wood_off",0,0),
    "jungle_button":("mesecons_button:button_off",0,8),
    "jungle_pressure_plate":("mesecons_pressureplates:pressure_plate_wood_off",0,0),
    "acacia_button":("mesecons_button:button_off",0,8),
    "acacia_pressure_plate":("mesecons_pressureplates:pressure_plate_wood_off",0,0),
    "dark_button":("mesecons_button:button_off",0,8),
    "dark_pressure_plate":("mesecons_pressureplates:pressure_plate_wood_off",0,0),
    "piston":("mesecons_pistons:piston_normal_off",0,8),
    "piston_head":("mesecons_pistons:piston_pusher_normal",0,8),
    "redstone_lamp":("mesecons_lightstone:lightstone_gray_off",0,0),
    "redstone_wire":("mesecons:wire_11111111_off",0,0),
    "repeater":("mesecons:wire_11111111_off",0,0),  
    "sticky_piston":("mesecons_pistons:piston_sticky_off",0,8),
    "stone_pressure_plate":("mesecons_pressureplates:pressure_plate_stone_off",0,0),
    "light_weighted_pressure_plate":("mesecons_pressureplates:pressure_plate_stone_off",0,0),
    "heavy_weighted_pressure_plate":("mesecons_pressureplates:pressure_plate_stone_off",0,0),
    "comparator" :  ("mesecons_fpga:fpga0000",0,0),
    "emerald_block":("default:diamondblock",0,0),
}

carpet_table = {
    "lime_carpet":("carpet:wool_green",0,0),
    "light_gray_carpet":("carpet:wool_grey",0,0),
    "green_carpet":("carpet:wool_dark_green",0,0),
    "black_carpet":("carpet:wool_black",0,0),
    "brown_carpet":("carpet:wool_brown",0,0),
    "light_blue_carpet":("carpet:wool_blue",0,0),
    "magenta_carpet":("carpet:wool_magenta",0,0),
    "pink_carpet":("carpet:wool_pink",0,0),
    "cyan_carpet":("carpet:wool_cyan",0,0),
    "gray_carpet":("carpet:wool_dark_grey",0,0),
    "purple_carpet":("carpet:wool_violet",0,0),
    "yellow_carpet":("carpet:wool_yellow",0,0),
    "orange_carpet":("carpet:wool_orange",0,0),
    "blue_carpet":("carpet:wool_blue",0,0),
    "red_carpet":("carpet:wool_red",0,0),
    "white_carpet":("carpet:wool_white",0,0),
    "lime_wall_banner":("carpet:wool_green",0,0),
    "light_gray_wall_banner":("carpet:wool_grey",0,0),
    "green_wall_banner":("carpet:wool_dark_green",0,0),
    "black_wall_banner":("carpet:wool_black",0,0),
    "brown_wall_banner":("carpet:wool_brown",0,0),
    "light_blue_wall_banner":("carpet:wool_blue",0,0),
    "magenta_wall_banner":("carpet:wool_magenta",0,0),
    "pink_wall_banner":("carpet:wool_pink",0,0),
    "cyan_wall_banner":("carpet:wool_cyan",0,0),
    "gray_wall_banner":("carpet:wool_dark_grey",0,0),
    "purple_wall_banner":("carpet:wool_violet",0,0),
    "yellow_wall_banner":("carpet:wool_yellow",0,0),
    "orange_wall_banner":("carpet:wool_orange",0,0),
    "blue_wall_banner":("carpet:wool_blue",0,0),
    "red_wall_banner":("carpet:wool_red",0,0),
    "white_wall_banner":("carpet:wool_white",0,0),
}

xdecor_table = {
    "bell_hook":("xdecor:lantern",0,0),
    "tripwire_hook":("xdecor:lever_off",0,0),
    "cobweb":("xdecor:cobweb",0,0),
    "crafting_table":("xdecor:workbench",0,0),
    "enchanting_table":("xdecor:enchantment_table",0,0),
    "polished_andesite":("xdecor:stone_tile",0,0),
    "polished_diorite":("xdecor:hard_clay",0,0),
    "polished_granite":("xdecor:desertstone_tile",0,0),
    "bee_nest" : ("xdecor:hive",0,0),
    "brewing_stand" : ("xdecor:baricade",15,0),
    "campfire" : ("xdecor:lantern",15,0),
    "cartography_table" : ("xdecor:enchantment_table",0,0),
    "cauldron" : ("xdecor:cauldron_idle",0,0),
    "composter" : ("xdecor:barrel",0,0),
    "dispenser" : ("xdecor:enderchest",0,0),
    "enchanting_table" : ("xdecor:enchantment_table",0,0),
    "end_portal_frame" : ("xdecor:enchantment_table",0,0),
    "fletching_table" : ("xdecor:mailbox",0,0),
    "grindstone" : ("xdecor:stone_rune",0,0),
    "hopper" : ("xdecor:cauldron_idle",0,0),
    "lantern" : ("xdecor:lantern",15,0),
    "lectern" : ("xdecor:table",15,0),
    "loom" : ("xdecor:workbench",0,0),
    "potted_acacia_sapling" : ("xdecor:potted_tulip",0,0),
    "potted_allium" : ("xdecor:potted_viola",0,0),
    "potted_azure_bluet" : ("xdecor:potted_dandelion_white",0,0),
    "potted_lily_of_the_valley" : ("xdecor:potted_dandelion_white",0,0),
    "potted_birch_sapling" : ("xdecor:potted_tulip",0,0),
    "potted_blue_orchid" : ("xdecor:potted_geranium",0,0),
    "potted_brown_mushroom" : ("xdecor:potted_viola",0,0),
    "potted_cactus" : ("xdecor:potted_dandelion_yellow",0,0),
    "potted_dandelion" : ("xdecor:potted_dandelion_yellow",0,0),
    "potted_dark_oak_sapling" : ("xdecor:potted_geranium",0,0),
    "potted_dead_bush" : ("xdecor:potted_viola",0,0),
    "potted_fern" : ("xdecor:potted_geranium",0,0),
    "potted_jungle_sapling" : ("xdecor:potted_viola",0,0),
    "potted_oak_sapling" : ("xdecor:potted_dandelion_yellow",0,0),
    "potted_orange_tulip" : ("xdecor:potted_tulip",0,0),
    "potted_oxeye_daisy" : ("xdecor:potted_dandelion_white",0,0),
    "potted_pink_tulip" :  ("xdecor:potted_tulip",0,0),
    "potted_poppy" : ("xdecor:potted_rose",0,0),
    "potted_red_mushroom" : ("xdecor:potted_rose",0,0),
    "potted_red_tulip" : ("xdecor:potted_rose",0,0),
    "potted_spruce_sapling" : ("xdecor:potted_rose",0,0),
    "potted_wither_rose" : ("xdecor:potted_rose",0,0),
    "potted_white_tulip" : ("xdecor:potted_dandelion_white",0,0),
    "redstone_wall_torch" : ("xdecor:candle",15,facing2wallmounted),
    "scaffolding" : ("xdecor:table",15,0),
    "smithing_table" : ("xdecor:multishelf",0,0),
    "stonecutter" : ("xdecor:workbench",0,0),
    "vine" : ("xdecor:ivy",15,0),
    "crafting_table" :  ("xdecor:workbench",0,0),
    "anvil" :  ("xdecor:workbench",0,0),
    "chiseled_stone_bricks":("xdecor:stone_rune",0,0),
}

materials_table = {
    "oak" : "wood",
    "spruce" : "pine_wood",
    "birch" : "aspen_wood",
    "jungle" : "junglewood",
    "acacia" : "acacia_wood",
    "dark_oak" : "wood",
    "stone" : "stone",
    "sandstone" : "sandstone",
    "petrified_oak" : "wood",
    "cobblestone" : "cobble",
    "brick" : "brick",
    "stone_brick" : "stonebrick",
    "nether_brick" : "desert_stonebrick",
    "quartz" : "snowblock",
    "red_sandstone" : "desert_stone",
    "purpur" : "goldblock",
    "prismarine" : "ice",
    "prismarine_brick" : "ice",
    "dark_prismarine" : "ice",
    "smooth_stone" : "stone_block",
    "cut_sandstone" : "sandstone_block",
    "cut_red_sandstone" : "desert_stone_block",
    "polished_granite" : "desert_stone_block",
    "smooth_red_sandstone" : "desert_stone_block",
    "mossy_stone_brick" : "mossycobble",
    "polished_diorite" : "silver_sandstone", 
    "mossy_cobblestone" : "mossycobble",
    "end_stone_brick" : "sandstonebrick",
    "smooth_sandstone" : "sandstone_block",
    "smooth_quartz" : "steel",
    "granite" : "desert_cobble",
    "andesite" : "stone",
    "red_nether_brick" : "desert_stonebrick",
    "polished_andesite" : "stone_block",
    "diorite" : "silver_sandstone",
}

guessing_table = {
    "_planks^" :("default:wood",0,0),
    "_log^" : ("default:tree",0,0),
    "_wood^" : ("default:tree",0,0),
    "_wall^" : ("walls:cobble",15,0),
    "_slab^" : ("stairs:slab_wood",15,0),
    "_wall_sign^" : ("default:sign_wall_wood",15,facing2wallmounted),
    #"_block^" : ("default:goldblock",0,0),
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
        try:
            param0,param1,param2 = convertBlock(block)
            if param0 != "air":
                print(f"Converted ({param0},{param1:02X},{param2:02X}) = {block}\t")
        except Exception as e:
             print("Conversion of block",block,"failed with",e)
             raise e
            


