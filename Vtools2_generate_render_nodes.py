import bpy

class Vtools2_generate_render_nodes_Operator(bpy.types.Operator):
    bl_idname = 'scene.generate_render_nodes'
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
                shadow_shitter.inputs.new('NodeSocketFloat', 'Shadow Pass')
                shadow_shitter.outputs.new('NodeSocketFloat', 'Shadow')
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


        return {'FINISHED'}