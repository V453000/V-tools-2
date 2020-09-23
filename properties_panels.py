import bpy

class VTOOLS2_PT_properties_view_layer(bpy.types.Panel):
    bl_idname = 'VTOOLS2_PT_view_layer_panel_layout'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'view_layer'
    bl_category = 'V-tools-2-view-layers'
    bl_label = 'V-tools-2'

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        row.operator('vtools.generate_render_nodes', text = 'Generate Render Nodes', icon = 'NODETREE')
