bpy.data.objects['Plane'].select_set(False) 
#Select all the random cubes then delete them
bpy.ops.object.select_same_collection(collection="cubes")
bpy.data.objects['Cube'].select_set(False) 
bpy.ops.object.delete()