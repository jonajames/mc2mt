import os,json
from .block_functions import * 

report_known_blocks = False
report_unknown_blocks = True
unknown_as_air = False
converted_blocks = {}
mods_priority = []
mods_enabled = {}
mods_table = {}

def load_mod(mod_file):
    with open(mod_file) as json_file:
        try:
            mod = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            print("Error in mod:",mod_file)
            print(e)
            exit(1)
    name = mod.get("name","unknown")
    author = mod.get("author","anonymous")
    description = mod.get("description","No description provided.")
    download = mod.get("download","No download provided.")
    enabled = mod.get("enabled",True)
    priority = mod.get("priority",0)
    print("Loading mod [",name,"] by",author)
    print("\t",description)
    print("\t",download)
    mods_table[name] = mod["table"]
    mods_enabled[name] = enabled
    mods_priority.append((priority,name))
    mods_priority.sort()
    
def load_mods_from_path():
    mod_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"mods")
    for mod_filename in os.listdir(mod_path):
        load_mod(os.path.join(mod_path,mod_filename))

def find_in_table(table,key):
    if key in table: return key
    parts = key.split("_")
    for i in range(1,len(parts)):
        key_part = ("_".join(parts[:i]))+"?"
        if key_part in table: return key_part
    for i in range(1,len(parts)):
        key_part = "?"+("_".join(parts[i:]))
        if key_part in table: return key_part
        
def get_from_table(table,block):
    key = find_in_table(table,block.id)
    if not key: return
    param0,param1,param2 = table[key]
    try:
        if type(param0)==str and param0[0]=="@":
            param0 = (globals()[param0[1:]])(block)
        if type(param1)==str and param1[0]=="@":
            param1 = (globals()[param1[1:]])(block)
        if type(param2)==str and param2[0]=="@":
            param2 = (globals()[param2[1:]])(block)
    except Exception as e:
        print_block("ERROR",block)
        raise e
    return param0,param1,param2
        
def convert_block(block):
    # Get conversion from cache
    if block.id == "air": return ("air",0,0)
    if block in converted_blocks:
        return converted_blocks[block]

    # Get conversion from mod
    for priority,mod_name in mods_priority:
        if not mods_enabled[mod_name]: continue
        mod_table = mods_table[mod_name]
        converted = get_from_table(mod_table,block)
        if converted:
            converted_blocks[block] = converted
            if report_known_blocks: print_block("ConvertedBlock",block)
            return converted
        
    # Unknown block
    if unknown_as_air: converted = ("air",15,0)
    else: converted = (f"mc2mt:{block.id}",0,0)
    converted_blocks[block] = converted
    if report_unknown_blocks: print_block("UnknownBlock",block)
    return converted

def print_block(prefix,block):
    properties = {}
    for p in block.properties:
        properties[p] = str(block.properties[p])
    print(f"{prefix}~{block.id}~{properties}")
            
