import bpy

class VTOOLS2_OT_generate_shadow_layers(bpy.types.Operator):
    '''Duplicate all -main layers and create -shadow layers.'''
    bl_idname = 'vtools.generate_shadow_layers'
    bl_label = 'Generate Shadow Layers'
    bl_options = {'REGISTER', 'UNDO'}
    
    AO_identifier : bpy.props.StringProperty(
        name = 'AO Identifier',
        description = 'Suffix or appendix in the name of RenderLayer for rendering AO.',
        default = 'main'
    )
    shadow_identifier : bpy.props.StringProperty(
        name = 'Shadow Identifier',
        description = 'Suffix or appendix in the name of RenderLayer for rendering Shadow.',
        default = 'shadow'
    )
    exclude_collections : bpy.props.StringProperty(
        name = 'Exclude Collections',
        description = 'Collections to exclude for shadow passes. !!! Must be formatted as a single string, separated by ",|---|, " !!!',
        default = 'Lighting, Ground Plane'
    )
    include_collections : bpy.props.StringProperty(
        name = 'Include Collections',
        description = 'Collections to include for shadow passes. !!! Must be formatted as a single string, separated by ",|---|, " !!!',
        default = 'Shadow Plane, Shadow Lamp'
    )
    individual_mode : bpy.props.StringProperty(
        name = 'Individual Mode',
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
        
        def force_collection_separator(collections):
            for collection in collections.children:
                #print(collection.name)
                bpy.data.collections[collection.name].name = collection.name.replace(', ', ',_')
                force_collection_separator(collection)

        def add_shadow_layer(view_layer, collection_list):
            if view_layer.name.endswith(self.AO_identifier):
                shadow_layer_name = view_layer.name.replace(self.AO_identifier, self.shadow_identifier)
            else:
                shadow_layer_name = view_layer.name + '-' + self.shadow_identifier
            # check if the shadow layer already exists, if not, create it
            if bpy.context.scene.view_layers.get(shadow_layer_name) is None:
                shadow_layer = bpy.context.scene.view_layers.new(shadow_layer_name)
            else:
                shadow_layer = bpy.context.scene.view_layers.get(shadow_layer_name)            
            # match the shadow layer's settings to the -main settings
            for collection in collection_list:
                #print(collection.name)
                #print(str(collection.exclude))
                #target_collection = shadow_layer.layer_collection.children.get(collection.name)
                #target_collection = find_collection_in_children(shadow_layer.layer_collection.children, collection.name)
                #print('Searching for collection ' + collection.name + ' in ' + shadow_layer.name)
                target_collection = find_collection(shadow_layer.layer_collection, collection.name)
                # if target_collection is None:
                #     print('Generate shadow layers: In', view_layer,'Target collection was "None". Skipping', collection.name, '!'*64)
                if target_collection is not None:
                    #print('target collection:', target_collection.name)

                    target_collection.exclude       = collection.exclude
                    target_collection.holdout       = collection.holdout
                    target_collection.indirect_only = collection.indirect_only
                    target_collection.hide_viewport = collection.hide_viewport

                    if collection.exclude == False:
                        target_collection.indirect_only = True
                    if collection.holdout == True:
                        target_collection.exclude = True
                    if collection.indirect_only == True:
                        target_collection.exclude = True
                    
                    megalist_separator = ', '
                    exclude_megalist = self.exclude_collections
                    exclude_list = exclude_megalist.split(megalist_separator)
                    for exclude_collection_name in exclude_list:
                        if exclude_collection_name != '':
                            target_exclude_collection = find_collection(shadow_layer.layer_collection, exclude_collection_name)
                            if target_exclude_collection is not None:
                                target_exclude_collection.exclude = True
                            else:
                                print('Collection to exclude:', exclude_collection_name, 'not found.')

                    include_megalist = self.include_collections
                    include_list = include_megalist.split(megalist_separator)
                    #print(include_list)
                    for include_collection_name in include_list:
                        if include_collection_name != '':
                            target_include_collection = find_collection(shadow_layer.layer_collection, include_collection_name)
                            if target_include_collection is not None:
                                target_include_collection.exclude = False
                                target_include_collection.holdout = False
                                target_include_collection.indirect_only = False
                            else:
                                print('Collection to include:', include_collection_name, 'not found.')
        
        print('-'*32)
        # start with making sure the naming of collections is acceptable
        force_collection_separator(bpy.context.view_layer.layer_collection)
        # get the list of collections for current view layer
        # collection_list = []
        # get_collections( bpy.context.view_layer.layer_collection, collection_list )
        # for col in collection_list:
        #     print(col.name)
                
        if self.individual_mode == '':
            for layer in bpy.context.scene.view_layers:
                if layer.name.endswith(self.AO_identifier):
                    collection_list = []
                    get_collections( layer.layer_collection, collection_list )
                    add_shadow_layer(layer, collection_list)
        else:
            v = bpy.context.scene.view_layers[self.individual_mode]
            collection_list = []
            get_collections( v.layer_collection, collection_list )
            add_shadow_layer(v, collection_list)
        
        return {'FINISHED'}