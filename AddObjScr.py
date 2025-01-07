import bpy

class TestPanel(bpy.types.Panel):
    bl_label = "test panel"
    bl_idbane = "PT_TestPabel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'My First Addon'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row() #new empty row
        row.label(text="Add Random Object", icon="FORCE_VORTEX")
        row = layout.row()
        row.operator("mesh.primitive_cube_add",icon='CUBE')
        row = layout.row()
        row.operator("mesh.primitive_cube_add(enter_editmode=False, align='WORLD', location=(1, 2, 3), scale=(1,2, 3))",icon='SPHERE')
        #row.operator("mesh.primitive_uv_sphere_add",icon='SPHERE')
        
        
def register():
    bpy.utils.register_class(TestPanel)
    
def unregister():
    bpy.utils.unregister_class(TestPanel)
    
if __name__ == "__main__":
    register()
    