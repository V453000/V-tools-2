import bpy

class VTOOLS2_OT_sort_view_layers(bpy.types.Operator):
    '''Sorts View Layers Alphabetically'''
    bl_idname = 'vtools.sort_view_layers'
    bl_label = 'Sort View Layers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        # Create a dictionary and sort it alphabetically
        view_layer_dict = dict(bpy.context.scene.view_layers.items())
        sorted_view_layer_dict = dict(sorted(view_layer_dict.items(), key=lambda x: x[0].lower()))

        # Duplicate View layers in the right order
        for idx, (name, vl) in enumerate(sorted_view_layer_dict.items()):
            bpy.context.window.view_layer = vl
            bpy.ops.scene.view_layer_add(type='COPY') 
            new_vl = bpy.context.view_layer 

        # Delete old view layers
        for name, vl in view_layer_dict.items():
            bpy.context.window.view_layer = vl 
            bpy.ops.scene.view_layer_remove()

        #fix names
        for view_layer in bpy.context.scene.view_layers:
            view_layer.name = view_layer.name.replace("_001", "")
            
        return {'FINISHED'}