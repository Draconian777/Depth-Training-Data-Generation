import bpy
from random import randint, uniform
from math import radians
import mathutils
from mathutils import Vector
from random import randint, uniform
import os
import cv2
import numpy as np
import csv


focalLength = 50
bpy.data.cameras[0].lens=focalLength
baseLine=1
totalScenes=64  #Total number of scenes to generate 
#pathL="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/Left/"
#pathR="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/Right/"
#pathD="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/Depth/"
#path="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/"
pathD="I:/TrainingData/Depth/"
pathR="I:/TrainingData/Right/"
pathL="I:/TrainingData/Left/"
startingSceneIndex=0

#Prepare Metadata file    
header=['Scene Index', 'Cam Position', 'Depth Image', 'Depth Data','Left Camera', 'Right Camera', 'Focal length', 'Base Line']

if startingSceneIndex==0:
    with open('DataOutput/MetaData.csv','w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(header)
    

def generateScene():

    bpy.data.objects['Plane'].select_set(True) 
    bpy.data.objects['Camera'].select_set(True) 
    bpy.ops.object.select_all(action='INVERT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0.5), scale=(1, 1, 1))

    #Set Active Object to be 'Plane'
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Plane'].select_set(True) 
    bpy.context.view_layer.objects.active = bpy.data.objects['Plane']


    bpy.context.active_object.select_set(False)
    bpy.data.objects['Plane'].select_set(True) 

    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_random(ratio=0.03, seed=randint(-10,50))
    bpy.ops.object.mode_set(mode = 'OBJECT')


    #Before running the scrip, make sure the plane is selected in object mode.
    #assign objects to variable

    cube=bpy.data.objects ['Cube']

    #access the active object, which is the plane
    obj=bpy.context.active_object


    #create the list of all vertices that we select using list comprehensoin.
    #use co array of the MeshVertex struct to access the local  vertex coordinate. In order to
    #get the global coordinates, we must multiply it by the world transformation Matrix.

    selected = [(obj.matrix_world @ v.co) for v in obj.data.vertices if v.select]
    #Note to self
    #Modify the above array to include a random set of coordinates
    #Modify Scaling

    #Loop through all the selected vertices and add cubes at each of them.

    for vertix in selected:
        #we need to name each object, so we concatenate the word
        #cube with the coords
        name = f'cube {vertix}'
        
        
        #create a new cube and give it the name and object data from the original cube.
        #We will assign the new object to a var.
        new_cube=bpy.data.objects.new(name=name, object_data = cube.data)
        
        #position the cube ath tcoordinat of hte selected vertex
        new_cube.location = (vertix[0], vertix[1], vertix[2])
        
        scaleX = uniform(0.6,2)
        scaleY = uniform(0.6,2)
        scaleZ = uniform(0.6,9)
        new_cube.scale = (scaleX,scaleY,scaleZ)
        
        rotX=randint(-10,10)*0
        rotZ=randint(-10,10)*0
        rotY=randint(-10,10)*0
        new_cube.rotation_euler = (radians(rotX),radians(rotY),radians(rotZ))
        
        #add the cube the cube collection
        bpy.data.collections["cubes"].objects.link(new_cube)
        
        
    #Deselect vertices    
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.select_random(ratio=1, seed=0, action='DESELECT')
    bpy.ops.object.mode_set(mode = 'OBJECT')


def aimCam():
    cam = bpy.context.scene.camera
    #object = bpy.context.active_object
    object = bpy.data.objects['Cube']

    direction = cam.location - object.location

    rot = direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    loc = mathutils.Matrix.Translation(cam.location)

    cam.matrix_world =  loc @ rot



def moveCam(X,Y,Z):
    #bpy.data.objects['Cube'].select_set(False) 
    #bpy.data.objects['Plane'].select_set(False) 
    #bpy.data.objects['Camera'].select_set(True) 
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Camera'].select_set(True) 
    bpy.context.view_layer.objects.active = bpy.data.objects['Camera']
    bpy.ops.transform.translate(value=(X, Y, Z), orient_type='GLOBAL')


def moveBase(Baseline):
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
    
    
def get_depth():
    """Obtains depth map from Blender render.
    return: The depth map of the rendered camera view as a numpy array of size (H,W).
    """
    z = bpy.data.images['Viewer Node']
    w, h = z.size
    dmap = np.array(z.pixels[:], dtype=np.float16) # convert to numpy array
    dmap = np.reshape(dmap, (h, w, 4))[:,:,0]
    dmap = np.rot90(dmap, k=2)
    dmap = np.fliplr(dmap)
    return dmap    
    
def render(index,cam,scene,path):
    #change rendering Engine to Workbench for faster image generattion
    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'      
    
    bpy.context.scene.render.filepath = "%sScene%sIm%s%s"%(path,str(scene),str(index),cam)
    bpy.context.scene.render.resolution_x = 960
    bpy.context.scene.render.resolution_y = 540
    bpy.context.scene.render.use_file_extension=True
    bpy.context.scene.render.image_settings.file_format='JPEG'  #JPEG #PNG
    bpy.ops.render.render(write_still=True)
    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write("Scene%sIm%s%s.jpg,"%(str(scene),str(index),cam))
        
    bpy.context.scene.render.filepath = "I:/TrainingData/temp"    
        
        
def renderDepth(index,cam='D',scene=0,path="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/"):
    
    # Change Rendering Engine to Cycles and enable Z pass
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.view_layers["ViewLayer"].use_pass_z = True
 
    bpy.ops.render.render(False, animation=False, write_still=True)
    dmap = get_depth()   
        
    dmap1=dmap*255
    dmap1 = dmap1.astype(np.uint8)
    
    
    im_path= "%sScene%sIm%s%s.jpg"%(path,str(scene),str(index),cam) 
    cv2.imwrite(im_path, dmap1)

    #Write Depth imagefile name
    with open('DataOutput/MetaData.csv','a') as f:
        f.write("Scene%sIm%s%s.jpg,"%(str(scene),str(index),cam))


    # save numpy array as csv file
    # define data
    # save to csv file
    
    #csv_path= "%sScene%sIm%s%s.csv"%(path,str(scene),str(index),cam) 
    #np.savetxt(csv_path, dmap1,fmt='%d', delimiter=',')
    npz_path= "%sScene%sIm%s%s.npz"%(path,str(scene),str(index),cam) 
    np.savez_compressed(npz_path, dmap1=dmap1)
    #Write Depth data file name
    with open('DataOutput/MetaData.csv','a') as f:
        f.write("Scene%sIm%s%s.npz,"%(str(scene),str(index),cam) )



#####################################################################
################### Data Generation Procedure #######################   
#####################################################################    
    

#Specify Variables


    
for sceneIndex in range(startingSceneIndex, startingSceneIndex + totalScenes):

    
    generateScene()
    

    returnStart()
    aimCam()    
    #Rotation Loop starts here potion 0----------
    ###
    
    #Print Postion index
    index=0
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')
        
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"    
        
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    bpy.context.scene.render.filepath = "%sScene%sIm%s%s"%(pathD,str(sceneIndex),str(index),cam)
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine) 
    
    #Render Image    
    cam="L"
    render(index,cam,sceneIndex,pathL)
    
    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)

   
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"



    #Print Focal Length and Baseline
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")
    
    #move to position 1-----------
    

    
    moveCam(0,12,0)
    aimCam()
    index+=1
    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')    
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)
    
    #Render Image
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)
    
    #bpy.context.scene.render.filepath = "%sScene%sIm%s%s"%(path,str(scene),str(index),'D')
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"


    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")

    #move to position 2--------------------

            
    moveCam(0,12,0)
    aimCam()
    index+=1
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')
            
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)
    
    #Render Image
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"

    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")    

    #move to position 3-----------------


    
    moveCam(-12,0,0)
    aimCam()
    index+=1
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')
            
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)
    
    #Render Image
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)

    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"
    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")    

    #move to position 4----------------------
    

    
    moveCam(-12,0,0)
    aimCam()
    index+=1

    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')
            
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)
    
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)

    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"

    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")        
    
    
    #move to position 5------------------------
    


    moveCam(0,-12,0)
    aimCam()
    index+=1
    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')   
         
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)
    
    #Render Image
    
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"


    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")    

    #move to position 6--------------------------

    moveCam(0,-12,0)
    aimCam()
    index+=1
        
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')

    
    
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)   
    
    #Render Image
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)
    
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"

    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")    
    
    #move to position 7--------------------------
    
    moveCam(12,0,0)
    aimCam()
    index+=1
        
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(sceneIndex))
        f.write(',')
        f.write(str(index))
        f.write(',')


    
    
    #Render Depth
    cam="D"
    moveBase(0.5*baseLine)
    aimCam()
    renderDepth(index,cam,sceneIndex,pathD)
    moveBase(-0.5*baseLine)   
    
    
    
    
    #Render Image
    cam="L"
    render(index,cam,sceneIndex,pathL)

    moveBase(baseLine)
    cam="R"
    render(index,cam,sceneIndex,pathR)
    moveBase(-1*baseLine)
    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/temp"
 
    
    with open('DataOutput/MetaData.csv','a') as f:
        f.write(str(focalLength))
        f.write(',')
        f.write(str(baseLine))
        f.write("\n")    
        
        
    returnStart()
    aimCam()



