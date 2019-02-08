# Downloaded from: https://github.com/netri/blender_neitri_tools


bl_info = {
    "name": "Neitri's Tools",
    "author": "Neitri",
    "version": (1, 1, 0),
    "blender": (2, 80, 0),
    "description": "Delete Zero Weight Bones and Vertex Groups, Delete Bones Constraints, Delete Bone and Add Weights To Parent",
    "location": "Space Menu",
    "warning": "",
    "wiki_url": "https://github.com/netri/blender_neitri_tools",
    "category": "Object"
}


import bpy



class NT_OT_OperatorBase(bpy.types.Operator):

    def optionallySelectBones(self):

        armature = bpy.context.object
        if armature is None:
            self.report({"ERROR"}, "Select something")
            return {"CANCELLED"}

        # find armature, try to select parent
        if armature is not None and armature.type != "ARMATURE" and armature.parent is not None:
            armature = armature.parent
            if armature is not None and armature.type != "ARMATURE" and armature.parent is not None:    
                armature = armature.parent

        # find armature, try to select first and only child
        if armature is not None and armature.type != "ARMATURE" and len(armature.children) == 1:
            armature = armature.children[0]
            if armature is not None and armature.type != "ARMATURE" and len(armature.children) == 1:
                armature = armature.children[0]

        if armature is None or armature.type != "ARMATURE":           
            self.report({"ERROR"}, "Select armature, it's child or it's parent")
            return {"CANCELLED"}

        # find which bones to work on
        if bpy.context.selected_editable_bones is not None and len(bpy.context.selected_editable_bones) > 0:
            bones_to_work_on = bpy.context.selected_editable_bones
        elif bpy.context.selected_pose_bones is not None and len(bpy.context.selected_pose_bones) > 0:
            bones_to_work_on = bpy.context.selected_pose_bones
        else:
            bones_to_work_on = armature.data.bones
        bone_names_to_work_on = set([bone.name for bone in bones_to_work_on]) # grab names only 

        self._armature = armature
        self._bone_names_to_work_on = bone_names_to_work_on
        self._objects_to_work_on = armature.children


    def mustSelectBones(self):

        armature = bpy.context.object

        if armature is None or armature.type != "ARMATURE":           
            self.report({"ERROR"}, "Select bones in armature edit or pose mode")
            return {"CANCELLED"}

        # find which bones to work on
        if bpy.context.selected_editable_bones is not None and len(bpy.context.selected_editable_bones) > 0:
            bones_to_work_on = bpy.context.selected_editable_bones
        else:
            bones_to_work_on = bpy.context.selected_pose_bones
        bone_names_to_work_on = set([bone.name for bone in bones_to_work_on]) # grab names only

        if len(bone_names_to_work_on) == 0:
            self.report({"ERROR"}, "Select at least one bone")
            return {"CANCELLED"}  

        self._armature = armature
        self._bone_names_to_work_on = bone_names_to_work_on
        self._objects_to_work_on = armature.children




class ArmatureEditMode:

    def __init__(self, armature):
        # save user state, select armature, go to armature edit mode
        self._armature = armature
        self._active_object = bpy.context.view_layer.objects.active 
        bpy.context.view_layer.objects.active = self._armature
        self._armature_hide = self._armature.hide_viewport
        self._armature.hide_viewport = False
        self._armature_mode = self._armature.mode
        bpy.ops.object.mode_set(mode="EDIT")

    def restore(self):
        # restore user state
        bpy.ops.object.mode_set(mode=self._armature_mode)
        self._armature.hide_viewport = self._armature_hide
        bpy.context.view_layer.objects.active  = self._active_object




