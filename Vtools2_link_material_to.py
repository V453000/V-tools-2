import bpy
import os

class VTOOLS2_OT_link_material_to(bpy.types.Operator):
  '''Choose whether materials should be linked to selected Objects or their Mesh data.'''
  bl_idname = 'vtools.link_material_to'
  bl_label = 'Link material to...'
  bl_options = {'REGISTER', 'UNDO'}

  set_mode = bpy.props.EnumProperty(
    name = 'Material Linking',
    description = 'Select what to link the material to.',
    items = [
      ('OBJECT', 'OBJECT',''),
      ('DATA'  , 'DATA','')
    ]
  )

  def execute(self,context):

    for obj in bpy.context.selected_objects:
      if obj.type == 'MESH':
        if obj.data.materials:
          slot_count = len(obj.material_slots)

          obj_material_list = []
          for slot_number in range(0, slot_count):
            obj_material_list.append(obj.material_slots[slot_number].material.name)
              
          for slot_number in range(0, slot_count):
            obj.material_slots[slot_number].link = self.set_mode
            obj.material_slots[slot_number].material = bpy.data.materials[obj_material_list[slot_number]]

    return {'FINISHED'}