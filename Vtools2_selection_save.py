import bpy

class VTOOLS2_PP_SavedSelection(bpy.types.PropertyGroup):
    """Saved selection."""
    name: bpy.props.StringProperty( name = 'SavedSelectionObjName', description = 'Saved Selection data - ObjName.', default = '')

class VTOOLS2_PP_SavedActive(bpy.types.PropertyGroup):
    """Saved active object."""
    name: bpy.props.StringProperty( name = 'SavedActiveObjName', description = 'Saved Active data - ObjName.', default = '')

class VTOOLS2_OT_selection_save(bpy.types.Operator):
    '''Save the current object selection'''
    bl_idname = 'vtools.selection_save'
    bl_label = 'Save Selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        selected_objects = bpy.context.selected_objects
        active_object = bpy.context.active_object

        context.scene.saved_selection.clear()
        for o in selected_objects:
            item = context.scene.saved_selection.add()
            item.name = o.name

        context.scene.saved_active.clear()
        a = context.scene.saved_active.add()
        a.name = active_object.name

        return ('FINISHED')


class VTOOLS2_OT_selection_load(bpy.types.Operator):
    '''Load the current object selection'''
    bl_idname = 'vtools.selection_load'
    bl_label = 'Load Selection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for obj in context.scene.saved_selection:
            print(obj.name)

        return ('FINISHED')
        