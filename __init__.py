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
	"version":     (2, 0, 0),
	"blender":     (2, 90, 0),
	"location":    "View 3D > Tool Shelf > Demo Updater",
	"warning":     "",  # used for warning icon and text in addons panel
	"category":    "User"
	}


import bpy
from bpy.app.handlers import persistent

# updater ops import, all setup in this file
from . import addon_updater_ops
class OBJECT_PT_DemoUpdaterPanel(bpy.types.Panel):
	"""Panel to demo popup notice and ignoring functionality"""
	bl_label = "Updater Demo Panel"
	bl_idname = "OBJECT_PT_hello"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS' if bpy.app.version < (2, 80) else 'UI'
	bl_context = "objectmode"
	bl_category = "Tools"

	def draw(self, context):
		layout = self.layout

		# Call to check for update in background
		# note: built-in checks ensure it runs at most once
		# and will run in the background thread, not blocking
		# or hanging blender
		# Internally also checks to see if auto-check enabled
		# and if the time interval has passed
		addon_updater_ops.check_for_update_background()


		layout.label(text="Demo Updater Addon")
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
	"""Demo bare-bones preferences"""
	bl_idname = __package__

	# addon updater preferences

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False,
		)
	updater_intrval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=7,
		min=0
		)
	updater_intrval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
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



# V-tools-2 classes import
from . Vtools2_generate_render_nodes       import Vtools2_generate_render_nodes_Operator
from . Vtools2_generate_render_nodes_panel import Vtools2_generate_render_nodes_Panel
from . Vtools2_view_layer_list             import ViewLayerListItem
from . Vtools2_view_layer_list             import ViewLayerUL_List
from . Vtools2_view_layer_list             import PT_ViewLayerListPanel
from . Vtools2_view_layer_list             import LIST_OT_ViewLayerListNewItem
from . Vtools2_view_layer_list             import LIST_OT_ViewLayerListDeleteItem
from . Vtools2_view_layer_list             import LIST_OT_ViewLayerListRefresh

classes = (
    OBJECT_PT_DemoUpdaterPanel,

    Vtools2_generate_render_nodes_Operator,
    Vtools2_generate_render_nodes_Panel
)

@persistent
def view_layer_list_refresh(scene):
    print('Refreshed list')
    bpy.ops.view_layer_list.refresh()

def register():
    # addon updater code and configurations
    # in case of broken version, try to register the updater first
    # so that users can revert back to a working version
    addon_updater_ops.register(bl_info)

    bpy.app.handlers.load_post.append(view_layer_list_refresh)

    bpy.utils.register_class(ViewLayerUL_List)
    bpy.utils.register_class(ViewLayerListItem)
    bpy.utils.register_class(PT_ViewLayerListPanel)
    bpy.utils.register_class(LIST_OT_ViewLayerListNewItem)
    bpy.utils.register_class(LIST_OT_ViewLayerListDeleteItem)
    bpy.utils.register_class(LIST_OT_ViewLayerListRefresh)
    
    bpy.types.Scene.view_layer_list = bpy.props.CollectionProperty(type = ViewLayerListItem)
    bpy.types.Scene.view_layer_list_index = bpy.props.IntProperty(name = "Index for view_layer_list", default = 0)
    

    # register the example panel, to show updater buttons
    for cls in classes:
        addon_updater_ops.make_annotations(cls) # to avoid blender 2.8 warnings
        bpy.utils.register_class(cls)

def unregister():
    del bpy.types.Scene.view_layer_list
    del bpy.types.Scene.view_layer_list_index
    
    bpy.app.handlers.load_post.remove(view_layer_list_refresh)

    bpy.utils.unregister_class(ViewLayerListItem)
    bpy.utils.unregister_class(ViewLayerUL_List)
    bpy.utils.unregister_class(PT_ViewLayerListPanel)
    bpy.utils.unregister_class(LIST_OT_ViewLayerListNewItem)
    bpy.utils.unregister_class(LIST_OT_ViewLayerListDeleteItem)
    bpy.utils.unregister_class(LIST_OT_ViewLayerListRefresh)

    # addon updater unregister
    addon_updater_ops.unregister()

    # register the example panel, to show updater buttons
    for cls in reversed(classes):
	    bpy.utils.unregister_class(cls)

