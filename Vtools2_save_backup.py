import bpy
import os

class VTOOLS2_OT_save_backup(bpy.types.Operator):
    '''Save a copy of the .blend file to the /backup folder, with timestamp.'''
    bl_idname = 'vtools.save_backup'
    bl_label = 'Save Backup'
    bl_options = {'REGISTER'}

    def execute(self, context):
        import time
        import datetime

        if bpy.path.abspath('//') != '':
            full_filename = bpy.path.basename(bpy.context.blend_data.filepath)
            filename = full_filename[:-6]

            timestamp_raw = time.time()
            timestamp = datetime.datetime.fromtimestamp(timestamp_raw).strftime('%Y-%m-%d_%H-%M')

            os.makedirs(bpy.path.abspath('//backup'), exist_ok = True)
            bpy.ops.wm.save_as_mainfile(filepath = bpy.path.abspath('//backup/' + filename + '_' + timestamp + '.blend'), copy = True, check_existing = True)

        else:
            self.report({'ERROR'}, 'You must save the .blend file first before making backups.')

        return {'FINISHED'}