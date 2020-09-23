import bpy

class Vtools2_images_pack(bpy.types.Operator):
    '''Unpack all packed images to /textures folder.'''
    bl_idname = 'scene.images_pack'
    bl_label = 'Pack Images'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        for img in bpy.data.images:
            image_name = bpy.path.display_name_from_filepath(img.name)
            print(image_name)
        
        # bpy.ops.file.pack_all()

        # for img in bpy.data.images:
        #     if img.tiles is not None:
        #         for tile in img.tiles:
        #             path = '//textures/' + base_name + 
        #             bpy.ops.image.save_as(save_as_render=False, filepath="//textures\\udim-test.1001.png", relative_path=True, show_multiview=False, use_multiview=False)

        return {'FINISHED'}