import bpy

class VTOOLS2_OT_relink_images(bpy.types.Operator):
    '''Finds and replaces parts of image paths.'''
    bl_idname = 'vtools.relink_images'
    bl_label = 'Relink Images'
    bl_options = {'REGISTER', 'UNDO'}

    # Settings
    path_find : bpy.props.StringProperty(
        name = 'Find',
        description = 'Path string to search for.',
        default = '10.0.0.1\\tank_volume1'
    )
    path_replace : bpy.props.StringProperty(
        name = 'Replace',
        description = 'Path string to replace with.',
        default = 'nas.factorio.com\\tank'
    )

    def execute(self, context):

        for img in bpy.data.images:
            image_filename = img.filepath

            if self.path_find in image_filename:
                print('Found and replaced to:')
                replaced_path = image_filename.replace(self.path_find, self.path_replace)
                img.filepath = replaced_path
                print(replaced_path)
                
        return {'FINISHED'}


