import argparse
from . import block_conversion

block_conversion.load_mods_from_path()

description = """
Convert maps from Minecraft to Minetest.
"""
epilog = "# Available Mods" + "\n"
for mod in block_conversion.mods_enabled:
    epilog += block_conversion.str_mod(mod) + "\n"
epilog += """
# Notes
This script uses "anvil-parser" library from "matcool" to parse world folders.
More details at https://github.com/matcool/anvil-parser
"""

print()
print("#####################################################")
print("# mc2mt - Minecraft to Minetest map conversion tool #")
print("#####################################################")
print()

parser = argparse.ArgumentParser(
    description=description,
    epilog=epilog,
    formatter_class=argparse.RawDescriptionHelpFormatter
)

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
    if block_conversion.mods_enabled[mod]:
        parser.add_argument(f'--disable_{mod}',action='store_true',
                            help=f'Disable mod {mod}')
    else:
        parser.add_argument(f'--enable_{mod}',action='store_true',
                            help=f'Enable mod {mod}')
