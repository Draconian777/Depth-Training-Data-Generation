import bpy
import mathutils
from mathutils import Vector
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


#bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'


#Camera to look at centre
#cam = bpy.context.scene.camera

def aimCam():
    cam = bpy.context.scene.camera
    #object = bpy.context.active_object
    object = bpy.data.objects['Cube']

    direction = cam.location - object.location

    rot = direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    loc = mathutils.Matrix.Translation(cam.location)

    cam.matrix_world =  loc @ rot

#path="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/output2/" 
def render(index,cam,path="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/"):
    bpy.context.scene.render.filepath = "%sIM%s%s"%(path,str(index),cam)
    bpy.context.scene.render.resolution_x = 960
    bpy.context.scene.render.resolution_y = 540
    bpy.context.scene.render.use_file_extension=True
    bpy.context.scene.render.image_settings.file_format='PNG'  #PNG
    bpy.ops.render.render(write_still=True)
    


def moveCam(X,Y,Z):
    bpy.data.objects['Cube'].select_set(False) 
    bpy.data.objects['Plane'].select_set(False) 
    bpy.data.objects['Camera'].select_set(True) 
    bpy.ops.transform.translate(value=(X, Y, Z), orient_type='GLOBAL')


def moveBase(Baseline):
    #bpy.data.objects['Cube'].select_set(False) 
    #bpy.data.objects['Plane'].select_set(False) 
    #bpy.data.objects['Camera'].select_set(True) 
    #Set Active Object to be 'Camera'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Camera'].select_set(True) 
    bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
        
    bpy.ops.transform.translate(value=(Baseline, 0, 0), orient_axis_ortho='X', orient_type='LOCAL', constraint_axis=(True, False, False))



def returnStart():
    bpy.data.objects['Cube'].select_set(False) 
    bpy.data.objects['Plane'].select_set(False) 
    bpy.data.objects['Camera'].select_set(True)
    cam = bpy.context.scene.camera
    start=Vector((12.0, -12.0, 9.5))
    delta=start-cam.location
    bpy.ops.transform.translate(value=delta, orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
    
   
   
returnStart()
aimCam()    
#Rotation Loop starts here

index=0
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)

#move to position 1
moveCam(0,12,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)



#move to position 2
moveCam(0,12,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)


#move to position 3
moveCam(-12,0,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)


#move to position 4
moveCam(-12,0,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)

#move to position 5
moveCam(0,-12,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)

#move to position 6
moveCam(0,-12,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)
#move to position 7
moveCam(12,0,0)
aimCam()
index+=1
orient="L"
render(index,orient)

moveBase(1)
orient="R"
render(index,orient)
moveBase(-1)

returnStart()
aimCam()

