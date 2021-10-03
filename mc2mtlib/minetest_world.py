import os
import sqlite3

from . import blob_writer

# Copied from world_format.txt
def getBlockAsInteger(p):
    return int64(p[2]*16777216 + p[1]*4096 + p[0])

def int64(u):
    while u >= 2**63:
        u -= 2**64
    while u <= -2**63:
        u += 2**64
    return u


class MinetestWorld:
    path = None
    connection = None
    saved_map_block = 0
    biggest_map_block = {"pos":(0,0,0),"size":0}

    def __init__(self,path,gameid):
        self.path = path
        self.gameid = gameid
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        #World mt
        with open(os.path.join(path,"world.mt"),'w') as world_mt:
            world_mt.write("\n".join([
                "enable_damage = false",
                "creative_mode = true",
                "gameid = " + self.gameid,
                "backend = sqlite3",
                "auth_backend = sqlite3",
                "player_backend = sqlite3",
            ]))

        #Database
        self.connection = sqlite3.connect(os.path.join(path,"map.sqlite"))
        self.connection.execute(" ".join([
            "CREATE TABLE IF NOT EXISTS `blocks`(",
            "        `pos` INT NOT NULL PRIMARY KEY,",
            "        `data` BLOB",
            ");",
        ]))
        self.connection.commit()

    def insert(self,converted_section):
        key = getBlockAsInteger(converted_section['pos'])
        blob = blob_writer.write_blob(converted_section)
        query = "INSERT OR REPLACE INTO blocks VALUES (?,?)"
        self.connection.execute(query,(key,blob))
        if len(blob) > self.biggest_map_block["size"]:
            self.biggest_map_block = {
                "pos":converted_section['pos'],
                "size":len(blob)
            }
        self.saved_map_block += 1

    def save(self):
        modpath = os.path.join(self.path,"worldmods","mc2mt")
        luapath = os.path.join(self.path,"worldmods","mc2mt","init.lua")
        try: os.makedirs(modpath)
        except: pass
        x,y,z = [str(8+i*16) for i in self.biggest_map_block["pos"]]
        with open(luapath,'w') as init_lua:
            init_lua.write("\n".join([
                "minetest.set_mapgen_params({water_level = -2})",
                "minetest.set_mapgen_params({chunksize = 1})",
                "minetest.set_mapgen_params({mgname = \"singlenode\"})",
                "minetest.register_on_generated(function(minp, maxp, seed)",
                "    local vm = minetest.get_voxel_manip(minp, maxp)",
                "    vm:calc_lighting()",
                "    vm:update_liquids()",
                "    vm:write_to_map()",
                "end)",
                "minetest.register_on_newplayer(function(player)",
                "    player:set_pos({",
                "        x="+x+",",
                "        y="+y+",",
                "        z="+z+",",
                "    })",
                "    minetest.set_player_privs(",
                "        player:get_player_name(),",
                "        {fly=true,noclip=true}",
                "    )"
                "end)",
            ]))
        self.connection.commit()
        self.connection.close()
