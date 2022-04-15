import bpy

class VTOOLS2_OT_viewport_display(bpy.types.Operator):
    '''Object viewport display settings.'''
    bl_idname = 'vtools.viewport_display'
    bl_label = 'Viewport Display'
    bl_options = {'REGISTER', 'UNDO'}

    # Settings
    show_name : bpy.props.EnumProperty(
      name = 'Name',
      description = 'Object shows name in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_axis : bpy.props.EnumProperty(
      name = 'Axis',
      description = 'Object shows axis in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_wire : bpy.props.EnumProperty(
      name = 'Wire',
      description = 'Object shows wire in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_all_edges : bpy.props.EnumProperty(
      name = 'All Edges',
      description = 'Object shows all edges in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_texture_space : bpy.props.EnumProperty(
      name = 'Texture Space',
      description = 'Object shows texture space in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_shadows : bpy.props.EnumProperty(
      name = 'Shadows',
      description = 'Object shows shadows in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_in_front : bpy.props.EnumProperty(
      name = 'In Front',
      description = 'Object shows in front in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    show_bounds : bpy.props.EnumProperty(
      name = 'Bounds',
      description = 'Object shows as bounds in viewport.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'         , 1),
        ('True'         , 'True'          ,'Turn on.'                    , 'RADIOBUT_ON'  , 2),
        ('False'        , 'False'         ,'Turn off'                    , 'RADIOBUT_OFF' , 3)
      ]
    )
    display_bounds_type : bpy.props.EnumProperty(
      name = 'Bounds Type',
      description = 'Type of bounds drawing.',
      items = [
        #identifier        #name           #descript  #icon                                 #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'   , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'          , 1),
        ('BOX'          , 'BOX'           ,'Show as a cube.'             , 'MESH_CUBE'     , 2),
        ('SPHERE'       , 'SPHERE'        ,'Show as a sphere.'           , 'MESH_UVSPHERE' , 3),
        ('CYLINDER'     , 'CYLINDER'      ,'Show as a cylinder.'         , 'MESH_CYLINDER' , 4),
        ('CONE'         , 'CONE'          ,'Show as a cone.'             , 'MESH_CONE'     , 5),
        ('CAPSULE'      , 'CAPSULE'       ,'Show as a capsule.'          , 'MESH_CAPSULE'  , 6)
      ]
    )
    display_type : bpy.props.EnumProperty(
      name = 'Display Type',
      description = 'Object drawing type.',
      items = [
        #identifier        #name           #descript  #icon                                   #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'             , 'PANEL_CLOSE'     , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.' , 'FUND'            , 1),
        ('BOUNDS'       , 'BOUNDS'        ,'Show as bounds.'             , 'SHADING_BBOX'    , 2),
        ('WIRE'         , 'WIRE'          ,'Show as wire.'               , 'SHADING_WIRE'    , 3),
        ('SOLID'        , 'SOLID'         ,'Show as solid.'              , 'SHADING_SOLID'   , 4),
        ('TEXTURED'     , 'TEXTURED'      ,'Show as textured.'           , 'SHADING_TEXTURE' , 5)
      ]
    )
    color_use : bpy.props.EnumProperty(
      name = 'Color - Use',
      description = 'Choose whether to override color or not.',
      items = [
        #identifier        #name           #descript  #icon                                #ID
        ('Unchanged'    , 'Unchanged'     ,'Keep unchanged.'               , 'PANEL_CLOSE'  , 0),
        ('Copy Active'  , 'Copy Active'   ,'Copy from to Active object.'   , 'FUND'         , 1),
        ('Custom'       , 'Custom'        ,'Set the below selected color.' , 'EYEDROPPER'   , 2),
      ]
    )
    color : bpy.props.FloatVectorProperty(
        name = 'Object Color',
        description = 'Object color to set.',
        size = 4,
        min = 0,
        max = 1,
        subtype = 'COLOR',
        default = (0, 0, 0, 1)
    )
    

    def execute(self, context):

        def to_bool(string):
          if string.lower() == 'true':
            return True
          if string.lower() == 'false':
            return False

        active_object = bpy.context.active_object
        
        class object_data:
          def __init__(self, show_name, show_axis, show_all_edges, show_texture_space, show_shadows, show_in_front, color, display_type, show_bounds, display_bounds_type):
            self.show_name = show_name
            self.show_axis = show_axis
            self.show_all_edges = show_all_edges
            self.show_texture_space = show_texture_space
            self.show_shadows = show_shadows
            self.show_in_front = show_in_front
            self.color = color
            self.display_type = display_type
            self.show_bounds = show_bounds
            self.display_bounds_type = display_bounds_type

        if active_object is not None:
          original_active_data = object_data(
                        active_object.show_name,
                        active_object.show_axis,
                        active_object.show_all_edges,
                        active_object.show_texture_space,
                        active_object.display.show_shadows,
                        active_object.show_in_front,
                        active_object.color,
                        active_object.display_type,
                        active_object.show_bounds,
                        active_object.display_bounds_type,
                        )

          for obj in bpy.context.selected_objects:

            if self.show_name != 'Unchanged':
              if self.show_name != 'Copy Active':
                obj.show_name = to_bool(self.show_name)
              else:
                obj.show_name = original_active_data.show_name

            if self.show_axis != 'Unchanged':
              if self.show_axis != 'Copy Active':
                obj.show_axis = to_bool(self.show_axis)
              else:
                obj.show_axis = original_active_data.show_axis

            if self.show_all_edges != 'Unchanged':
              if self.show_all_edges != 'Copy Active':
                obj.show_all_edges = to_bool(self.show_all_edges)
              else:
                obj.show_all_edges = original_active_data.show_all_edges

            if self.show_texture_space != 'Unchanged':
              if self.show_texture_space != 'Copy Active':
                obj.show_texture_space = to_bool(self.show_texture_space)
              else:
                obj.show_texture_space = original_active_data.show_texture_space
            
            if self.show_shadows != 'Unchanged':
              if self.show_shadows != 'Copy Active':
                obj.display.show_shadows = to_bool(self.show_shadows)
              else:
                obj.display.show_shadows = original_active_data.show_shadows

            if self.show_in_front != 'Unchanged':
              if self.show_in_front != 'Copy Active':
                obj.show_in_front = to_bool(self.show_in_front)
              else:
                obj.show_in_front = original_active_data.show_in_front

            if self.show_bounds != 'Unchanged':
              if self.show_bounds != 'Copy Active':
                obj.show_bounds = to_bool(self.show_bounds)
              else:
                obj.show_bounds = original_active_data.show_bounds

            if self.display_type != 'Unchanged':
              if self.display_type != 'Copy Active':
                obj.display_type = self.display_type
              else:
                obj.display_type = original_active_data.display_type

            if self.display_bounds_type != 'Unchanged':
              if self.display_bounds_type != 'Copy Active':
                obj.display_bounds_type = self.display_bounds_type
              else:
                obj.coldisplay_bounds_typeor = original_active_data.display_bounds_type

            if self.color_use != 'Unchanged':
              if self.color_use != 'Copy Active':
                obj.color = self.color
              else:
                obj.color = original_active_data.color

        return {'FINISHED'}


