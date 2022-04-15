import bpy

class VTOOLS2_OT_ray_visibility(bpy.types.Operator):
    '''Object settings of viewport and ray visibilities.'''
    bl_idname = 'vtools.ray_visibility'
    bl_label = 'Ray visibility'
    bl_options = {'REGISTER', 'UNDO'}

    # Settings
    hide_select : bpy.props.EnumProperty(
      name = 'Selectable',
      description = 'Object is selectable.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('False'        , 'Allow'         ,'Turn on.'                    , 'RESTRICT_SELECT_OFF', 2),
        ('True'         , 'Disallow'      ,'Turn off'                    , 'RESTRICT_SELECT_ON' , 3)
      ]
    )
    hide_viewport : bpy.props.EnumProperty(
      name = 'Viewports',
      description = 'Show object in viewports.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('False'        , 'Show'          ,'Show'                        , 'RESTRICT_VIEW_OFF', 2),
        ('True'         , 'Hide'          ,'Hide'                        , 'RESTRICT_VIEW_ON' , 3)
      ]
    )
    hide_render : bpy.props.EnumProperty(
      name = 'Renders',
      description = 'Object affects diffuse.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('False'        , 'Show'          ,'Show'                        , 'RESTRICT_RENDER_OFF', 2),
        ('True'         , 'Hide'          ,'Hide'                        , 'RESTRICT_RENDER_ON' , 3)
      ]
    )
    is_shadow_catcher : bpy.props.EnumProperty(
      name = 'Shadow Catcher',
      description = 'Object becomes a shadow catcher.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    is_holdout : bpy.props.EnumProperty(
      name = 'Holdout',
      description = 'Object becomes holdout.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )

    visible_camera : bpy.props.EnumProperty(
      name = 'Camera',
      description = 'Object is visible to camera directly.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    visible_diffuse : bpy.props.EnumProperty(
      name = 'Diffuse',
      description = 'Object affects diffuse.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    visible_glossy : bpy.props.EnumProperty(
      name = 'Glossy',
      description = 'Object affects glossy.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    visible_transmission : bpy.props.EnumProperty(
      name = 'Transmission',
      description = 'Object affects transmission.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    visible_volume_scatter : bpy.props.EnumProperty(
      name = 'Volume scatter',
      description = 'Object affects volume scatter.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    visible_shadow : bpy.props.EnumProperty(
      name = 'Shadow',
      description = 'Object casts shadows.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    
    

    def execute(self, context):

        def to_bool(string):
          if string.lower() == 'true':
            return True
          if string.lower() == 'false':
            return False

        active_object = bpy.context.active_object
        render_engine = bpy.context.scene.render.engine
        if render_engine != 'CYCLES':
          self.report({"INFO"}, "V-tools-2: Ray Visibility: Cycles isn't enabled, non-cycles settings won't take effect.")
        
        class object_data:
          def __init__(self, hide_select, hide_viewport, hide_render, is_shadow_catcher, is_holdout, visible_camera, visible_diffuse, visible_glossy, visible_transmission, visible_volume_scatter, visible_shadow):
            self.hide_select            = hide_select
            self.hide_viewport          = hide_viewport
            self.hide_render            = hide_render
            self.is_shadow_catcher      = is_shadow_catcher
            self.is_holdout             = is_holdout
            self.visible_camera         = visible_camera
            self.visible_diffuse        = visible_diffuse
            self.visible_glossy         = visible_glossy
            self.visible_transmission   = visible_transmission
            self.visible_volume_scatter = visible_volume_scatter
            self.visible_shadow         = visible_shadow

        if active_object is not None:
          original_active_data = object_data(
                        active_object.hide_select,
                        active_object.hide_viewport,
                        active_object.hide_render,
                        active_object.is_shadow_catcher,
                        active_object.is_holdout,
                        active_object.visible_camera,
                        active_object.visible_diffuse,
                        active_object.visible_glossy,
                        active_object.visible_transmission,
                        active_object.visible_volume_scatter,
                        active_object.visible_shadow,
                        )

          for obj in bpy.context.selected_objects:

            if self.hide_select != 'Unchanged':
              if self.hide_select != 'Copy Active':
                obj.hide_select = to_bool(self.hide_select)
              else:
                obj.hide_select = original_active_data.hide_select

            if self.hide_viewport != 'Unchanged':
              if self.hide_viewport != 'Copy Active':
                obj.hide_viewport = to_bool(self.hide_viewport)
              else:
                obj.hide_viewport = original_active_data.hide_viewport

            if self.hide_render != 'Unchanged':
              if self.hide_render != 'Copy Active':
                obj.hide_render = to_bool(self.hide_render)
              else:
                obj.hide_render = original_active_data.hide_render

            if render_engine == 'CYCLES':
              if self.is_shadow_catcher != 'Unchanged':
                if self.is_shadow_catcher != 'Copy Active':
                  obj.is_shadow_catcher = to_bool(self.is_shadow_catcher)
                else:
                  obj.is_shadow_catcher = original_active_data.is_shadow_catcher

            if self.is_holdout != 'Unchanged':
              if self.is_holdout != 'Copy Active':
                obj.is_holdout = to_bool(self.is_holdout)
              else:
                obj.is_holdout = original_active_data.is_holdout

            if render_engine == 'CYCLES':
              if self.visible_camera != 'Unchanged':
                if self.visible_camera != 'Copy Active':
                  obj.visible_camera = to_bool(self.visible_camera)
                else:
                  obj.visible_camera = original_active_data.visible_camera

              if self.visible_diffuse != 'Unchanged':
                if self.visible_diffuse != 'Copy Active':
                  obj.visible_diffuse = to_bool(self.visible_diffuse)
                else:
                  obj.visible_diffuse = original_active_data.visible_diffuse

              if self.visible_glossy != 'Unchanged':
                if self.visible_glossy != 'Copy Active':
                  obj.visible_glossy = to_bool(self.visible_glossy)
                else:
                  obj.visible_glossy = original_active_data.visible_glossy

              if self.visible_transmission != 'Unchanged':
                if self.visible_transmission != 'Copy Active':
                  obj.visible_transmission = to_bool(self.visible_transmission)
                else:
                  obj.visible_transmission = original_active_data.visible_transmission

              if self.visible_volume_scatter != 'Unchanged':
                if self.visible_volume_scatter != 'Copy Active':
                  obj.visible_volume_scatter = to_bool(self.visible_volume_scatter)
                else:
                  obj.visible_volume_scatter = original_active_data.visible_volume_scatter

              if self.visible_shadow != 'Unchanged':
                if self.visible_shadow != 'Copy Active':
                  obj.visible_shadow = to_bool(self.visible_shadow)
                else:
                  obj.visible_shadow = original_active_data.visible_shadow

        return {'FINISHED'}


