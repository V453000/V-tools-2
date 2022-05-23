import bpy

class VTOOLS2_OT_apply_modifiers(bpy.types.Operator):
    '''Apply modifiers to mesh data. Removes modifiers from all objects that use the same mesh data, and keeps them linked.'''
    bl_idname = 'vtools.apply_modifiers'
    bl_label = 'Subsurf Settings'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        for obj in bpy.context.selected_objects:
            # store the data name
            
            # if this data name was already processed, just link it
            
            # make unique data
            original_data_name = obj.data.name.copy()
            if obj.data.users > 1:
                single_user_data = obj.data.copy()
                obj.data = single_user_data
            # apply all modifiers
            for mod in obj.modifiers:
                print(obj.name, '-', mod.name)
            
        # apply all modifiers
        # find all objects with the originally linked data
        # select all objects with the originally linked data
        #     remove all modifiers on all of them
        #     link the data back to the new applied version
        return {'FINISHED'}