import argparse
from . import block_conversion

description = """
Convert maps from Minecraft to Minetest.
"""
epilog = """
This script uses "anvil-parser" library from "matcool" to parse world folders.
More details at https://github.com/matcool/anvil-parser
"""

block_conversion.load_mods_from_path()

print()
print("#####################################################")
print("# mc2mt - Minecraft to Minetest map conversion tool #")
print("#####################################################")
print()

parser = argparse.ArgumentParser(description=description,epilog=epilog)

parser.add_argument('input',
                    help='Minecraft input world folder')
parser.add_argument('output',
                    help='Output folder for the generated world.')
parser.add_argument('--mod','-m',action='append',
                    help='Load mod from json file')
parser.add_argument('--disable_all_mods','-d',action='store_true',
                    help='Disable all mods')
parser.add_argument('--enable_all_mods','-e',action='store_true',
                    help='Enable all mods')
parser.add_argument('--unknown_as_air','-u',action='store_true',
                    help='Unknown blocks will be converted to air')
parser.add_argument('--quiet','-q',action='store_true',
                    help='Do not report unknown blocks')

for mod in block_conversion.mods_enabled:
    parser.add_argument(f'--disable_{mod}',action='store_true',
                        help=f'Disable mod {mod}')
    parser.add_argument(f'--enable_{mod}',action='store_true',
                        help=f'Enable mod {mod}')
