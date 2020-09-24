import bpy
import math

class VTOOLS2_OT_default_render_settings(bpy.types.Operator):
    '''Set our default render settings'''
    bl_idname = 'vtools.default_render_settings'
    bl_label = 'Default Render Settings'
    bl_options = {'REGISTER', 'UNDO'}

    set_for_all_scenes = bpy.props.EnumProperty(
        name = 'Scene:',
        description = 'Target scenes to change settings of.',
        items = [
            ('THIS', 'This Scene', '', 'FILE_IMAGE', 0),
            ('ALL', 'All Scenes', '', 'RENDERLAYERS', 1)
        ]
    )

    def execute(self, context):

        if self.set_for_all_scenes == 'THIS':
            list_of_scenes = [bpy.context.scene]
        else:
            list_of_scenes = []
            for scene in bpy.data.scenes:
                list_of_scenes.append(scene)

        for scn in list_of_scenes:

            scn.render.engine = 'CYCLES'
            scn.cycles.device = 'GPU'

            scn.render.tile_x = scn.render.resolution_x
            scn.render.tile_y = scn.render.resolution_y

            scn.cycles.samples = 1024

            scn.render.film_transparent = True

        return{'FINISHED'}