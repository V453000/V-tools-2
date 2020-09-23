import bpy

class VTOOLS2_OT_generate_render_nodes(bpy.types.Operator):
    '''Generating Compositor nodes automatically from View layer names'''
    bl_idname = 'vtools.generate_render_nodes'
    bl_label = 'Generate Render Nodes'
    bl_description = 'Generate Render Nodes from View Layers'
    bl_options = {'REGISTER', 'UNDO'}

    remove_existing_nodes = bpy.props.EnumProperty(
    name = 'Remove Existing Nodes',
    description = 'Choose whether the function should remove existing nodes, or only add new.',
    items = [
        #identifier   #name         #desc  #icon        #ID
        ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
        ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Regenerate'
    )
    regenerate_height_material = bpy.props.EnumProperty(
    name = 'Regenerate HEIGHT material',
    description = 'Delete the nodes in current HEIGHT material and create new ones.',
    items = [
        #identifier   #name         #desc  #icon        #ID
        ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
        ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
    )
    regenerate_shadow_shitter = bpy.props.EnumProperty(
    name = 'Regenerate Shadow Shitter',
    description = 'Delete the nodes in current SHADOW Shitter and create new ones.',
    items = [
        #identifier   #name         #desc  #icon        #ID
        ('Regenerate', 'Regenerate', '' ,  'CANCEL'     , 0),
        ('Keep'      , 'Keep'      , '' ,  'FILE_TICK'  , 1)
    ],
    default = 'Keep'
    )

    AO_identifier = bpy.props.StringProperty(
    name = 'AO Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering AO.',
    default = 'main'
    )
    shadow_identifier = bpy.props.StringProperty(
    name = 'Shadow Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Shadow.',
    default = 'shadow'
    )
    height_identifier = bpy.props.StringProperty(
    name = 'Height Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Height.',
    default = 'height'
    )
    Znormal_identifier = bpy.props.StringProperty(
    name = 'Z-Normal Identifier',
    description = 'Suffix or appendix in the name of RenderLayer for rendering Z-Normal.',
    default = 'Z-normal'
    )

    def execute(self, context):
        def generate_HEIGHT_material():
            # check if HEIGHT material exists and remember it
            if bpy.data.materials.get('HEIGHT') is None:
                height_material_existed = False
                bpy.data.materials.new('HEIGHT')
            else:
                height_material_existed = True
            
            heightmtl = bpy.data.materials['HEIGHT']
            heightmtl.use_nodes = True
            height_nodes = heightmtl.node_tree.nodes

            if self.regenerate_height_material == 'Regenerate' or height_material_existed == False:
                # remove existing height material nodes
                for node in height_nodes:
                    height_nodes.remove(node)
            
                # create new height material nodes
                geometry_node = height_nodes.new(type = 'ShaderNodeNewGeometry')
                geometry_node.name = 'HEIGHT-Geometry'
                geometry_node.label = geometry_node.name
                geometry_node.location = (-400,0)
                
                mapping_node = height_nodes.new(type = 'ShaderNodeMapping')
                mapping_node.name = 'HEIGHT-Mapping'
                mapping_node.label = mapping_node.name
                mapping_node.location = (-200,0)
                mapping_node.inputs[3].default_value[0] = 0.1

                separateXYZ_node = height_nodes.new(type = 'ShaderNodeSeparateXYZ')
                separateXYZ_node.name = 'HEIGHT-SeparateXYZ'
                separateXYZ_node.label = separateXYZ_node.name
                separateXYZ_node.location = (180,0)

                emission_node = height_nodes.new(type = 'ShaderNodeEmission')
                emission_node.name = 'HEIGHT-Emission'
                emission_node.label = emission_node.name
                emission_node.location = (380,0)

                material_output = height_nodes.new(type = 'ShaderNodeOutputMaterial')
                material_output.name = 'HEIGHT-MaterialOutput'
                material_output.label = material_output.name
                material_output.location = (580,0)

                # link height material nodes
                heightmtl.node_tree.links.new(geometry_node.outputs[0], mapping_node.inputs[0])
                heightmtl.node_tree.links.new(mapping_node.outputs[0], separateXYZ_node.inputs[0])
                heightmtl.node_tree.links.new(separateXYZ_node.outputs[2], emission_node.inputs[0])
                heightmtl.node_tree.links.new(emission_node.outputs[0], material_output.inputs[0])
            
        def generate_shadow_shitter():
            # destroy shadow shitter first, if set to 'Regenerate'
            if self.regenerate_shadow_shitter == 'Regenerate':
                if bpy.data.node_groups.get('ShadowShitter') is not None:
                    bpy.data.node_groups.remove(bpy.data.node_groups['ShadowShitter'])
            # check if shadow shitter exists, if not, create it
            if bpy.data.node_groups.get('ShadowShitter') is None:
                # create Shadow Shitter
                shadow_shitter = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = 'ShadowShitter')
                # add node group sockets
                shadow_shitter.inputs.new('NodeSocketColor', 'Shadow Pass')
                shadow_shitter.outputs.new('NodeSocketColor', 'Shadow')
                # add nodes
                input_node = shadow_shitter.nodes.new('NodeGroupInput')
                input_node.location = (-200,0)

                output_node = shadow_shitter.nodes.new('NodeGroupOutput')
                output_node.location = (600,0)
                
                alpha_over_node = shadow_shitter.nodes.new(type="CompositorNodeAlphaOver")
                alpha_over_node.name = 'ShadowShitter-alpha-over-node'
                alpha_over_node.label = 'ShadowShitter-alpha-over-node'
                alpha_over_node.location = (0,0)

                invert_node = shadow_shitter.nodes.new(type="CompositorNodeInvert")
                invert_node.name = 'ShadowShitter-invert-node'
                invert_node.label = 'ShadowShitter-invert-node'
                invert_node.location = (200,0)

                set_alpha_node = shadow_shitter.nodes.new(type="CompositorNodeSetAlpha")
                set_alpha_node.name = 'ShadowShitter-set-alpha-node'
                set_alpha_node.label = 'ShadowShitter-set-alpha-node'
                set_alpha_node.location = (400,0)

                # link shadow shitter nodes
                shadow_shitter.links.new(input_node.outputs[0], alpha_over_node.inputs[2])
                shadow_shitter.links.new(alpha_over_node.outputs[0], invert_node.inputs[1])
                shadow_shitter.links.new(invert_node.outputs[0], set_alpha_node.inputs[1])
                shadow_shitter.links.new(set_alpha_node.outputs[0], output_node.inputs[0])

        def remove_existing_nodes():
            if self.remove_existing_nodes == 'Regenerate':
                for node in bpy.context.scene.node_tree.nodes:
                    bpy.context.scene.node_tree.nodes.remove(node)

        def identify_view_layer(view_layer_name):
            AO_identifier      = '-' + self.AO_identifier
            shadow_identifier  = '-' + self.shadow_identifier
            height_identifier  = '-' + self.height_identifier
            Znormal_identifier = '-' + self.Znormal_identifier

            view_layer_appendix_AO      = view_layer_name[-len(AO_identifier):]
            view_layer_appendix_shadow  = view_layer_name[-len(shadow_identifier):]
            view_layer_appendix_height  = view_layer_name[-len(height_identifier):]
            view_layer_appendix_Znormal = view_layer_name[-len(Znormal_identifier):]

            if view_layer_appendix_AO == AO_identifier:
                view_layer_type = self.AO_identifier
            elif view_layer_appendix_shadow == shadow_identifier:
                view_layer_type = self.shadow_identifier
            elif view_layer_appendix_height == height_identifier:
                view_layer_type = self.height_identifier
            elif  view_layer_appendix_Znormal == Znormal_identifier:
                view_layer_type = self.Znormal_identifier
            else:
                view_layer_type = ''

            return view_layer_type




        # basic settings
        bpy.context.scene.use_nodes = True
        # generate HEIGHT material (if settings allow)
        generate_HEIGHT_material()
        # generate Z-normal material (if settings allow)
        # generate Normal material (if settings allow)
        # generate ShadowShitter material (if settings allow)
        generate_shadow_shitter()

        # set material override on view layers that need it
        # set shadow pass on shadow view layers
        
        # remove existing nodes (if settings allow)
        remove_existing_nodes()
        
        # generate compositor nodes
        output_folder = '//OUTPUT\\'
        nodes = bpy.context.scene.node_tree.nodes
        x_multiplier = 300
        y_multiplier = -680
        y_count = 0
        for viewlayer in bpy.context.scene.view_layers:
            view_layer_type = identify_view_layer(viewlayer.name)
            x_count = 0

            # view layer node
            input_node = nodes.new('CompositorNodeRLayers')
            input_node.name = 'view-layer-' + viewlayer.name
            input_node.label = input_node.name
            input_node.location = (x_count * x_multiplier, y_count * y_multiplier)
            input_node.width = x_multiplier - 30
            input_node.scene = bpy.context.scene
            input_node.layer = viewlayer.name

            x_count += 2

            output_node = nodes.new('CompositorNodeOutputFile')
            output_node.name = 'file-output-' + viewlayer.name
            output_node.label = output_node.name
            output_node.location = (x_count*x_multiplier, y_count*y_multiplier)
            output_node.width = x_multiplier -30 + 150

            output_node.base_path = output_folder + bpy.context.scene.name + '\\' + bpy.context.scene.name + '_' + viewlayer.name
            
            # remove output node default input socket
            output_node.file_slots.remove(output_node.inputs[0])
            # add output node input socket
            output_node.file_slots.new(bpy.context.scene.name + '_' + viewlayer.name + '_')

            
            if view_layer_type == self.shadow_identifier:
                viewlayer.use_pass_shadow = True
                shadow_shitter = nodes.new('CompositorNodeGroup')
                shadow_shitter.node_tree = bpy.data.node_groups['ShadowShitter']
                shadow_shitter.name = viewlayer.name + '-ShadowShitter'
                shadow_shitter.label = shadow_shitter.name
                x_count -= 1
                shadow_shitter.location = (x_count*x_multiplier, y_count*y_multiplier)
                x_count += 1
                shadow_shitter.width = x_multiplier - 30

                index_shadow = input_node.outputs.find('Shadow')

                bpy.context.scene.node_tree.links.new(input_node.outputs[index_shadow], shadow_shitter.inputs[0])
                bpy.context.scene.node_tree.links.new(shadow_shitter.outputs[0], output_node.inputs[0])

            elif view_layer_type == self.height_identifier:
                viewlayer.material_override = bpy.data.materials['HEIGHT']
                height_alpha_over_black_node = bpy.context.scene.node_tree.nodes.new('CompositorNodeAlphaOver')
                height_alpha_over_black_node.name = viewlayer.name + '-Alpha-Over-Black'
                height_alpha_over_black_node.label = height_alpha_over_black_node.name
                height_alpha_over_black_node.location = ( input_node.location[0] + x_multiplier, input_node.location[1])
                height_alpha_over_black_node.width = x_multiplier - 30
                height_alpha_over_black_node.inputs[1].default_value = (0, 0, 0, 1)

                bpy.context.scene.node_tree.links.new(input_node.outputs[0], height_alpha_over_black_node.inputs[2])
                bpy.context.scene.node_tree.links.new(height_alpha_over_black_node.outputs[0], output_node.inputs[0])

            else:
                if view_layer_type == self.AO_identifier:
                    viewlayer.use_pass_ambient_occlusion = True
                    output_node_AO = nodes.new('CompositorNodeOutputFile')
                    output_node_AO.name = 'file-output-' + viewlayer.name + '-AO'
                    output_node_AO.label = 'file-output-' + viewlayer.name + '-AO'
                    output_node_AO.location = (x_count*x_multiplier, y_count*y_multiplier - 140 - 180)
                    output_node_AO.width = x_multiplier-30+150

                    output_node_AO.file_slots.remove(output_node_AO.inputs[0])
                    output_node_AO.file_slots.new(bpy.context.scene.name + '_' + viewlayer.name + '-AO' + '_')

                    output_node_AO.base_path = output_folder + bpy.context.scene.name + '\\' + bpy.context.scene.name + '_' + viewlayer.name + '-AO'

                    index_AO = input_node.outputs.find('AO')
                    bpy.context.scene.node_tree.links.new(input_node.outputs[index_AO], output_node_AO.inputs[0])

                # main output link
                bpy.context.scene.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])

            y_count += 1

            

            
            
            





        return {'FINISHED'}