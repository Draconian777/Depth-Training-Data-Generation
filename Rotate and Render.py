import bpy
import mathutils
from random import randint, uniform
from math import radians
import os

#check https://docs.blender.org/api/current/bpy.types.RenderSettings.html


'''
def rotate_and_render(output_dir, output_file_pattern_string = 'render%d.jpg', rotation_steps = 32, rotation_angle = 360.0, subject = bpy.context.object):
  
  original_rotation = subject.rotation_euler
  for step in range(0, rotation_steps):
    subject.rotation_euler[2] = radians(step * (rotation_angle / rotation_steps))
    bpy.context.scene.render.filepath = os.path.join(output_dir, (output_file_pattern_string % step))
    bpy.ops.render.render(write_still = True)
  subject.rotation_euler = original_rotation

rotate_and_render('/Users/myusername/Pictures/VR', 'render%d.jpg')


#Alternatively
rotate_and_render('/Users/myusername/Pictures/VR', 'render%d.jpg', subject = bpy.data.objects["Cube"])
'''
'''
bpy.context.scene.render.filepath = 'pathToOutputImage'
bpy.context.scene.render.resolution_x = w #perhaps set resolution in code
bpy.context.scene.render.resolution_y = h
bpy.ops.render.render()

'''
'''

bpy.context.scene.render.filepath = 'E:\OneDrive\Computer Engineering MSc\Thesis\Blender Files\Scripting\output\test.jpg'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.use_file_extension=True
bpy.ops.render.render(write_still=True)

'''


bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'


#Camera to look at centre
import bpy

cam = bpy.context.scene.camera
object = bpy.context.active_object

direction = cam.location - object.location

rot = direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
loc = mathutils.Matrix.Translation(cam.location)

cam.matrix_world =  loc @ rot