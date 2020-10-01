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

        def show_collections(collection):
            for sub_collection in collection.children:
                sub_collection.exclude = False
                show_collections(sub_collection)

        def check_hidden_collections(collection):
            for sub_collection in collection.children:
                if sub_collection.exclude == True:
                    return True
                if check_hidden_collections(sub_collection) == True:
                    return True
                
            return False

        # create a list of collections
        collection_list = []
        get_collections( bpy.context.view_layer.layer_collection, collection_list )

        # change the memory only if any collection is excluded?
        hidden_collection_found = check_hidden_collections(bpy.context.view_layer.layer_collection)
        print('Found hidden:', hidden_collection_found)

        if hidden_collection_found == True:
            # go through the list of collections and save their state to memory
            context.scene.collection_visibility_show.clear()
            for c in collection_list:
                item = context.scene.collection_visibility_show.add()
                item.name = c.name
                item.exclude = c.exclude

        # show all collections
        show_collections(bpy.context.view_layer.layer_collection)

        return {'FINISHED'}


class VTOOLS2_OT_show_all_collections_revert(bpy.types.Operator):
    '''Revert "Show all collections" to original state.'''
    bl_idname = 'vtools.show_all_collections_revert'
    bl_label = 'Revert Show All Collections'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        def revert_collections(collection, col_memory):
            for sub_collection in collection.children:
                if sub_collection.name in col_memory:
                    sub_collection.exclude = col_memory[sub_collection.name].exclude
                revert_collections(sub_collection, col_memory)

        view_layer_collection = bpy.context.view_layer.layer_collection
        collection_memory = bpy.context.scene.collection_visibility_show
        revert_collections(view_layer_collection, collection_memory)

        return {'FINISHED'}

