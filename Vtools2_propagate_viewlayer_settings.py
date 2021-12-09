import bpy

class VTOOLS2_OT_propagate_viewlayer_settings(bpy.types.Operator):
    bl_idname = 'vtools.propagate_viewlayer_settings'
    bl_label = 'Propagate Viewlayer Settings'
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = 'Propagates viewlayer settings like "Holdout" and "Indirect-only" to the children of all collections'

    def execute(self, context):

        def check_children(collection):
            if len(collection.children) > 0:
                for child in collection.children:
                    if collection.holdout == True:
                        child.holdout = True
                        
                    if collection.indirect_only == True:
                        child.indirect_only = True

                    check_children(child)

        for view_layer in bpy.context.scene.view_layers:
            master_collection = view_layer.layer_collection
            for collection in master_collection.children:
                check_children(collection)
        return {'FINISHED'}