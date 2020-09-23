import bpy

class Vtools2_tools_panel(bpy.types.Panel):
    bl_idname = 'generate_render_nodes_panel'
    bl_label = 'V-Tools-2 Panel'
    bl_category = 'V-Tools-2'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('scene.generate_render_nodes', text = 'Generate Render Nodes', icon = 'NODETREE')
        row = layout.row()
        row.operator('scene.images_pack', text = 'Pack Images', icon = 'PACKAGE')
