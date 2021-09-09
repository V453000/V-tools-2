import bpy

class VTOOLS2_OT_subsurf_settings(bpy.types.Operator):
  '''Change settings of all subsurf modifiers on selected objects.'''
  bl_idname = 'vtools.subsurf_settings'
  bl_label = 'Subsurf Settings'
  bl_options = {'REGISTER', 'UNDO'}


  subsurf_algorithm : bpy.props.EnumProperty(
    name = 'Mode',
    description = 'Subdivision Algorithm',
    items = [
      #identifier        #name           #descript  #icon         #ID
      ('Unchanged'    , 'Unchanged'     ,''      , 'PANEL_CLOSE' , 0),
      ('CATMULL_CLARK', 'Catmull-Clark' ,''      , 'MATSPHERE'   , 1),
      ('SIMPLE'       , 'Simple'        ,''      , 'MATCUBE'     , 2)
    ]
  )

  subsurf_render_visibility : bpy.props.EnumProperty(
    name = 'Render visibility',
    description = 'Render visibility',
    items = [
      #identifier      #name          #descript  #icon     #ID
      ('Unchanged'   , 'Unchanged'   ,''      , 'PANEL_CLOSE'   , 0),
      ('ON'          , 'ON'          ,''      , 'RESTRICT_RENDER_OFF'   , 1),
      ('OFF'         , 'OFF'         ,''      , 'RESTRICT_RENDER_ON'   , 2)
    ]
  )
  subsurf_viewport_visibility : bpy.props.EnumProperty(
    name = 'Viewport Visibility',
    description = 'Viewport Visibility',
    items = [
      #identifier      #name          #descript  #icon     #ID
      ('Unchanged'   , 'Unchanged'   ,''      , 'PANEL_CLOSE'   , 0),
      ('ON'          , 'ON'          ,''      , 'RESTRICT_VIEW_OFF'   , 1),
      ('OFF'         , 'OFF'         ,''      , 'RESTRICT_VIEW_ON'   , 2)
    ]
  )
  subsurf_editmode_visibility : bpy.props.EnumProperty(
    name = 'Edit Mode Visibility',
    description = 'Edit Mode Visibility',
    items = [
      #identifier      #name          #descript  #icon     #ID
      ('Unchanged'   , 'Unchanged'   ,''      , 'PANEL_CLOSE'   , 0),
      ('ON'          , 'ON'          ,''      , 'EDITMODE_HLT'   , 1),
      ('OFF'         , 'OFF'         ,''      , 'SNAP_VERTEX'   , 2)
    ]
  )
  subsurf_cage_visibility : bpy.props.EnumProperty(
    name = 'On Cage Visibility',
    description = 'On Cage Visibility',
    items = [
      #identifier      #name          #descript  #icon     #ID
      ('Unchanged'   , 'Unchanged'   ,''      , 'PANEL_CLOSE'   , 0),
      ('ON'          , 'ON'          ,''      , 'OUTLINER_DATA_MESH'   , 1),
      ('OFF'         , 'OFF'         ,''      , 'OUTLINER_DATA_EMPTY'   , 2)
    ]
  )
  
  subsurf_change_levels : bpy.props.BoolProperty(
    name = 'ChangeViewport Levels',
    default = False
  )
  subsurf_levels : bpy.props.IntProperty(
    name = 'Subsurf Levels',
    default = 1
  )

  subsurf_change_render_levels : bpy.props.BoolProperty(
    name = 'Change Render Levels',
    default = False
  )
  subsurf_render_levels : bpy.props.IntProperty(
    name = 'Subsurf Render Levels',
    default = 2
  )
  


  subsurf_adaptive_subdivision : bpy.props.BoolProperty(
    name = 'Adaptive Subdivision',
    default = False
  )
  subsurf_adaptive_subdivision : bpy.props.EnumProperty(
    name = 'Adaptive Subdivision',
    description = 'Adaptive Subdivision',
    items = [
      #identifier      #name          #descript  #icon     #ID
      ('Unchanged'   , 'Unchanged'   ,''      , 'PANEL_CLOSE'   , 0),
      ('ON'          , 'ON'          ,''      , 'PROP_ON'   , 1),
      ('OFF'         , 'OFF'         ,''      , 'PROP_OFF'   , 2)
    ]
  )


  subsurf_change_adaptive_dicing_rate : bpy.props.BoolProperty(
    name = 'Change Adaptive Dicing Rate',
    default = False
  )
  subsurf_adaptive_dicing_rate : bpy.props.FloatProperty(
    name = 'Adaptive Dicing Rate',
    default = 1.0
  )


  def execute(self, context):
    
    for obj in bpy.context.selected_objects:
      #bpy.context.scene.objects.active = obj
      subsurf_found = False

      if not obj.modifiers:
        print(obj.name + " has no modifiers")
      else:
        for modifier in obj.modifiers:
          if modifier.type == "SUBSURF":
            subsurf_found = True
            
            if self.subsurf_algorithm != 'Unchanged':
              modifier.subdivision_type = self.subsurf_algorithm

            if self.subsurf_render_visibility != 'Unchanged':
              if self.subsurf_render_visibility == 'ON':
                modifier.show_render =      True
              if self.subsurf_render_visibility == 'OFF':
                modifier.show_render =      False

            if self.subsurf_viewport_visibility != 'Unchanged':
              if self.subsurf_viewport_visibility == 'ON':
                modifier.show_viewport =    True
              if self.subsurf_viewport_visibility == 'OFF':
                modifier.show_viewport =    False

            if self.subsurf_editmode_visibility != 'Unchanged':
              if self.subsurf_editmode_visibility == 'ON':
                modifier.show_in_editmode = True
              if self.subsurf_editmode_visibility == 'OFF':
                modifier.show_in_editmode = False

            if self.subsurf_cage_visibility != 'Unchanged':
              if self.subsurf_cage_visibility == 'ON':
                modifier.show_on_cage =     True
              if self.subsurf_cage_visibility == 'OFF':
                modifier.show_on_cage =     False

            if self.subsurf_change_levels == True:
              modifier.levels =           self.subsurf_levels
            if self.subsurf_change_render_levels == True:
              modifier.render_levels =    self.subsurf_render_levels
         
          else:
            print("No Subsurf modifiers for " + obj.name)

      if subsurf_found == True:
        if self.subsurf_adaptive_subdivision != 'Unchanged':
          if self.subsurf_adaptive_subdivision == 'ON':
            obj.cycles.use_adaptive_subdivision = True
          if self.subsurf_adaptive_subdivision == 'OFF':
            obj.cycles.use_adaptive_subdivision = False
        
        if self.subsurf_change_adaptive_dicing_rate == True:
          obj.cycles.dicing_rate = self.subsurf_adaptive_dicing_rate

    return {'FINISHED'}