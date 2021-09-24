import bpy

class VTOOLS2_OT_generate_height_layers(bpy.types.Operator):
    '''Duplicate all -main layers and create -height layers.'''
    bl_idname = 'vtools.generate_height_layers'
    bl_label = 'Generate Height Layers'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        def get_collections(collection, col_list):
            col_list.append(collection)
            for sub_collection in collection.children:
                get_collections(sub_collection, col_list)

        # get the list of collections for current view layer
        collection_list = []
        get_collections( bpy.context.view_layer.layer_collection, collection_list )

        
        def add_height_layer(view_layer, collection_list):
            height_layer_name = view_layer.name.replace('-main', '-height')
            height_layer = bpy.context.scene.view_layers.new(height_layer_name)
            height_layer.



        print('x')
        
        return {'FINISHED'}