class DeleteZeroWeightBonesAndVertexGroups(NT_OT_OperatorBase):

    bl_idname = "neitri_tools.delete_zero_weight_bones_and_vertex_groups"
    bl_label = "Delete Zero Weight Bones and Vertex Groups"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        error = self.optionallySelectBones()
        if error:
            return error

        armature_edit_mode = ArmatureEditMode(self._armature)

        # create lookup table
        bone_name_to_edit_bone = dict()
        for edit_bone in self._armature.data.edit_bones:
            bone_name_to_edit_bone[edit_bone.name] = edit_bone

        # figure out which bones we can delete
        vertex_group_names_used = set()
        vertex_group_name_to_objects_having_same_named_vertex_group = dict()
        for object in self._objects_to_work_on:
            vertex_group_id_to_vertex_group_name = dict()
            for vertex_group in object.vertex_groups:               
                vertex_group_id_to_vertex_group_name[vertex_group.index] = vertex_group.name
                if not vertex_group.name in vertex_group_name_to_objects_having_same_named_vertex_group:
                    vertex_group_name_to_objects_having_same_named_vertex_group[vertex_group.name] = set()    
                vertex_group_name_to_objects_having_same_named_vertex_group[vertex_group.name].add(object)                
            for vertex in object.data.vertices:
                for group in vertex.groups:
                    if group.weight > 0:
                        vertex_group_names_used.add(vertex_group_id_to_vertex_group_name[group.group])

        not_used_bone_names = self._bone_names_to_work_on - vertex_group_names_used

        for bone_name in not_used_bone_names:
            self._armature.data.edit_bones.remove(bone_name_to_edit_bone[bone_name]) # delete bone
            if bone_name in vertex_group_name_to_objects_having_same_named_vertex_group:
                for objects in vertex_group_name_to_objects_having_same_named_vertex_group[bone_name]: # delete vertex groups
                    vertex_group = object.vertex_groups.get(bone_name)
                    if vertex_group is not None:
                        object.vertex_groups.remove(vertex_group)

        armature_edit_mode.restore()

        self.report({"INFO"}, "Deleted " + str(len(not_used_bone_names)) + " zero weight bones")

        return {"FINISHED"}




class DeleteBonesConstraints(NT_OT_OperatorBase):

    bl_idname = "neitri_tools.delete_bones_constraints"
    bl_label = "Delete Bones Constraints"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        error = self.optionallySelectBones()
        if error:
            return error

        armature_edit_mode = ArmatureEditMode(self._armature)

        bone_name_to_pose_bone = dict()
        for bone in self._armature.pose.bones:
            bone_name_to_pose_bone[bone.name] = bone

        bones_worked_on = 0
        constraints_deleted = 0

        for bone_name in self._bone_names_to_work_on:
            bone = bone_name_to_pose_bone[bone_name]
            if len(bone.constraints) > 0:
                bones_worked_on += 1
                for constraint in bone.constraints:
                    bone.constraints.remove(constraint)
                    constraints_deleted += 1

        armature_edit_mode.restore()

        self.report({"INFO"}, "Deleted " + str(constraints_deleted) + " constraints on " + str(bones_worked_on) + " bones")

        return {"FINISHED"}




class DeleteBoneAndAddWeightsToParent(NT_OT_OperatorBase):

    bl_idname = "neitri_tools.delete_bone_and_add_weights_to_parent"
    bl_label = "Delete Bone and Add Weights To Parent"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        error = self.mustSelectBones()
        if error:
            return error

        armature_edit_mode = ArmatureEditMode(self._armature)

        # create lookup table
        bone_name_to_edit_bone = dict()
        for edit_bone in self._armature.data.edit_bones:
            bone_name_to_edit_bone[edit_bone.name] = edit_bone

        for bone_name_to_remove in self._bone_names_to_work_on:

            bone_name_to_add_weights_to = bone_name_to_edit_bone[bone_name_to_remove].parent.name        
            self._armature.data.edit_bones.remove(bone_name_to_edit_bone[bone_name_to_remove]) # delete bone

            for object in self._objects_to_work_on:

                vertex_group_to_remove = object.vertex_groups.get(bone_name_to_remove)
                vertex_group_to_add_weights_to = object.vertex_groups.get(bone_name_to_add_weights_to)

                if vertex_group_to_remove is not None:
                    
                    if vertex_group_to_add_weights_to is None:
                        vertex_group_to_add_weights_to = object.vertex_groups.add(bone_name_to_add_weights_to)

                    for vertex in object.data.vertices: # transfer weight for each vertex                        
                            weight_to_transfer = 0
                            for group in vertex.groups:
                                if group.group == vertex_group_to_remove.index:
                                    weight_to_transfer = group.weight
                                    break
                            if weight_to_transfer > 0:
                                vertex_group_to_add_weights_to.add([vertex.index], weight_to_transfer, "ADD")

                    object.vertex_groups.remove(vertex_group_to_remove) # delete vertex group

        armature_edit_mode.restore()

        self.report({"INFO"}, "Deleted " + str(len(self._bone_names_to_work_on)) + " bones and added their weights to their parents")

        return {"FINISHED"}




def register():
    bpy.utils.register_class(DeleteZeroWeightBonesAndVertexGroups)
    bpy.utils.register_class(DeleteBonesConstraints)
    bpy.utils.register_class(DeleteBoneAndAddWeightsToParent)

def unregister():
    bpy.utils.unregister_class(DeleteZeroWeightBonesAndVertexGroups)    
    bpy.utils.unregister_class(DeleteBonesConstraints)
    bpy.utils.unregister_class(DeleteBoneAndAddWeightsToParent)

if __name__ == "__main__":
    register()