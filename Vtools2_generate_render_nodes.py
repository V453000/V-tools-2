import bpy

class Vtools2_generate_render_nodes_Operator(bpy.types.Operator):
    bl_idname = 'scene.generate_render_nodes'
    bl_label = 'Generate Render Nodes'
    bl_description = 'Generate Render Nodes from View Layers'

    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_center()
        return {'FINISHED'}