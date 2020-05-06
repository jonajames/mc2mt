# mc2mt
Convert maps from Minecraft to Minetest

## Dependencies

Quarry library is used to decode nbt format 

`pip install quarry` 

https://github.com/barneygale/quarry

## Usage
```
usage: mc2mt.py [-h] input output

Convert maps from Minecraft to Minetest.

positional arguments:
  input       Minecraft input world folder
  output      Output folder for the generated world. Must not exist.

optional arguments:
  -h, --help  show this help message and exit

This script uses quarry library from barneygale to read mca files. More details at quarry.readthedocs.io
```

## Unknown Block

All unknown block will be replaced with air.

The block conversion is made by [block_conversion.py](block_conversion.py).

Have a look at it and if you want to improve it, please send me a pull request.

## Known Bugs

Block rotation is completely off. I have no idea why.

Quarry can sometime cause buffer underruns 
