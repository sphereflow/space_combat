import collision
import math_3d

col_hash = {}
collidable_group_ids = {}

def register_group_ids(id1, id2) :
   if not id1 in collidable_group_ids :
      collidable_group_ids[id1] = []
   collidable_group_ids[id1].append(id2)
   if not id1 in col_hash :
      col_hash[id1] = []   
   if not id2 in col_hash :
      col_hash[id2] = []   

def add(game_obj) :
   if not game_obj.COL_ID in col_hash :
      col_hash[game_obj.COL_ID] = []
   col_hash[game_obj.COL_ID].append(game_obj)
   game_obj.containers.append(col_hash[game_obj.COL_ID])

#def remove(game_obj) :
   #if not game_obj.COL_ID in col_hash :
      #return
   #if game_obj in col_hash[game_obj.COL_ID] :
#      col_hash[game_obj.COL_ID].remove(game_obj)

def update() :
   for id1 in collidable_group_ids :
      for id2 in collidable_group_ids[id1] :
         for go1 in col_hash[id1] :
            for go2 in col_hash[id2] :
               if go1.m.r.contains_vertex_of(go2.m.r) or go2.m.r.contains_vertex_of(go1.m.r) :
                  go1.collision_with(go2)
                  go2.collision_with(go1)
   # TODO : replace with Quadtree version
