from mc2mtlib import block_conversion
from anvil.block import Block

print("Reading unknown blocks from stdin and testing conversion")
lines = []
converted = []

while not lines or lines[-1]:
    try: lines.append(input())
    except EOFError: break

for line in lines:
    if line[:12] != "UnknownBlock": continue
    unknown,name,properties = line.split("~")
    block = Block("minecraft",name,eval(properties))
    param0,param1,param2 = convert_block(block)
    print(f"({param0},{param1:02X},{param2:02X}) = {block}")
