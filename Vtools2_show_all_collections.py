import bpy

class VTOOLS2_PP_CollectionVisibilityShow(bpy.types.PropertyGroup):
    """Collection visibility data for 'Show' Function."""
    name: bpy.props.StringProperty( name = 'CollectionVisibilityShowName', description = 'Collection visibility "Show" data - Name.', default = 'Untitled')
    exclude: bpy.props.BoolProperty( name = 'CollectionVisibilityShowExclude', description = 'Collection visibility "Show" data - Exclude.', default = False)


class VTOOLS2_OT_show_all_collections(bpy.types.Operator):
    '''Show all collections, and remember the last state.'''
    bl_idname = 'vtools.show_all_collections'
    bl_label = 'Show All Collections'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        def get_collections(collection, col_list):
            col_list.append(collection)
            for sub_collection in collection.children:
                get_collections(sub_collection, col_list)

        #collection_memory = []
        #context.scene.collection_visibility_show.clear()
        collection_memory = []
        get_collections( bpy.context.view_layer.layer_collection, collection_memory )

        for c in collection_memory:
            item = context.scene.collection_visibility_show.add()
            item.name = c.name
            item.exclude = c.exclude
            print(c.name, '||', c.exclude)

        return {'FINISHED'}

class VTOOLS2_OT_show_all_collections_revert(bpy.types.Operator):
    '''Revert collection visibility to the last remembered state.'''
    bl_idname = 'vtools.show_all_collections_revert'
    bl_label = 'Revert Collection Visibility'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        


        return {'FINISHED'}