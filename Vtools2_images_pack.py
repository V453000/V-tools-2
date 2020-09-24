import bpy

class VTOOLS2_OT_images_pack(bpy.types.Operator):
    '''Pack all images to the .blend file.'''
    bl_idname = 'vtools.images_pack'
    bl_label = 'Pack Images'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        for img in bpy.data.images:
            if img.tiles is None:
                img.pack()
            # image_name = bpy.path.display_name_from_filepath(img.name)
            # print(image_name)
        
        return {'FINISHED'}