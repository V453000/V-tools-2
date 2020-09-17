class view_layer_panel(bpy.types.Panel):
  bl_space_type = 'PROPERTIES'
  bl_region_type = 'WINDOW'
  bl_context = 'view_layer'
  bl_category = 'V-tools-2-view-layers'
  bl_label = 'V-tools-2-view-layers'
  bl_idname = 'view_layer_panel_layout'

  def draw(self,context):
    layout = self.layout
    row.operator('scene.generate_render_nodes', text = 'Generate Render Nodes', icon = 'NODETREE')
