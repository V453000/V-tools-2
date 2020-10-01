import bpy

class VTOOLS2_PP_CollectionVisibilityHide(bpy.types.PropertyGroup):
    """Collection visibility data for 'Hide' Function."""
    name: bpy.props.StringProperty( name = 'CollectionVisibilityHideName', description = 'Collection visibility "Hide" data - Name.', default = 'Untitled')
    exclude: bpy.props.BoolProperty( name = 'CollectionVisibilityHideExclude', description = 'Collection visibility "Hide" data - Exclude.', default = False)


class VTOOLS2_OT_hide_all_collections(bpy.types.Operator):
    '''Hide all collections, and remember the last state.'''
    bl_idname = 'vtools.hide_all_collections'
    bl_label = 'Hide All Collections'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        def get_collections(collection, col_list):
            col_list.append(collection)
            for sub_collection in collection.children:
                get_collections(sub_collection, col_list)

        def hide_collections(collection):
            for sub_collection in collection.children:
                sub_collection.exclude = True
                hide_collections(sub_collection)

        def check_shown_collections(collection):
            shown_collection_found = False
            for sub_collection in collection.children:
                if sub_collection.exclude == False:
                    shown_collection_found = True
                shown_collection_found |= check_shown_collections(sub_collection)

            return shown_collection_found

        # create a list of collections
        collection_list = []
        get_collections( bpy.context.view_layer.layer_collection, collection_list )

        # change the memory only if any collection is not excluded?
        shown_collection_found = check_shown_collections(bpy.context.view_layer.layer_collection)
        print('Found shown:', shown_collection_found)

        if shown_collection_found == True:
            # go through the list of collections and save their state to memory
            context.scene.collection_visibility_hide.clear()
            for c in collection_list:
                item = context.scene.collection_visibility_hide.add()
                item.name = c.name
                item.exclude = c.exclude

        # hide all collections
        hide_collections(bpy.context.view_layer.layer_collection)

        return {'FINISHED'}


class VTOOLS2_OT_hide_all_collections_revert(bpy.types.Operator):
    '''Revert "Hide all collections" to original state.'''
    bl_idname = 'vtools.hide_all_collections_revert'
    bl_label = 'Revert Hide All Collections'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        def revert_collections(collection, col_memory):
            for sub_collection in collection.children:
                if sub_collection.name in col_memory:
                    sub_collection.exclude = col_memory[sub_collection.name].exclude
                revert_collections(sub_collection, col_memory)

        view_layer_collection = bpy.context.view_layer.layer_collection
        collection_memory = bpy.context.scene.collection_visibility_hide
        revert_collections(view_layer_collection, collection_memory)

        return {'FINISHED'}

