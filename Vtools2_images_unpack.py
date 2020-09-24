import bpy

class VTOOLS2_OT_images_unpack(bpy.types.Operator):
    '''Unpack all packed images to /textures folder.'''
    bl_idname = 'vtools.images_unpack'
    bl_label = 'Unpack Images'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        for img in bpy.data.images:
            if img.packed_file is not None:
                img.unpack()
            # image_name = bpy.path.display_name_from_filepath(img.name)
            # print(image_name)
        
        return {'FINISHED'}