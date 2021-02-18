import bpy

class VTOOLS2_OT_add_excluded_collection(bpy.types.Operator):
    '''Add a collection that's excluded in all View layers'''
    bl_idname = 'vtools.add_excluded_collection'
    bl_label = 'Add Excluded Collection'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        scn = bpy.context.scene
        added_collection = bpy.data.collections.new('Excluded Collection')
        scn.collection.children.link(added_collection)

        for view_layer in scn.view_layers:
            collection_in_view_layer = view_layer.layer_collection.children.get(added_collection.name)
            collection_in_view_layer.exclude = True

        return{'FINISHED'}