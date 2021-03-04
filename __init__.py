# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name":        'V-tools-2',
    "description": 'Various tools.',
    "author":      'V453000',
    "version":     (2, 1, 7),
    "blender":     (2, 90, 0),
    "location":    "View 3D > Tool Shelf",
    "warning":     "",  # used for warning icon and text in addons panel
    "category":    "User"
    }


import bpy
from bpy.app.handlers import persistent

# updater ops import, all setup in this file
from . import addon_updater_ops
class OBJECT_PT_DemoUpdaterPanel(bpy.types.Panel):
    """Panel to demo popup notice and ignoring functionality"""
    bl_label = "V-Tools-2 Updates"
    bl_idname = "VTOOLS2_PT_updater_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
    bl_context = "objectmode"
    bl_category = "V-Tools-2"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        # Call to check for update in background
        # note: built-in checks ensure it runs at most once
        # and will run in the background thread, not blocking
        # or hanging blender
        # Internally also checks to see if auto-check enabled
        # and if the time interval has passed
        addon_updater_ops.check_for_update_background()


        layout.label(text="V-Tools 2 Updates")
        layout.label(text="")

        col = layout.column()
        col.scale_y = 0.7
        col.label(text="If an update is ready,")
        col.label(text="popup triggered by opening")
        col.label(text="this panel, plus a box ui")

        # could also use your own custom drawing
        # based on shared variables
        if addon_updater_ops.updater.update_ready == True:
            layout.label(text="Custom update message", icon="INFO")
        layout.label(text="")

        # call built-in function with draw code/checks
        addon_updater_ops.update_notice_box_ui(self, context)
@addon_updater_ops.make_annotations
class VTools_preferences(bpy.types.AddonPreferences):
    """Add-on Preferences Panel"""
    bl_idname = __package__

    # addon updater preferences

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
        )
    updater_intrval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
        )
    updater_intrval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=1,
        min=0,
        max=31
        )
    updater_intrval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
        )
    updater_intrval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
        )

    def draw(self, context):
        layout = self.layout

        # works best if a column, or even just self.layout
        mainrow = layout.row()
        col = mainrow.column()

        # updater draw function
        # could also pass in col as third arg
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # col.operator("wm.url_open","Open webpage ").url=addon_updater_ops.updater.website


# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# ----------   E N D   O F   U P D A T E R   S T U F F ---------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------


# V-tools-2 classes import
from . Vtools2_generate_render_nodes       import VTOOLS2_OT_generate_render_nodes
from . Vtools2_view_layer_list             import VTOOLS2_PP_ViewLayerListItem
from . Vtools2_view_layer_list             import VTOOLS2_UL_View_Layer_List
from . Vtools2_view_layer_list             import VTOOLS2_PT_View_Layer_List_Panel
from . Vtools2_view_layer_list             import VTOOLS2_OT_ViewLayerListNewItem
from . Vtools2_view_layer_list             import VTOOLS2_OT_ViewLayerListDeleteItem
from . Vtools2_view_layer_list             import VTOOLS2_OT_ViewLayerListRefresh
from . Vtools2_images_pack                 import VTOOLS2_OT_images_pack
from . Vtools2_images_unpack               import VTOOLS2_OT_images_unpack
from . Vtools2_render_computers            import VTOOLS2_OT_render_multicomputer
from . Vtools2_render_computers            import VTOOLS2_OT_render_singlecomputer
from . Vtools2_relink_images               import VTOOLS2_OT_relink_images
from . Vtools2_save_backup                 import VTOOLS2_OT_save_backup
from . Vtools2_default_render_settings     import VTOOLS2_OT_default_render_settings
from . Vtools2_show_all_collections        import VTOOLS2_PP_CollectionVisibilityShow
from . Vtools2_show_all_collections        import VTOOLS2_OT_show_all_collections
from . Vtools2_show_all_collections        import VTOOLS2_OT_show_all_collections_revert
from . Vtools2_hide_all_collections        import VTOOLS2_PP_CollectionVisibilityHide
from . Vtools2_hide_all_collections        import VTOOLS2_OT_hide_all_collections
from . Vtools2_hide_all_collections        import VTOOLS2_OT_hide_all_collections_revert
from . Vtools2_add_excluded_collection     import VTOOLS2_OT_add_excluded_collection
from . properties_panels                   import VTOOLS2_PT_properties_view_layer
from . tools_panel                         import VTOOLS2_PT_tools_panel

classes = (
    # Preferences
    VTools_preferences,

    # Generate Render Nodes
    VTOOLS2_OT_generate_render_nodes,

    # View Layer List
    VTOOLS2_UL_View_Layer_List,
    VTOOLS2_PP_ViewLayerListItem,
    #VTOOLS2_PT_View_Layer_List_Panel,
    VTOOLS2_OT_ViewLayerListNewItem,
    VTOOLS2_OT_ViewLayerListDeleteItem,
    VTOOLS2_OT_ViewLayerListRefresh,

    # packing images
    VTOOLS2_OT_images_pack,
    VTOOLS2_OT_images_unpack,

    # relink images
    VTOOLS2_OT_relink_images,

    # save backup
    VTOOLS2_OT_save_backup,

    # add excluded collection
    VTOOLS2_OT_add_excluded_collection,

    # default render settings
    VTOOLS2_OT_default_render_settings,

    # render computers
    VTOOLS2_OT_render_multicomputer,
    VTOOLS2_OT_render_singlecomputer,

    # show all collections
    VTOOLS2_PP_CollectionVisibilityShow,
    VTOOLS2_OT_show_all_collections,
    VTOOLS2_OT_show_all_collections_revert,
    # hide all collections
    VTOOLS2_PP_CollectionVisibilityHide,
    VTOOLS2_OT_hide_all_collections,
    VTOOLS2_OT_hide_all_collections_revert,

    # Properties panels
    VTOOLS2_PT_properties_view_layer,
    VTOOLS2_PT_tools_panel,

    # updater panel
    OBJECT_PT_DemoUpdaterPanel,
)

@persistent
def view_layer_list_refresh(scene):
    ''' disabled for now
    bpy.ops.view_layer_list.refresh()
    '''

def register():
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)
    

    # register classes from list
    for cls in classes:
        addon_updater_ops.make_annotations(cls) # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)
    
    # special handler for refreshing view layer list
    bpy.app.handlers.load_post.append(view_layer_list_refresh)
    # creating view layer list props
    bpy.types.Scene.view_layer_list = bpy.props.CollectionProperty(type = VTOOLS2_PP_ViewLayerListItem)
    bpy.types.Scene.view_layer_list_index = bpy.props.IntProperty(name = "Index for view_layer_list", default = 0)

    bpy.types.Scene.collection_visibility_show = bpy.props.CollectionProperty(type = VTOOLS2_PP_CollectionVisibilityShow)
    bpy.types.Scene.collection_visibility_hide = bpy.props.CollectionProperty(type = VTOOLS2_PP_CollectionVisibilityHide)

def unregister():
    # deleting view layer list props
    del bpy.types.Scene.view_layer_list
    del bpy.types.Scene.view_layer_list_index
    # special handler for refreshing view layer list
    bpy.app.handlers.load_post.remove(view_layer_list_refresh)

    # addon updater unregister
    addon_updater_ops.unregister()

    # unregister classes from list
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

