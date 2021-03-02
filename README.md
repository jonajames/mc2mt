# mc2mtthe one 
Convert maps from Minecraft to Minetest

## Dependencies

Anvil-Parser library is used to decode nbt format 

`pip install anvil-parser` 

https://github.com/matcool/anvil-parser

## Usage
```
usage: mc2mt.py [OPTIONS] input output

Convert maps from Minecraft to Minetest.

positional arguments:
  input                 Minecraft input world folder
  output                Output folder for the generated world.

optional arguments:
  -h, --help            show this help message and exit
  -m MOD                Load mod from json file
  -d                    Disable all mods
  -e                    Enable all mods
  -u                    Unknown blocks will be converted to air
  -q                    Do not report unknown blocks
  --disable_MOD         Disable mod MOD
  --enable_MOD          Enable mod MOD

This script uses "anvil-parser" library from "matcool" to parse world folders. More details at https://github.com/matcool/anvil-parser
```

## Custom Blocks Definition
You can provide a JSON file like shown below to implement your custom definition
```json
{
    "table" : {
        "full_block_id" : ["minetest:itemstring",param1,param2],
        "beginning_of_id?": ["minetest:itemstring",param1,param2],,
        "?end_of_id" : ["minetest:itemstring",param1,param2],
    }
}
```

