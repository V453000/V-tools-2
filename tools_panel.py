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
        row.operator('blend.save_backup', text = 'Save Backup', icon = 'FILE_BACKUP')
        row = layout.row()
        row.operator('scene.images_pack', text = 'Pack Images', icon = 'IMPORT')
        row.operator('scene.images_unpack', text = 'Unpack Images', icon = 'EXPORT')
        row = layout.row()
        row.operator('render.default_render_settings', text = 'Render Settings', icon = 'RESTRICT_RENDER_OFF')
        row = layout.row()
        row.operator('scene.generate_render_nodes', text = 'Generate Render Nodes', icon = 'NODETREE')
        
