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
    use_Z_pass = bpy.props.BoolProperty(
    name = 'use_Z',
    description = 'Use Z/Depth pass in all View Layers that have it enabled.',
    default = False
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
                mapping_node.inputs[3].default_value[2] = 0.1

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

            view_layer_appendix_AO      = view_layer_name[-len(AO_identifier):]
            view_layer_appendix_shadow  = view_layer_name[-len(shadow_identifier):]
            view_layer_appendix_height  = view_layer_name[-len(height_identifier):]

            if view_layer_appendix_AO == AO_identifier:
                view_layer_type = self.AO_identifier
            elif view_layer_appendix_shadow == shadow_identifier:
                view_layer_type = self.shadow_identifier
            elif view_layer_appendix_height == height_identifier:
                view_layer_type = self.height_identifier
            else:
                view_layer_type = ''

            return view_layer_type

        def handle_special_pass(pass_name, socket_name, input_node):
            print(input_node.name, pass_name)
            # create output node
            pass_output_node = nodes.new('CompositorNodeOutputFile')
            pass_output_node.name = 'file-output-' + viewlayer.name + pass_name
            pass_output_node.label = pass_output_node.name
            pass_output_node.location = (input_node.location[0] + 1500, input_node.location[1] - (output_extra_height * output_extra_height_multiplier)) 
            pass_output_node.width = x_multiplier - 30 + 150 + 150
            pass_output_node.base_path = output_folder + scn.name + '\\' + scn.name + '_' + viewlayer.name + '_' + pass_name

            # clear file slots and add a new one
            pass_output_node.file_slots.remove(pass_output_node.inputs[0])
            pass_output_node.file_slots.new(scn.name + '_' + viewlayer.name + '_' + pass_name + '_')

            # find index of special pass
            pass_index = input_node.outputs.find(socket_name)

            # create links
            scn.node_tree.links.new(input_node.outputs[pass_index], pass_output_node.inputs[0])




        # basic settings
        bpy.context.scene.use_nodes = True
        # generate HEIGHT material (if settings allow)
        generate_HEIGHT_material()
        # generate Normal material (if settings allow)
        # generate ShadowShitter material (if settings allow)
        generate_shadow_shitter()

        # set material override on view layers that need it
        # set shadow pass on shadow view layers
        
        # remove existing nodes (if settings allow)
        remove_existing_nodes()
        
        # generate compositor nodes
        scn = bpy.context.scene
        output_folder = '//OUTPUT\\'
        nodes = scn.node_tree.nodes
        x_multiplier = 300
        y_multiplier = -680
        y_count = 0
        for viewlayer in scn.view_layers:
            viewlayer.samples = 0
            view_layer_type = identify_view_layer(viewlayer.name)
            x_count = 0

            # view layer node
            input_node = nodes.new('CompositorNodeRLayers')
            input_node.name = 'view-layer-' + viewlayer.name
            input_node.label = input_node.name
            input_node.location = (x_count * x_multiplier, y_count * y_multiplier)
            input_node.width = x_multiplier - 30
            input_node.scene = scn
            input_node.layer = viewlayer.name

            x_count += 2

            output_node = nodes.new('CompositorNodeOutputFile')
            output_node.name = 'file-output-' + viewlayer.name
            output_node.label = output_node.name
            output_node.location = (x_count*x_multiplier, y_count*y_multiplier)
            output_node.width = x_multiplier -30 + 150

            output_node.base_path = output_folder + scn.name + '\\' + scn.name + '_' + viewlayer.name
            
            # remove output node default input socket
            output_node.file_slots.remove(output_node.inputs[0])
            # add output node input socket
            output_node.file_slots.new(scn.name + '_' + viewlayer.name + '_')

            
            if view_layer_type == self.shadow_identifier:
                viewlayer.use_pass_shadow = True
                viewlayer.samples = 128
                shadow_shitter = nodes.new('CompositorNodeGroup')
                shadow_shitter.node_tree = bpy.data.node_groups['ShadowShitter']
                shadow_shitter.name = viewlayer.name + '-ShadowShitter'
                shadow_shitter.label = shadow_shitter.name
                x_count -= 1
                shadow_shitter.location = (x_count*x_multiplier, y_count*y_multiplier)
                x_count += 1
                shadow_shitter.width = x_multiplier - 30

                index_shadow = input_node.outputs.find('Shadow')

                scn.node_tree.links.new(input_node.outputs[index_shadow], shadow_shitter.inputs[0])
                scn.node_tree.links.new(shadow_shitter.outputs[0], output_node.inputs[0])

            elif view_layer_type == self.height_identifier:
                viewlayer.material_override = bpy.data.materials['HEIGHT']
                viewlayer.samples = 128
                height_alpha_over_black_node = scn.node_tree.nodes.new('CompositorNodeAlphaOver')
                height_alpha_over_black_node.name = viewlayer.name + '-Alpha-Over-Black'
                height_alpha_over_black_node.label = height_alpha_over_black_node.name
                height_alpha_over_black_node.location = ( input_node.location[0] + x_multiplier, input_node.location[1])
                height_alpha_over_black_node.width = x_multiplier - 30
                height_alpha_over_black_node.inputs[1].default_value = (0, 0, 0, 1)

                scn.node_tree.links.new(input_node.outputs[0], height_alpha_over_black_node.inputs[2])
                scn.node_tree.links.new(height_alpha_over_black_node.outputs[0], output_node.inputs[0])

            else:
                if view_layer_type == self.AO_identifier:
                    viewlayer.use_pass_ambient_occlusion = True
                    output_node_AO = nodes.new('CompositorNodeOutputFile')
                    output_node_AO.name = 'file-output-' + viewlayer.name + '-AO'
                    output_node_AO.label = 'file-output-' + viewlayer.name + '-AO'
                    output_node_AO.location = (x_count*x_multiplier, y_count*y_multiplier - 140 - 180)
                    output_node_AO.width = x_multiplier-30+150

                    output_node_AO.file_slots.remove(output_node_AO.inputs[0])
                    output_node_AO.file_slots.new(scn.name + '_' + viewlayer.name + '-AO' + '_')

                    output_node_AO.base_path = output_folder + scn.name + '\\' + scn.name + '_' + viewlayer.name + '-AO'

                    index_AO = input_node.outputs.find('AO')
                    scn.node_tree.links.new(input_node.outputs[index_AO], output_node_AO.inputs[0])

                # main output link
                scn.node_tree.links.new(input_node.outputs[0], output_node.inputs[0])

            special_pass_args = [
                # data path                                  # pass name                          # socket name           
                (viewlayer.use_pass_z                      , 'pass-z'                             , 'Depth'               ),
                (viewlayer.use_pass_mist                   , 'pass-mist'                          , 'Mist'                ),
                (viewlayer.use_pass_normal                 , 'pass-normal'                        , 'Normal'              ),
                (viewlayer.use_pass_vector                 , 'pass-vector'                        , 'Vector'              ),
                (viewlayer.use_pass_uv                     , 'pass-uv'                            , 'UV'                  ),
                (viewlayer.use_pass_object_index           , 'pass-object-index'                  , 'IndexOB'             ),
                (viewlayer.use_pass_material_index         , 'pass-material-index'                , 'IndexMA'             ),
                (viewlayer.use_pass_diffuse_direct         , 'pass-diffuse-direct'                , 'DiffDir'             ),
                (viewlayer.use_pass_diffuse_indirect       , 'pass-diffuse-indirect'              , 'DiffInd'             ),
                (viewlayer.use_pass_diffuse_color          , 'pass-diffuse-color'                 , 'DiffCol'             ),
                (viewlayer.use_pass_glossy_direct          , 'pass-glossy-direct'                 , 'GlossDir'            ),
                (viewlayer.use_pass_glossy_indirect        , 'pass-glossy-indirect'               , 'GlossInd'            ),
                (viewlayer.use_pass_glossy_color           , 'pass-glossy-color'                  , 'GlossCol'            ),
                (viewlayer.use_pass_transmission_direct    , 'pass-transmission-direct'           , 'TransDir'            ),
                (viewlayer.use_pass_transmission_indirect  , 'pass-transmission-indirect'         , 'TransInd'            ),
                (viewlayer.use_pass_transmission_color     , 'pass-transmission-color'            , 'TransCol'            ),
                #(viewlayer.use_pass_subsurface_direct      , 'pass-subsurface-direct'             , ''                   ), #I think this isn't in cycles
                #(viewlayer.use_pass_subsurface_indirect    , 'pass-subsurface-indirect'           , ''                   ), #I think this isn't in cycles
                #(viewlayer.use_pass_subsurface_color       , 'pass-subsurface-color'              , ''                   ), #I think this isn't in cycles
                (viewlayer.use_pass_emit                   , 'pass-emit'                          , 'Emit'                ),
                (viewlayer.use_pass_environment            , 'pass-environment'                   , 'Env'                 ),                
                (viewlayer.cycles.use_pass_volume_direct   , 'pass-volume-direct'                 , 'VolumeDir'           ),
                (viewlayer.cycles.use_pass_volume_indirect , 'pass-volume-indirect'               , 'VolumeInd'           ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-noisy-image'         , 'Noisy Image'         ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-normal'    , 'Denoising Normal'    ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-albedo'    , 'Denoising Albedo'    ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-depth'     , 'Denoising Depth'     ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-shadowing' , 'Denoising Shadowing' ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-variance'  , 'Denoising Variance'  ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-intensity' , 'Denoising Intensity' ),
                (viewlayer.cycles.denoising_store_passes   , 'pass-denoising-denoising-clean'     , 'Denoising Clean'     ),
            ]

            if view_layer_type != self.shadow_identifier and view_layer_type != self.height_identifier:
                # if the pass isn't shadow or height, try to check for extra things to output
                output_extra_height = 110
                output_extra_height_multiplier = 0

                for args in special_pass_args:
                    pass_enabled = args[0]
                    pass_name    = args[1]
                    socket_name  = args[2]
                    

                    print(viewlayer.name, pass_name, pass_enabled)
                    if pass_enabled == True:
                        if pass_name != 'pass-z' or self.use_Z_pass == True:
                            print(pass_name, 'is enabled.')
                            handle_special_pass(pass_name, socket_name, input_node)
                            
                            output_extra_height_multiplier += 1


            # handle AOV outputs
            x_count += 2

            aov_node_y = 120
            aov_node_y_multiplier = 0

            for aov in viewlayer.aovs:
                aov_output_node = nodes.new('CompositorNodeOutputFile')
                aov_output_node.name = 'file-output-' + viewlayer.name + '_AOV_' + aov.name
                aov_output_node.label = aov_output_node.name
                aov_output_node.location = (input_node.location[0] + 2000+160, y_count*y_multiplier - aov_node_y * aov_node_y_multiplier)
                aov_output_node.width = x_multiplier -30 + 150
                
                aov_output_node.base_path = output_folder + scn.name + '\\' + scn.name + '_' + viewlayer.name + '_' + 'AOV-' + aov.name

                aov_output_node.file_slots.remove(aov_output_node.inputs[0])
                aov_output_node.file_slots.new(scn.name + '_' + viewlayer.name + '_' + 'AOV-' + aov.name + '_')

                aov_output_index = input_node.outputs.find(aov.name)

                scn.node_tree.links.new(input_node.outputs[aov_output_index], aov_output_node.inputs[0])

                aov_node_y_multiplier += 1

            y_count += 1


        return {'FINISHED'}