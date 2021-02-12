# mc2mt
Convert maps from Minecraft to Minetest

## Dependencies

Quarry library is used to decode nbt format 

`pip install quarry` 

https://github.com/barneygale/quarry

## Usage
```
usage: mc2mt.py [OPTIONS] input output

Convert maps from Minecraft to Minetest.

positional arguments:
  input                 Minecraft input world folder
  output                Output folder for the generated world.

optional arguments:
  -h, --help            show this help message and exit
  --disable_xdecor      Disable mod xdecor
  --enable_quartz       Enable mod quartz
  --enable_nether       Enable mod nether
  --enable_bedrock      Enable mod bedrock
  --disable_stained_glass
                        Disable mod stained_glass
  --disable_liquids     Disable mod liquids
  --disable_carpet      Disable mod carpet
  --disable_mesecons    Disable mod mesecons
  --enable_hardenedclay
                        Enable mod hardenedclay

This script uses quarry library from barneygale to read mca files. More details at https://quarry.readthedocs.io/en/latest
```

## Unknown Block

All unknown block will be replaced with air.

Mods can be enabled/disabled to convert those blocks.

The block conversion is made by [block_conversion.py](block_conversion.py).

Have a look at it and if you want to help improve it open an issue/pull request

## Known Bugs

+ Beds have no top part
+ Trapdoor rotation is not yet implemented
+ Some stairs are not rotated correctly
+ Water and lava behaves differently in MT and may cause spills

