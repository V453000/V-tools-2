import bpy

class VTOOLS2_OT_render_multicomputer(bpy.types.Operator):
    '''Set rendering to multi-computer.'''
    bl_idname = 'vtools.render_multicomputer'
    bl_label = 'Render Multi-computer'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        scn = bpy.context.scene

        scn.render.filepath = '//cache\\\\' + scn.name + '/' + scn.name + '-cache_'
        scn.render.image_settings.file_format = 'PNG'
        scn.render.image_settings.color_mode = 'RGBA'
        scn.render.use_overwrite = False
        scn.render.use_placeholder = True
        
        return {'FINISHED'}

class VTOOLS2_OT_render_singlecomputer(bpy.types.Operator):
    '''Set rendering to single computer.'''
    bl_idname = 'vtools.render_singlecomputer'
    bl_label = 'Render Single computer'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        scn = bpy.context.scene

        scn.render.filepath = '//OUTPUT\\\\x\\x_'
        scn.render.image_settings.file_format = 'PNG'
        scn.render.image_settings.color_mode = 'RGBA'
        scn.render.use_overwrite = True
        scn.render.use_placeholder = False
        
        return {'FINISHED'}