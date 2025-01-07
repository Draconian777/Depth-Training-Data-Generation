import bpy
import cv2
import numpy as np
import os



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


'''

def dmap2norm(dmap):
    """Computes surface normals from a depth map.
    :param dmap: A grayscale depth map image as a numpy array of size (H,W).
    :return: The corresponding surface normals map as numpy array of size (H,W,3).
    """
    zx = cv2.Sobel(dmap, cv2.CV_64F, 1, 0, ksize=5)
    zy = cv2.Sobel(dmap, cv2.CV_64F, 0, 1, ksize=5)

    # convert to unit vectors
    normals = np.dstack((-zx, -zy, np.ones_like(dmap)))
    length = np.linalg.norm(normals, axis=2)
    normals[:, :, :] /= length

    # offset and rescale values to be in 0-1
    normals += 1
    normals /= 2
    return normals[:, :, ::-1].astype(np.float32)
'''




def renderDepth(index,cam='D',path="E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/DataOutput/"):
    
    

    #bpy.context.scene.render.filepath = "E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/rgb.png"
    bpy.ops.render.render(False, animation=False, write_still=True)
    dmap = get_depth()
    #nmap = dmap2norm(dmap)
    #np.savez_compressed("d.npz", dmap=dmap, nmap=nmap)

    im_path= r'E:/OneDrive/Computer Engineering MSc/Thesis/Blender Files/Scripting/output2/'
    
    
    
    dmap1=dmap*255
    dmap1 = dmap1.astype(np.uint8)
    #dmap1=np.astype(np.int32)
    #dmap1=np.around(dmap1,decimals=3)

    #cv2.imwrite(os.path.join(im_path , 'depth.png'), dmap1)
    im_path= "%sIM%s%s.png"%(path,str(index),cam) 
    cv2.imwrite(im_path, dmap1)
    #cv2.imwrite('normals.png', nmap * 255)


    # save numpy array as csv file
    # define data
    # save to csv file
    
    csv_path= "%sIM%s%s.csv"%(path,str(index),cam) 
    np.savetxt(csv_path, dmap1,fmt='%d', delimiter=',')
    npz_path= "%sIM%s%s.npz"%(path,str(index),cam) 
    np.savez_compressed(npz_path, dmap1=dmap1)



renderDepth(index=0,cam='D')

'''
file = open(os.path.join(im_path ,"depth.txt"), "w+")
content = str(dmap)
file.write(content)
file.close()
'''