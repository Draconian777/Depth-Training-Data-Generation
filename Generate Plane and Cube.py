import bpy


collection2 = bpy.data.collections.new("planeCol") 
bpy.context.scene.collection.children.link(collection2)

planesize=25
Cuts=int(planesize*0.5)
Plane=bpy.ops.mesh.primitive_plane_add(size=planesize, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.data.collections["planeCol"].objects.link(Plane)


bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.subdivide(number_cuts=Cuts)


collection = bpy.data.collections.new("cubes") 
bpy.context.scene.collection.children.link(collection)
