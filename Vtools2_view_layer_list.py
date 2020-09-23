import bpy

class ViewLayerListItem(bpy.types.PropertyGroup):
    """The list of data"""
    name: bpy.props.StringProperty( name = 'ViewLayerName', description = 'Name of the View Layer.', default = 'Untitled')

class VTOOLS2_UL_View_Layer_List(bpy.types.UIList):
    """The list widget"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # centralized custom icon definion as here could be code to decide what should the icon be
        custom_icon = 'RENDERLAYERS'

        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text = item.name, icon = custom_icon)
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text = '', icon = custom_icon)

class VTOOLS2_PT_View_Layer_List_Panel(bpy.types.Panel):
    """The panel to be put in Properties window / View Layer tab"""

    bl_label = "View Layers"
    bl_idname = "VTOOLS2_PT_View_Layer_List_Panel"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_context = 'view_layer'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.template_list('ViewLayerUL_List', 'ViewLayerList', scene, 'view_layer_list', scene, 'view_layer_list_index' )

        row = layout.row()
        row.operator('view_layer_list.new_item', text = 'New')
        row.operator('view_layer_list.delete_item', text = 'Delete')
        row.operator('view_layer_list.refresh', text = 'Refresh')

        if scene.view_layer_list_index >= 0 and scene.view_layer_list:
            item = scene.view_layer_list[scene.view_layer_list_index]
            row = layout.row()
            row.prop(item, 'name')



class LIST_OT_ViewLayerListNewItem(bpy.types.Operator):
    """Add a new item to the list of View Layers."""

    bl_label = 'Add a new View Layer'
    bl_idname = 'view_layer_list.new_item'

    def execute(self, context):
        context.scene.view_layer_list.add()

        return{'FINISHED'}

class LIST_OT_ViewLayerListDeleteItem(bpy.types.Operator):
    """Delete the selected item from the list of View Layers."""

    bl_label = 'Remove a View Layer'
    bl_idname = 'view_layer_list.delete_item'

    @classmethod
    def poll(cls, context):
        return context.scene.view_layer_list
    
    def execute(self, context):
        view_layer_list = context.scene.view_layer_list
        index = context.scene.view_layer_list_index

        view_layer_list.remove(index)
        context.scene.view_layer_list_index = min(max(0, index - 1), len(view_layer_list) - 1)

        return{'FINISHED'}

class LIST_OT_ViewLayerListRefresh(bpy.types.Operator):
    """Refresh the list based on current View Layers"""

    bl_label = 'Refresh the View Layer List'
    bl_idname = 'view_layer_list.refresh'

    def execute(self, context):
        context.scene.view_layer_list.clear()

        for viewlayer in context.scene.view_layers:
            item = context.scene.view_layer_list.add()
            item.name = viewlayer.name

        return {'FINISHED'}