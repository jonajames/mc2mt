import os,json
from .block_functions import *

report_known_blocks = False
report_unknown_blocks = True
unknown_as_air = False
converted_blocks = {}
mods_available = {}
mods_priority = []
mods_enabled = {}

def str_mod(name):
    author = mods_available[name]['author']
    download = mods_available[name]['download']
    description = mods_available[name]['description']
    return f"[ {name} ] by {author}\n\t{description}\n\t{download}"

def load_mod(mod_file):
    mod = {
        'name': 'unknown',
        'author': 'anonymous',
        'description': 'No description provided.',
        'download': 'No download provided.',
        'enabled': True,
        'priority': 0,
        'table': {},
    }
    with open(mod_file) as json_file:
        try:
            load = json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            print("Error in mod:",mod_file)
            print(e)
            exit(1)
    mod.update(load)
    mods_available[mod['name']] = mod
    mods_enabled[mod['name']] = mod['enabled']
    mods_priority.append((mod['priority'],mod['name']))
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
    if block.id == "air": return ("air",15,0)
    if str_block(block) in converted_blocks:
        return converted_blocks[str_block(block)]

    # Get conversion from mod
    for priority,mod_name in mods_priority:
        if not mods_enabled[mod_name]: continue
        mod_table = mods_available[mod_name]['table']
        converted = get_from_table(mod_table,block)
        if converted:
            converted_blocks[str_block(block)] = converted
            if report_known_blocks: print_block("ConvertedBlock",block)
            return converted

    # Unknown block
    if unknown_as_air: converted = ("air",15,0)
    else: converted = (f"mc2mt:{block.id}",0,0)
    converted_blocks[str_block(block)] = converted
    if report_unknown_blocks: print_block("UnknownBlock",block)
    return converted

def print_block(prefix,block):
    print(prefix,str_block(block),sep="~")

def str_block(block):
    string = str(block.id) + "~{"
    for p in sorted(block.properties.keys()):
        string += "'" + str(p) + "':'" + str(block.properties[p]) + "', "
    return string[:-2] + "}"
