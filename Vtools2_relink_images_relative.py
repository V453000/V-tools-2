import bpy

class VTOOLS2_OT_relink_images_relative(bpy.types.Operator):
    '''Set all paths of all images to the relative path from this Blend file location.'''
    bl_idname = 'vtools.relink_images_relative'
    bl_label = 'Relative Paths'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        bpy.ops.vtools.relink_images(path_find = bpy.path.abspath('//'), path_replace = '//')
        
        return {'FINISHED'}