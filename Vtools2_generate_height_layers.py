import bpy

class VTOOLS2_OT_generate_height_layers(bpy.types.Operator):
    '''Duplicate all -main layers and create -height layers.'''
    bl_idname = 'vtools.generate_height_layers'
    bl_label = 'Generate Height Layers'
    bl_options = {'REGISTER', 'UNDO'}
    
    AO_identifier : bpy.props.StringProperty(
        name = 'AO Identifier',
        description = 'Suffix or appendix in the name of RenderLayer for rendering AO.',
        default = 'main'
    )
    height_identifier : bpy.props.StringProperty(
        name = 'Height Identifier',
        description = 'Suffix or appendix in the name of RenderLayer for rendering Height.',
        default = 'height'
    )
    height_material_name : bpy.props.StringProperty(
        name = 'Height Material Name',
        description = 'Name of the Height material to be used for the Height pass.',
        default = 'HEIGHT',
    )
    individual_mode : bpy.props.StringProperty(
        name = 'Individual mode',
        description = 'Turn on to only generate from one specific view layer. Leave blank if you want to process all -main layers.',
        default = '',
    )

    def execute(self, context):

        def get_collections(collection, col_list):
            if collection.name != 'Master Collection':
                col_list.append(collection)
            for sub_collection in collection.children:
                get_collections(sub_collection, col_list)
       
        def find_collection(root_collection, searched_name):
            if root_collection.children is not None:
                for child in root_collection.children:
                    if child.name == searched_name:
                        #print('Found', child.name)
                        return child
                    else:
                        result = find_collection(child, searched_name)
                        if result is not None:
                            return result
            else:
                print('No collections found in this scene.')
        
        def add_height_layer(view_layer, collection_list, height_mtl_name):
            if view_layer.name.endswith(self.AO_identifier):
                height_layer_name = view_layer.name.replace(self.AO_identifier, self.height_identifier)
            else:
                height_layer_name = view_layer.name + '-' + self.height_identifier
            # check if the height layer already exists, if not, create it
            if bpy.context.scene.view_layers.get(height_layer_name) is None:
                height_layer = bpy.context.scene.view_layers.new(height_layer_name)
            else:
                height_layer = bpy.context.scene.view_layers.get(height_layer_name)
            if bpy.data.materials.get(height_mtl_name) is not None:
                height_layer.material_override = bpy.data.materials.get(height_mtl_name)
            # match the height layer's settings to the -main settings
            for collection in collection_list:
                #print(collection.name)
                #print(str(collection.exclude))
                #target_collection = height_layer.layer_collection.children.get(collection.name)
                #target_collection = find_collection_in_children(height_layer.layer_collection.children, collection.name)
                #print('Searching for collection ' + collection.name + ' in ' + height_layer.name)
                target_collection = find_collection(height_layer.layer_collection, collection.name)
                # if target_collection is None:
                #     print('Generate height layers: In', view_layer, 'Target collection was "None". Skipping', collection.name, '!'*64)
                if target_collection is not None:
                    #print('target collection:', target_collection.name)
                    target_collection.exclude       = collection.exclude
                    target_collection.holdout       = collection.holdout
                    target_collection.indirect_only = collection.indirect_only
                    target_collection.hide_viewport = collection.hide_viewport
                    #target_collection.hide_render   = collection.hide_render
                    #target_collection.hide_select   = collection.hide_select

        # for col in collection_list:
        #     print(col.name)
        # print('-'*32)
        
        if self.individual_mode == '':
            for layer in bpy.context.scene.view_layers:
                if layer.name.endswith(self.AO_identifier):
                    collection_list = []
                    get_collections( layer.layer_collection, collection_list )
                    add_height_layer(layer, collection_list, self.height_material_name)
        else:
            v = bpy.context.scene.view_layers[self.individual_mode]
            collection_list = []
            get_collections( v.layer_collection, collection_list )
            add_height_layer(v, collection_list, self.height_material_name)
        
        return {'FINISHED'}