import bpy

def draw_ui(self, context, compositor:bool = False):
    layout = self.layout
    box = layout.box()
    box.label(text = 'Blend file')
    row = box.row()
    row.operator('vtools.save_backup', text = 'Save Backup', icon = 'FILE_BACKUP')
    
    box = layout.box()
    box.label(text = 'Image packing')
    row = box.row()
    row.operator('vtools.images_pack', text = 'Pack Images', icon = 'IMPORT')
    row.operator('vtools.images_unpack', text = 'Unpack Images', icon = 'EXPORT')
    row = box.row()
    row.operator('vtools.relink_images', text = 'Relink Images', icon = 'LIBRARY_DATA_BROKEN')
    row.operator('vtools.relink_images_relative', text = 'Relative Paths', icon = 'CON_FOLLOWPATH')
    
    box = layout.box()
    box.label(text = 'Render settings')
    row = box.row()
    row.operator('vtools.default_render_settings', text = 'Render Settings', icon = 'RESTRICT_RENDER_OFF')
    row = box.row()
    row.operator('vtools.render_singlecomputer', text = 'Render 1 PC', icon = 'LAYER_ACTIVE')
    row.operator('vtools.render_multicomputer', text = 'Render N PC', icon = 'OUTLINER_OB_POINTCLOUD')

    box = layout.box()
    box.label(text = 'Collection visibility')
    row = box.row(align = True)
    row.operator('vtools.show_all_collections', text = 'Show All', icon = 'HIDE_OFF')
    row.operator('vtools.show_all_collections_revert', text = 'Revert', icon = 'RECOVER_LAST')
    row = box.row(align = True)
    row.operator('vtools.hide_all_collections', text = 'Hide All', icon = 'HIDE_ON')
    row.operator('vtools.hide_all_collections_revert', text = 'Revert', icon = 'RECOVER_LAST')

    box = layout.box()
    box.label(text = 'Collections')
    row = box.row(align = True)
    row.operator('vtools.add_excluded_collection', text = 'Add Excluded', icon = 'COLLECTION_NEW')
    row = box.row()
    row.operator('vtools.propagate_viewlayer_settings', text = 'Propagate Settings', icon = 'OUTLINER')

    #if not compositor:
    box = layout.box()
    box.label(text = 'Objects')
    row = box.row(align = True)
    row.operator('vtools.viewport_display', text = 'Viewport Display', icon = 'RESTRICT_VIEW_OFF')
    row = box.row(align = True)
    row.operator('vtools.ray_visibility', text = 'Ray visibility', icon = 'RESTRICT_RENDER_OFF')
    row = box.row(align = True)
    row.operator('vtools.selection_save', text = 'Save Selection', icon = 'COPYDOWN')
    row.operator('vtools.selection_load', text = 'Load Selection', icon = 'PASTEDOWN')

    box = layout.box()
    box.label(text = 'Materials')
    row = box.row(align = True)
    row.operator('vtools.link_material_to', text = 'Link material to...', icon = 'LINKED')

    box = layout.box()
    box.label(text = 'Modifiers')
    row = box.row(align = True)
    row.operator('vtools.subsurf_settings', text = 'Subsurf Settings', icon = 'MOD_SUBSURF')
    row = box.row(align = True)
    row.operator('vtools.apply_modifiers', text = 'Apply Modifiers', icon = 'CHECKMARK')

    box = layout.box()
    box.label(text = 'View Layers')
    # row = box.row()
    # row.operator('vtools.generate_height_layers', text = 'Generate Height Layers', icon = 'RENDERLAYERS')
    # row = box.row()
    # row.operator('vtools.generate_shadow_layers', text = 'Generate Shadow Layers', icon = 'LIGHT')
    row = box.row()
    row.operator('vtools.sort_view_layers', text = 'Sort View Layers', icon = 'RENDERLAYERS')
    row = box.row()
    row.operator('vtools.generate_render_nodes', text = 'Generate Render Nodes', icon = 'NODETREE')



class VTOOLS2_PT_tools_panel(bpy.types.Panel):
    bl_idname = 'VTOOLS2_PT_tools_panel'
    bl_label = 'V-Tools-2 Panel'
    bl_category = 'V-Tools-2'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        draw_ui(self, context, False)

class VTOOLS2_PT_compositor_tools_panel(bpy.types.Panel):
    bl_idname = 'VTOOLS2_PT_compositor_tools_panel'
    bl_label = 'V-Tools-2 Compositor Panel'
    bl_category = 'V-Tools-2'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        draw_ui(self, context, True)
