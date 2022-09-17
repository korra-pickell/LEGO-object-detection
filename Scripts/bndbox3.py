import bpy
import bpy_extras
import json
import os
from mathutils import Vector
from math import *

file = ''

def write_frame(scene):
    print("----Starting Render function----")
    #with open('collision.json', 'r') as f:
    #    datastore = json.load(f)
    power = bpy.data.objects['Cube']
    camera = bpy.data.objects['Camera']
    scn = bpy.data.scenes['Scene']
    box = power.bound_box
    bbox_corners = [power.matrix_world * Vector(corner) for corner in box]
    verts = [bpy_extras.object_utils.world_to_camera_view(scn,camera,Vector(vert)) for vert in bbox_corners]
    frame=[]
    for vert in verts:
        vert.x = vert.x * bpy.context.scene.render.resolution_x
        vert.y = vert.y * bpy.context.scene.render.resolution_y
        frame.append(vert.x)
        frame.append(vert.y)
    print(verts)
    print(frame)

    #framenum = len(datastore)
    #datastore[framenum]=frame

    #print
    #with open('collision.json', 'w') as f:
    ##    jsondat = json.dumps(datastore)
    #    f.write(jsondat)
    #print('-------dump to file---------')

def pre_render(scene):
    with open('collision.json', 'w') as f:
        f.write('{}') 

bpy.app.handlers.frame_change_post.append(write_frame)
bpy.app.handlers.render_pre.append(pre_render)