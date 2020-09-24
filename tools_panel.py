import bpy

class VTOOLS2_PT_tools_panel(bpy.types.Panel):
    bl_idname = 'VTOOLS2_PT_tools_panel'
    bl_label = 'V-Tools-2 Panel'
    bl_category = 'V-Tools-2'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator('vtools.save_backup', text = 'Save Backup', icon = 'FILE_BACKUP')
        row = layout.row()
        row.operator('vtools.images_pack', text = 'Pack Images', icon = 'IMPORT')
        row.operator('vtools.images_unpack', text = 'Unpack Images', icon = 'EXPORT')
        row = layout.row()
        row.operator('vtools.relink_images', text = 'Relink Images', icon = 'LIBRARY_DATA_BROKEN')
        row = layout.row()
        row.operator('vtools.default_render_settings', text = 'Render Settings', icon = 'RESTRICT_RENDER_OFF')
        row = layout.row()
        row.operator('vtools.generate_render_nodes', text = 'Generate Render Nodes', icon = 'NODETREE')
        
