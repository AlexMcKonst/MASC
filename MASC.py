###!/usr/bin/env python
bl_info = {
    "name": "MASC",
    "author": "Alex McKonst",
    "version": (1, 7, 10),
    "blender": (2, 79, 0),
    "location": "Mesh",
    "description": "'MASC' is a set of scenarios for automating routine workflows and settings.",
    "warning": "WIP",
    "wiki_url": "",
    "tracker_url": "https://github.com/AlexMcKonst/MASC",
    "category": "UI"}
import bpy
import os
from bpy.types import Panel, Menu, Group, GroupObjects
from bpy import props
from bpy.props import *

bpy.selection_msc = []

def select_msc():
    if bpy.context.mode == "OBJECT":
        obj = bpy.context.object
        sel = len(bpy.context.selected_objects)

        if sel == 0:
            bpy.selection_msc = []
        else:
            if sel == 1:
                bpy.selection_msc = []
                bpy.selection_msc.append(obj)
            elif sel > len(bpy.selection_msc):
                for sobj in bpy.context.selected_objects:
                    if (sobj in bpy.selection_msc) is False:
                        bpy.selection_msc.append(sobj)

            elif sel < len(bpy.selection_msc):
                for it in bpy.selection_msc:
                    if (it in bpy.context.selected_objects) is False:
                        bpy.selection_msc.remove(it)


class MASCSelection(bpy.types.Header):
    bl_label = "Selection MASC"
    bl_space_type = "VIEW_3D"

    def __init__(self):
        select_msc()

    def draw(self, context):
        """
        bpy.selection_msc
        """

bpy.types.Scene.CurvBox = BoolProperty(
        default = 0
        )
def selallcr(self, context):
    if bpy.context.scene.SerSpline == 1:
        bpy.ops.object.editmode_toggle()
        lss=len(bpy.context.object.data.splines.items())
        crv=0
        for s in  range(lss):
            lsb=len(bpy.context.object.data.splines[s].bezier_points.items())
            for b in range(lsb):
                spv=bpy.context.object.data.splines[s].bezier_points[b]
                spv.tilt = False
                spv.select_control_point = False
                spv.select_right_handle = False
                spv.select_left_handle = False
            crv+=1
        print(crv)
        while crv !=1:
            for s in  range(crv):
                crv-=1
                if s!=1:
                    for b in range(len(bpy.context.object.data.splines[s].bezier_points.items())):
                        spv=bpy.context.object.data.splines[s].bezier_points[b]
                        spv.tilt = True
                        spv.select_control_point = True
                        spv.select_right_handle = True
                        spv.select_left_handle = True                       
                    bpy.ops.curve.separate()
                break
        bpy.ops.object.editmode_toggle()
    bpy.context.scene.SerSpline = 0
    return
bpy.types.Scene.SerSpline = BoolProperty(
        update = selallcr,
        default = 0
        )  
def joincr(self, context):
#    if bpy.context.scene.joincrv == 1:
    crv=0
    for s in  range(len(bpy.selection_msc)):    
        crv+=1
    print('osc', crv)
    while crv>=1:
        if crv >=1:
            j = bpy.selection_msc
            jc=j.copy()
            bpy.ops.object.select_all(action='TOGGLE')
            for i in range(crv):
                crv-=1
                jc[1].select = True
                jc[0].select = True
                bpy.context.scene.objects.active = jc[0]
                bpy.ops.object.join()
                bpy.ops.object.select_all(action='TOGGLE')
                jc.remove(jc[1])
        break
    bpy.context.scene.joincrv = 0
#    bpy.context.scene.joincrv = 0
    return
  
bpy.types.Scene.joincrv = BoolProperty(
        update = joincr,
        default = 0
        )       
       
def MD(param):
    if param == 'md':
        return bpy.context.mode
    elif param == 'ob':
        return bpy.context.selected_objects
    elif param == 'act':
        return bpy.context.active_object
        
def Edg_covertCrv(self, context):
    bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, -0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'VIEW', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":28.1025, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    bpy.ops.mesh.separate(type='SELECTED')
    bpy.ops.object.editmode_toggle()
    bpy.context.active_object.select = False
    bpy.context.scene.objects.active = bpy.context.selected_objects[0]
    bpy.ops.object.convert(target='CURVE')
    bpy.ops.object.editmode_toggle()
    bpy.ops.curve.spline_type_set(type='BEZIER')
    bpy.ops.curve.subdivide()
    bpy.ops.curve.handle_type_set(type='AUTOMATIC')
    bpy.ops.curve.smooth()
    bpy.ops.curve.smooth()
    bpy.ops.curve.smooth()
    bpy.ops.curve.smooth()
    bpy.ops.object.editmode_toggle()
    bpy.context.scene.EdgConvert = False
    return 

bpy.types.Scene.EdgConvert = BoolProperty(
        update = Edg_covertCrv,
        default = 0)

def fstrd(self, context):
    bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
    for i in range(int(bpy.context.scene.fastrnd)):
        import math
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": True, "mode": 'TRANSLATION'},
                                      TRANSFORM_OT_translate={"value": (0, 0, 0),
                                                              "constraint_axis": (False, False, False),
                                                              "constraint_orientation": 'LOCAL', "mirror": False,
                                                              "proportional": 'DISABLED',
                                                              "proportional_edit_falloff": 'SMOOTH',
                                                              "proportional_size": 2.48857, "snap": False,
                                                              "snap_target": 'CLOSEST', "snap_point": (0, 0, 0),
                                                              "snap_align": False, "snap_normal": (0, 0, 0),
                                                              "gpencil_strokes": False, "texture_space": False,
                                                              "remove_on_cancel": False, "release_confirm": False})

##            bpy.ops.transform.translate(value=(self.rmx, self.rmy, 0), constraint_axis=(True, True, False), constraint_orientation='GLOBAL' if self.drot == 0 else 'LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SPHERE', proportional_size=2.14359)
        bpy.ops.transform.rotate(value=(math.radians(360)/int(bpy.context.scene.fastrnd)),
        axis=(0, 0, 1),
        constraint_axis=(False, False,True),
            constraint_orientation='LOCAL',
            mirror=False, proportional='DISABLED',
            proportional_edit_falloff='SPHERE',
            proportional_size=2.14359, release_confirm=True
        )
        bpy.context.selected_objects
    bpy.ops.object.delete(use_global=False)
#        bpy.data.objects[self.robj.name].select = True
#        bpy.context.scene.objects.active = self.robj
    return 

bpy.types.Scene.fastrnd = bpy.props.EnumProperty(name ='',
    description = 'Fast Rot&Dub',
    items=[
    ('2','2','2'),
    ('3','3','3'),
    ('4','4','4'),
    ('5','5','5'),
    ('6','6','6')], 
    update=fstrd)

#----->
class QuickShrink(bpy.types.Operator):
    """Quick_Shrink"""
    bl_idname = "scene.qshrink"
    bl_label = "QShrink"
#    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        sel = bpy.selection_msc
        bpy.context.scene.objects.active = sel[0]
        if len(sel) >=2:
            sel[1].select = False
        asl = bpy.selection_msc[0].name
        if bpy.data.objects[asl].modifiers.items() != []:
            if 'QShrinkwrap' in bpy.data.objects[asl].modifiers.items()[-1][0]:
                bpy.ops.object.modifier_remove(modifier="QShrinkwrap")
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        lst = bpy.data.objects[asl].modifiers.items()[-1][0]
        bpy.context.object.modifiers[lst].name = "QShrinkwrap"
        lst = bpy.data.objects[asl].modifiers.items()[-1][0]
        bpy.data.objects[asl].modifiers[lst].target = sel[-1]
        bpy.context.object.modifiers[lst].show_on_cage = True 
        return {"FINISHED"}
    
class QuickMirror(bpy.types.Operator):
    """Quick_Mirror"""
    bl_idname = "scene.qmirror"
    bl_label = "QMirror_Object"
    bl_options = {"REGISTER", "UNDO"}
    
    axm = BoolVectorProperty(
            name="Axis", 
            description="Axis", 
            default=(1, 0, 0),
            subtype = 'XYZ')
    axm2 = BoolProperty(
            name="Axis", 
            description="Axis", 
            default=0
            )
    def execute(self, context):
        print(self.axm[0], self.axm[1], self.axm[2])
        sel = bpy.selection_msc
        bpy.context.scene.objects.active = sel[0]
#        bpy.context.scene.objects.active.select = True
#        if len(sel) >=2:
#            sel[1].select = False
        asl = bpy.context.scene.objects.active.name
        if bpy.data.objects[asl].modifiers.items() != []:
            if 'QMirror' in bpy.data.objects[asl].modifiers.items()[-1][0]:
                bpy.ops.object.modifier_remove(modifier="QMirror")
        bpy.ops.object.modifier_add(type='MIRROR')
        lst = bpy.data.objects[asl].modifiers.items()[-1][0]
        bpy.context.object.modifiers[lst].name = "QMirror"
        lst = bpy.data.objects[asl].modifiers.items()[-1][0]
        bpy.context.object.modifiers[lst].mirror_object = sel[-1]
        bpy.context.object.modifiers[lst].show_on_cage = True 
        bpy.context.object.modifiers[lst].use_x = self.axm[0]
        bpy.context.object.modifiers[lst].use_y = self.axm[1]
        bpy.context.object.modifiers[lst].use_z = self.axm[2]
        bpy.context.scene.objects.active = sel[1]   
        return {"FINISHED"}
     
#-----> """Grading of objects""
class Gradobj(bpy.types.Operator):
    """Graduation"""
    bl_idname = "scene.gradobj"
    bl_label = "Grading of objects"
    bl_options = {"REGISTER", "UNDO"}

    opc = bpy.props.BoolProperty(
        name="XY (Scaling axes)",
        description="Scaling axes",
        default=1
        )
    sz = bpy.props.FloatProperty(
        name="SIZE",
        description="The scale of the duplicated object",
        default=0.9,
        min=0.0
    )
    pr = bpy.props.FloatProperty(
        name="%",
        description="percent",
        default=1.95,
    )
    rt = bpy.props.FloatProperty(
        name="Axis rotation",
        description="Rotate duplicate object",
        default=0
    )
    rsc = bpy.props.FloatProperty(
        name="Scale",
        description="Scale",
        default=0
    )
    dp = bpy.props.IntProperty(
        name="Number",
        description="Number of object duplicates",
        default=3,
        min=0
    )

    def execute(self, context):
        def obsyp():
            bpy.ops.mesh.primitive_uv_sphere_add(size=self.sz, view_align=False, enter_editmode=False)
            bpy.ops.apply.transformscale()
        def dup2():
            """дублировать, скайлить, переместить на величину скайла"""
#            bpy.ops.apply.transformscale()
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},
                        TRANSFORM_OT_translate={"value":(-0, 0, 0),
                        "constraint_axis":(False, False, False),
                        "constraint_orientation":'LOCAL', "mirror":False, "proportional":'DISABLED',
                        "proportional_edit_falloff":'SMOOTH', "proportional_size":1.4641, "snap":False,
                        "snap_target":'CLOSEST', "snap_point":(0, 0, 0),
                        "snap_align":False, "snap_normal":(0, 0, 0),
                        "gpencil_strokes":False, "texture_space":False,
                        "remove_on_cancel":False, "release_confirm":False})
            bpy.ops.transform.resize(value=(self.sz, self.sz, 1.0 if self.opc == 1 else self.sz),
                        constraint_axis=(True, True, False if self.opc == 1 else True),
                        constraint_orientation='LOCAL')
#            bpy.ops.apply.transformscale()
            ns = bpy.data.objects[bpy.context.active_object.name].scale[0]
            # print(ns)
            bpy.ops.transform.translate(value=(0, ns/self.pr, 0),
                        constraint_axis=(False, True, False),
                        constraint_orientation='LOCAL')
        def dup3():
            """режим правки, дублировать, скайлить, переместить на величину скайла"""
            #            bpy.ops.apply.transformscale()
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1}, TRANSFORM_OT_translate={"value": (-0, self.pr, 0),
                                                                                               "constraint_axis": (
                                                                                               False, True, False),
                                                                                               "constraint_orientation": 'LOCAL',
                                                                                               "mirror": False,
                                                                                               "proportional": 'DISABLED',
                                                                                               "proportional_edit_falloff": 'SMOOTH',
                                                                                               "proportional_size": 1,
                                                                                               "snap": False,
                                                                                               "snap_target": 'CLOSEST',
                                                                                               "snap_point": (0, 0, 0),
                                                                                               "snap_align": False,
                                                                                               "snap_normal": (0, 0, 0),
                                                                                               "gpencil_strokes": False,
                                                                                               "texture_space": False,
                                                                                               "remove_on_cancel": False,
                                                                                               "release_confirm": False})

            bpy.ops.transform.resize(value=(self.sz, self.sz, 1.0 if self.opc == 1 else self.sz),
                                     constraint_axis=(True, True, False if self.opc == 1 else True),
                                     constraint_orientation='LOCAL')
            #            bpy.ops.apply.transformscale()
            # print(ns)

            # bpy.ops.transform.translate(value=(0, self.pr, 0),
            #                             constraint_axis=(False, True, False),
            #                             constraint_orientation='LOCAL')
            bpy.ops.object.editmode_toggle()
        # rotation mass
        if bpy.context.selected_objects != []:
#            bpy.ops.transform.resize(value=(self.sz, self.sz, 1.0),
#                        constraint_axis=(False, False, False),
#                        constraint_orientation='LOCAL', mirror=False,
#                        proportional='DISABLED', proportional_edit_falloff='SMOOTH',
#                        proportional_size=1.1
#                        )
            slo = bpy.context.selected_objects
            bpy.ops.transform.resize(value=(1+self.rsc, 1+self.rsc, 1), constraint_axis=(True, True, False), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=0.13513)
            bpy.ops.transform.rotate(value=self.rt, axis=(0, 0, 0), constraint_axis=(False, False, True), constraint_orientation='LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1.1, release_confirm=True)
            zz = bpy.data.objects[slo[0].name].dimensions[2]
            for i in range(self.dp):
                dup2()
                # print("SEL", len(slo))
        else:
            self.report({'WARNING'}, "Please select an object for duplication!")

        return {"FINISHED"}

#-----> """RotateObject(DUPLI)""
class Robject(bpy.types.Operator):
    """I rotate duplicate objects around the anchor point\nor relative to the cursor point"""
    bl_idname = "scene.robject"
    bl_label = "Rotate & Duble Me"
    bl_options = {"REGISTER", "UNDO"}

    grad = bpy.props.IntProperty(
        name="copies",
        description="copies",
        default=2,
        min=2
    )
    rmx = bpy.props.FloatProperty(
        name="Move_X",
        description="Move_X(LOCAL)",
        default=0
    )
    rmy = bpy.props.FloatProperty(
        name="Move_Y",
        description="Move_Y(LOCAL)",
        default=0
    )
    rax = bpy.props.EnumProperty(
        items=[('X', 'X', 'X'),
               ('Y', 'Y', 'Y'),
               ('Z', 'Z', 'Z'),],
        name="Axis",
        default = 'Z'
        )
    arrc = bpy.props.BoolProperty(
        name="ArroundCursor",
        description="To rotate relative to the cursor",
        default=1
    )
    dstp = bpy.props.BoolProperty(
        name="LINK",
        description="A linked copy",
        default=1
    )
    drot = bpy.props.BoolProperty(
        name="LOCAL",
        description='''Rotation according to the local coordinates\nof the active object''',
        default=0
    )
    def execute(self, context):
        if self.arrc == 1:
            bpy.context.space_data.pivot_point = 'CURSOR'
        else:
            bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
        bpy.ops.transform.translate(value=(self.rmx, self.rmy, 0), constraint_axis=(True, True, False), constraint_orientation='GLOBAL' if self.drot == 0 else 'LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SPHERE', proportional_size=2.14359)
        for i in range(self.grad):
            import math
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": True if self.dstp ==1 else False, "mode": 'TRANSLATION'},
                                          TRANSFORM_OT_translate={"value": (0, 0, 0),
                                                                  "constraint_axis": (False, False, False),
                                                                  "constraint_orientation": 'LOCAL', "mirror": False,
                                                                  "proportional": 'DISABLED',
                                                                  "proportional_edit_falloff": 'SMOOTH',
                                                                  "proportional_size": 2.48857, "snap": False,
                                                                  "snap_target": 'CLOSEST', "snap_point": (0, 0, 0),
                                                                  "snap_align": False, "snap_normal": (0, 0, 0),
                                                                  "gpencil_strokes": False, "texture_space": False,
                                                                  "remove_on_cancel": False, "release_confirm": False})

##            bpy.ops.transform.translate(value=(self.rmx, self.rmy, 0), constraint_axis=(True, True, False), constraint_orientation='GLOBAL' if self.drot == 0 else 'LOCAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SPHERE', proportional_size=2.14359)
            bpy.ops.transform.rotate(value=(math.radians(360)/self.grad),
            axis=(0, 0, 1),
            constraint_axis=(True if self.rax == 'X' else False,
                True if self.rax == 'Y' else False,
                True if self.rax == 'Z' else False
                ),
                constraint_orientation='GLOBAL' if self.drot == 0 else 'LOCAL',
                mirror=False, proportional='DISABLED',
                proportional_edit_falloff='SPHERE',
                proportional_size=2.14359, release_confirm=True
            )
            bpy.context.selected_objects
        bpy.ops.object.delete(use_global=False)
#        bpy.data.objects[self.robj.name].select = True
#        bpy.context.scene.objects.active = self.robj
        return {"FINISHED"}

#-----> """Create_the_one_ring""
class Crlwo(bpy.types.Operator):
    """I create the one ring
       or the connection
       of the two rings(bézier_curve)
       And more...
       Mark the curve
       and give it a profile button "FillCurve"
    """
    bl_idname = "scene.crlwo"
    bl_label = "Curve Profile"
    bl_options = {"REGISTER", "UNDO"}

    lnc2 = bpy.props.EnumProperty(
        items=[('2Circle', '2Circle', '2Circle'),
               ('FillCurve', 'FillCurve', 'FillCurve'),
               ('Selcet', 'Selcet', 'Selcet')],
        name="Select a method",
        default='Selcet'
    )
    bzc = bpy.props.FloatProperty(
        name="Inner diameter('Cyrcle')",
        description="inner_diameter",
        default=1,
        min=0.0
    )
    bdc = bpy.props.FloatProperty(
        name="1 profile(diameter)",
        description="bevel_depth",
        default=1,
        min=0.0
    )
    trcl = bpy.props.FloatProperty(
        name = "Move Circl 'X'",
        description = "TRANSFORM_OT_translate={"'value'":(self.trcl, 0, 0)",
        default = 1.07748
    )
    vwc = bpy.props.BoolProperty(
        name="Algin View('Cyrcle')",
        description="view_align",
        default=False
    )
    cqv = bpy.props.EnumProperty(
        items = [('rhomb', 'rhomb', 'rhomb'),
                 ('square', 'square', 'square'),
                 ('0', '0', '0')],
        name = "2 profile('Cuve')",
        description = "PrFill",
        default = '0'
        #options={'HIDDEN' if flc[1]['default']!=1 else 'ANIMATABLE'},
    )
    md = 0
    rd = 0
##    @classmethod
##    def poll(cls, context):
##        return bpy.context.mode !='EDIT_CURVE'

    def execute(self, context):
        csm = bpy.context.mode
        sel = bpy.context.selected_objects
        CdR = (self.bzc + self.bdc)/2
        #        bpy.opself.script.python_file_run(filepath = p + "TranspON.py")
        def selvert():
            """Select all the vertices of the curve"""
            spv = bpy.context.object.data.splines[0].bezier_points
            for i in range(len(spv)):
                spv[i].tilt = True
                spv[i].select_control_point = True
                spv[i].select_right_handle = True
        def tilt():
            spv = bpy.context.object.data.splines[0].bezier_points
            for i in range(len(spv)):
                spv[i].tilt = 0
                spv[i].tilt = 0
                spv[i].tilt = 0
        def prof():
            if csm == 'EDIT_CURVE':
                bpy.ops.object.editmode_toggle()
            bpy.context.object.data.fill_mode = 'FULL'
            bpy.context.object.data.bevel_depth = self.bdc/2
            if self.cqv == '0':
                bpy.context.object.data.bevel_resolution = 16 #self.brc
            else:
                if self.cqv == 'square':
                    import math
                    d2 = self.bdc * math.sqrt(2) # new diag for new side squar
                    tilt()
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.transform.tilt(value=(math.radians(45)), mirror=False, proportional='DISABLED',
                                           proportional_edit_falloff='SMOOTH', proportional_size=2.48857)
                    bpy.ops.object.editmode_toggle()
                    bpy.context.object.data.bevel_resolution = 0
##                    bpy.data.curves[sel[0].name].bevel_depth = d2/2
                    bpy.context.object.data.bevel_depth = d2/2
##                    print('0', sel[0].name)
                if self.cqv == 'rhomb':
                    # bpy.ops.object.editmode_toggle()
                    # bpy.ops.curve.tilt_clear()
                    # bpy.ops.object.editmode_toggle()
                    bpy.context.object.data.bevel_resolution = 0.
                    spv = bpy.context.object.data.splines[0].bezier_points
                    tilt()
        if sel == [] and self.rd == 0:
            self.lnc2 = 'Selcet'
            self.report({'INFO'}, "RING MODE 'ON': Not found the curves for editing.")
            self.rd = 1
        if self.lnc2=='Selcet' or self.lnc2=='2Circle':
            bpy.ops.curve.primitive_bezier_circle_add(
                radius=CdR,
                view_align=self.vwc)
            bpy.context.object.data.fill_mode = 'FULL'
            if self.cqv == '0':
                bpy.context.object.data.bevel_depth = self.bdc / 2
                bpy.context.object.data.bevel_resolution = 16 #self.brc
            else:
                prof()
        #            leenk = self.lnc2:
        while self.lnc2=='2Circle':
            bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True, "mode":'TRANSLATION'},
                                                 TRANSFORM_OT_translate={"value":(self.trcl, 0, 0), "constraint_axis":(True, False, False),
                                                                         "constraint_orientation":'LOCAL', "mirror":False, "proportional":'DISABLED',
                                                                         "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False,
                                                                         "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0),
                                                                         "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
            bpy.ops.transform.rotate(value=1.5708, axis=(0.397503, 0.917601, -2.2628e-007), constraint_axis=(True, False, False),
                                     constraint_orientation='LOCAL', mirror=False, proportional='DISABLED',
                                     proportional_edit_falloff='SMOOTH', proportional_size=6.11584, release_confirm=True)
            break

        if self.lnc2== "FillCurve" and self.md == 0: # fill curve ON
            self.report({'INFO'}, "CURE MODE 'ON'")
            selvert()
            self.md = 1
        if bpy.context.active_object.type == 'CURVE' and self.lnc2=="FillCurve":
            prof()
        return {"FINISHED"}

#-----> """Props ops_Kursor"""
class kurs(bpy.types.Operator):
    """Porps ops_Kursor"""
    bl_idname = "scene.kursor"
    bl_label = "Pos Kursor"
    bl_options = {"REGISTER", "UNDO"}

    kr1 = bpy.props.BoolProperty(name="To_selected", description="K1", default=0)
    kr2 = bpy.props.BoolProperty( name="point_align", description="K2", default=0)
    kNull = bpy.props.BoolProperty(name="0.0.0", description="0.0.0", default=1)
    defo = bpy.props.BoolProperty(name="reset", description="res", default=0)
    krpnt = bpy.props.BoolProperty(name="LOCpoint_to_kursor", description="pnt2krsr", default=0)
    def execute(self, context):
        if self.kr1 == 1:
            #Cur01(scale)
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.context.space_data.pivot_point = 'CURSOR'
#            bpy.data.screens['Default'].areas[3].spaces[0].transform_orientation = "GLOBAL"
            bpy.context.space_data.transform_orientation = 'GLOBAL'
        #Cur02(move)
        bpy.context.space_data.use_pivot_point_align = self.kr2
        if self.defo == 1:
            bpy.context.space_data.use_pivot_point_align = False
            bpy.context.space_data.pivot_point = 'ACTIVE_ELEMENT'
            bpy.context.space_data.transform_orientation = 'LOCAL'
            self.kr1=self.kr2=self.kNull=self.defo=0
#            self.kr1=0
#            self.kNull=0
#            self.defo=0
        if self.kNull == 1:
            bpy.context.scene.cursor_location.xyz = 0
            bpy.context.space_data.pivot_point = 'CURSOR'
            bpy.context.space_data.transform_orientation = 'GLOBAL'
            self.kr1=self.kr2=self.kNull=0
        if self.krpnt == 1:
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            bpy.ops.object.editmode_toggle()
            self.krpnt = 0

        return {"FINISHED"}

    def invoke(self, context, event):
        global kr1, kr2, kNull, defo, krpnt
        return context.window_manager.invoke_props_dialog(self)


#-----> """dissolution"""
class dissol(bpy.types.Operator):
    """I reduce the number of points on the edge"""
    bl_idname = "scene.dissol"
    bl_label = "dissolution"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # bpy.ops.script.python_file_run(filepath = p + "Dsel_Vrtx_ches.py")
        bpy.ops.mesh.select_linked(delimit={'SEAM'})
        bpy.ops.mesh.select_nth()
        bpy.ops.mesh.dissolve_mode(use_verts=True)
        bpy.ops.mesh.select_linked(delimit={'SEAM'})
        bpy.ops.mesh.looptools_space()
        return {"FINISHED"}

#-----> """Change active object"""
class changobj(bpy.types.Operator):
    """Change active object"""
    bl_idname = "scene.changobj"
    bl_label = "Change_active_object"
    bl_options = {"REGISTER", "UNDO"}

    chl = bpy.props.BoolProperty(
        name="Set active object",
        description="chl",
        default=0
        )
    chlst = bpy.props.IntProperty(
        name="List active object",
        description="chlst",
        default=0,
#        min=-(len(bpy.context.selected_objects)),
        max=-1
        )
#    lo = bpy.selection_msc
    def execute(self, context):
        try:
            Ob = bpy.context.object.select
        except IndexError:
            print(No_Object)
#        if Ob == True:
        lo = bpy.context.selected_objects
#        bpy.context.object.show_name = False
        if self.chl==0 and self.chlst<len(lo)-1:
            try:
                bpy.context.scene.objects.active = bpy.data.objects[lo[self.chlst].name]
#                bpy.context.object.show_name = True
            except IndexError:
                bpy.context.scene.objects.active = bpy.data.objects[lo[-1].name]
#                bpy.context.object.show_name = True
                self.chl=0
                self.chlst=0
#            else:
#                bpy.context.scene.objects.active = bpy.data.objects[lo[0].name]
        if self.chl!=0:
            bpy.context.scene.objects.active = bpy.data.objects[lo[0].name]
            self.chl=0
            self.chlst=0

#        if self.chl !=0:
        #        bpy.ops.script.python_file_run(filepath = p + "ChangeActiveObj.py")
        return {"FINISHED"}


#-----> """Join 1 object (objects) to the active object"""
class AplyJion(bpy.types.Operator):
    """Join 1 object (objects) to the active object"""
    bl_idname = "scene.apjion"
    bl_label = "APLY(Join, locRot)"
    bl_options = {"REGISTER", "UNDO"}

    CMs = bpy.props.BoolProperty(
        name="ORIGIN_CENTER_OF_MASS",
        description="ORIGIN_CENTER_OF_MASS",
        default=0
        )

    def execute(self, context):
        # # CURVE BLOCK
        # def selvert():
        #     """Select all the vertices of the curve"""
        #     spv = bpy.context.object.data.splines[0].bezier_points
        #     for i in range(len(spv)):
        #         spv[i].tilt = True
        #         spv[i].select_control_point = True
        #         spv[i].select_right_handle = True
        # def tilt():
        #     spv = bpy.context.object.data.splines[0].bezier_points
        #     for i in range(len(spv)):
        #         spv[i].tilt = 0
        #         spv[i].tilt = 0
        #         spv[i].tilt = 0
        # # END))
        if bpy.context.selected_objects != []:
            obj = bpy.context.selected_objects
            def actic(act):
                for i in bpy.context.selected_objects:
                    if i != act:
                        bpy.context.scene.objects.active = i
            def sel(SEL):
                import bmesh
                """Here second seleted all vertex"""
                bpy.ops.object.editmode_toggle()
                mesh = bmesh.from_edit_mesh(bpy.context.object.data)
                for v in mesh.verts:
                    v.select = SEL
                for v in mesh.edges:
                    v.select = SEL
                for v in mesh.faces:
                    v.select = SEL
                bpy.ops.object.editmode_toggle()
            def joint():
                for i in bpy.context.selected_objects:
                    if i != bpy.context.scene.objects.active:
                        nm = bpy.context.scene.objects.active.name
                if len(obj) >= 2:                   
                    sel(True)
                    ##   Here first object made is active
                    # bpy.context.scene.objects.active = obd[1]
                    actic(bpy.context.scene.objects.active)
                    sel(False)
                    #     ##   Selected acive seconde object
                    bpy.ops.object.make_links_data(type='MODIFIERS')
                    actic(bpy.context.scene.objects.active)
                    #     ##   object.join
                    bpy.ops.object.join()
                    #     ##    Edit mode del vertex
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.mesh.delete(type='VERT')
                    bpy.ops.object.editmode_toggle()
                    bpy.context.object.name = nm
                return

            if len(obj) == 1: # single selected objct
                act = bpy.context.selected_objects[0]
                bpy.ops.view3d.snap_cursor_to_active()
                # if bpy.context.scene.objects.active.type =='CURVE':
                #     bpy.ops.curve.primitive_bezier_curve_add()
                # else:
                #     bpy.ops.mesh.primitive_cube_add()
                bpy.ops.mesh.primitive_cube_add()
                bpy.context.scene.objects.active = act
                bpy.context.active_object.select = True
                bpy.ops.object.make_links_data(type='MODIFIERS')
                obj = bpy.context.selected_objects
                actic(act) # change activ obj
                joint() # join to second obj del selected vert
                obj = []
            if len(obj) == 2:
                print('2obj')
                joint()

            if len(bpy.context.selected_objects) < 2:
                if self.CMs == 1:
                    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')

        return {"FINISHED"}

#-----> """Sculpt"""
class SculptMyDint(bpy.types.Operator):
    """
    My prop for Sculpt(activate Dintopo)
    Get the name of the sculpture brush.
    Written to the variable "aname"
    Create a pattern brush in quotes
    Enter parametters
    """
    bl_idname = "scene.scdint"
    bl_label = "Sculpt_MyDintopo"
    bl_options = {"REGISTER", "UNDO"}

    myspec = bpy.props.BoolProperty(
        name="MY_SPEC",
        description="MSPC",
        default=0
        )

    def execute(self, context):
        # Get the name of the sculpture brush. Written to the variable "aname"
        #bpy.ops.script.python_file_run(filepath = p + "Sculpt_MyDint.py")
        aname = bpy.context.scene.tool_settings.sculpt.brush.name

        # Create a pattern brush in quotes
        B = "%s" % aname + ""

        # Put options sculpting
        if self.myspec == 1:
            bpy.context.scene.tool_settings.sculpt.detail_refine_method = 'SUBDIVIDE_COLLAPSE'
            bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False
            bpy.data.brushes[B].use_frontface = True
            bpy.data.brushes[B].strength = 0.5
            bpy.data.brushes[B].auto_smooth_factor = 0.6
            bpy.context.scene.tool_settings.unified_paint_settings.size = 40
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 10

        md = bpy.context.mode
        if md == 'OBJECT':
            bpy.ops.sculpt.sculptmode_toggle()
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting == False:
                bpy.ops.sculpt.dynamic_topology_toggle()
        if md == 'SCULPT' and self.myspec != 1:
            if bpy.context.sculpt_object.use_dynamic_topology_sculpting != False:
                bpy.ops.sculpt.dynamic_topology_toggle()
            bpy.ops.sculpt.sculptmode_toggle()
        return {"FINISHED"}

#-----> """AutoRend+FS"""
class OpsRenderLrs(bpy.types.Operator):
    """My Prop For Render & Render Layers, activate FS"""
    bl_idname = "scene.autorend"
    bl_label = "AutoRend+FS"
    bl_options = {"REGISTER", "UNDO"}

    rgsl = bpy.props.BoolProperty(
        name="RGSL",
        description="RGSL",
        default=0
        )
    rprop = bpy.props.BoolProperty(
        name="MySetR",
        description="MySetR",
        default=0
        )
    chr = bpy.props.BoolProperty(
        name="CAMERA PREF",
        description="Change_resol",
        default=0
        )
    chr = bpy.props.EnumProperty(
        items = [('[]', '[]', '[]'),
                 ('Change_resol', 'Change_resol', 'Change_resol'),
                 ('Select', 'Select', 'Select')],
        name = "CAMERA PREF",
        description = "CAMERA PREF",
        default = 'Select'
        #options={'HIDDEN' if flc[1]['default']!=1 else 'ANIMATABLE'},
    )
    def execute(self, context):
        if self.rgsl == 1:
            bpy.context.scene.render.resolution_percentage = 100
            bpy.context.scene.render.use_antialiasing = True
            bpy.context.scene.render.antialiasing_samples = '16'
            bpy.context.scene.render.use_motion_blur = False
            bpy.context.scene.render.resolution_percentage = 100
            bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
            bpy.context.space_data.viewport_shade = 'MATERIAL'
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
            bpy.context.scene.render.image_settings.compression = 0
            bpy.context.scene.render.use_freestyle = False

            self.rgsl = 0
        if self.rprop == 1:
##            bpy.ops.script.python_file_run(filepath= p + "AutoRend.py")
                #Render set for fin rndr
            bpy.context.scene.render.resolution_percentage = 75
            bpy.context.scene.render.use_border = True
            bpy.context.scene.render.use_crop_to_border = True
            bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
            bpy.context.scene.render.use_freestyle = True
            bpy.context.scene.render.line_thickness = 0.55
            bpy.context.scene.render.use_antialiasing = True
            bpy.context.scene.render.image_settings.compression = 0
            #bpy.context.scene.render.layers.active.use_pass_ambient_occlusion = True
            bpy.context.scene.render.threads_mode = 'FIXED'
            bpy.context.scene.render.threads = 2
            bpy.context.scene.render.use_motion_blur = False
            bpy.context.scene.render.antialiasing_samples = '8'
                #RenderLayer_options
            if len(bpy.context.scene.render.layers) >=2: # del layers
                for i in range(len(bpy.context.scene.render.layers)):
                    if i !=0:
                        bpy.context.scene.render.layers.active_index = i
                        bpy.ops.scene.render_layer_remove()
            bpy.context.scene.render.layers[bpy.context.scene.render.layers.active.name].name = "RenderLayer"
            bpy.context.scene.render.layers["RenderLayer"].use_strand = False
            bpy.context.scene.render.layers["RenderLayer"].use_sky = False
            bpy.context.scene.render.layers["RenderLayer"].use_pass_z = False
            bpy.context.scene.render.layers["RenderLayer"].use_freestyle = False
                #RenderLayer_FS_options
            bpy.context.scene.render.layers.new('FS')
            bpy.context.scene.render.layers.active_index = 1
            bpy.context.scene.render.layers["FS"].use_strand = False
            bpy.context.scene.render.layers["FS"].use_edge_enhance = False
            bpy.context.scene.render.layers["FS"].use_sky = False
            bpy.context.scene.render.layers["FS"].use_ztransp = False
            bpy.context.scene.render.layers["FS"].use_halo = False
            bpy.context.scene.render.layers["FS"].use_solid = False
            bpy.context.scene.render.layers["FS"].use_pass_z = False
            bpy.context.scene.render.layers["FS"].use_pass_combined = False
                #Freestyle set.
            bpy.context.scene.render.layers.active.freestyle_settings.use_smoothness = True
            bpy.context.scene.render.layers.active.freestyle_settings.crease_angle = 2.53073
            lineset = bpy.context.scene.render.layers.active.freestyle_settings.linesets.new('my lineset')
            lineset.select_external_contour = True
            lineset.select_contour = True
                # image_settings
            bpy.context.space_data.viewport_shade = 'MATERIAL'
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
            bpy.context.scene.render.image_settings.compression = 0
                #NODE
            bpy.context.scene.use_nodes = False
                #AO
            AOs=bpy.context.scene.render.layers["RenderLayer"].use_pass_ambient_occlusion
            if AOs == False:
                bpy.context.scene.render.layers["RenderLayer"].use_pass_ambient_occlusion = True
            AOw = bpy.context.scene.world.light_settings.use_ambient_occlusion
            if AOw == False:
                bpy.context.scene.world.light_settings.use_ambient_occlusion = True
                bpy.context.scene.world.light_settings.use_ambient_occlusion = True
                bpy.context.scene.world.light_settings.ao_factor = 1
            del AOs, lineset, AOw
            self.rprop = 0
        if self.chr == "Change_resol":
            rx = bpy.data.scenes['Scene'].render.resolution_x
            ry = bpy.data.scenes['Scene'].render.resolution_y
            #if bpy.context.selected_objects[0].type != 'CAMERE' or bpy.context.selected_objects == []:
            #    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(5, 5, 7), rotation=(0.785398, 0, 2.35619), layers=(False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            #else:
            #    bpy.data.scenes['Scene'].render.resolution_x = ry
            #    bpy.data.scenes['Scene'].render.resolution_y = rx

            #bpy.context.object.data.type = 'ORTHO'
            bpy.data.scenes['Scene'].render.resolution_x = ry
            bpy.data.scenes['Scene'].render.resolution_y = rx
            self.chr ="Select"
        if self.chr == "[]":
            rx = bpy.data.scenes['Scene'].render.resolution_x
            ry = bpy.data.scenes['Scene'].render.resolution_y
            if rx > ry:
                bpy.data.scenes['Scene'].render.resolution_y = rx
            else:
                bpy.data.scenes['Scene'].render.resolution_x = ry
        return {"FINISHED"}
    def invoke(self, context, event):
        global rgsl, rprop
        return context.window_manager.invoke_props_dialog(self)

#-----> """Gruop For Name Items"""
class GruopForNameItems(bpy.types.Operator):
    """I create a group by the name(item) of the active object"""
    bl_idname = "scene.grpnmimts"
    bl_label = "Grouping, joining existing groups"
    bl_options = {"REGISTER", "UNDO"}

    def myfunc(self, d):
        d=[(i.name, i.name, i.name) for i in list(bpy.data.groups)] if bpy.data.groups.items() != [] else [('The list is empty', 'The list is empty', 'The list is empty')]
        if bpy.data.groups.items() != []:
            d.append(('Select a group name', 'Select a group name', 'Select a group name'))
        return d

    gset = bpy.props.EnumProperty(
        items=[('Total group', 'Total group', 'Total group'), # все элементы собираются в общую группу с именем активного объекта
               ('Many groups', 'Many groups', 'Many groups')], # Каждый элемент в отдельную группу под своим именем
        name="Grouping method",
        description="Select a method for grouping",
        default='Total group')

    gstr = bpy.props.StringProperty(
        name="Any Name", # любое имя
        description="Enter the name of the 'Total group'.\nBy default, the group takes the name of the active object",
        default=''
        )
    gset2 = bpy.props.EnumProperty(
        items= myfunc, # список групп проекта
        name="Existing groups",
        description="Select groups from the project to join them"
        )
    def __init__(self):
        self.gstr =''
        if bpy.data.groups.items() != []:
            self.gset2 = 'Select a group name'
    def execute(self, context):
        obj = bpy.context.selected_objects
        if obj != []:
            if self.gstr == '':  # И если сторка пустая
                if self.gset == 'Many groups':
                    if bpy.data.groups.items() != []:
                        self.gset2='Select a group name'
                    # снять выделение со всего
                    self.gstr = ''
                    bpy.ops.object.select_all(action='TOGGLE')
                    for i in range(len(obj)):  # цикл от длины списка
                        if obj != None:
                            # удалить значение по идексу
                            nm = obj.pop(0)
                        # получение имени выделенного элемента
                        nmpop = nm.name
                        # выделяем обж по индексу
                        obsl = bpy.data.objects[nmpop]
                        obsl.select = True
                        # делаем обж "активным"
                        bpy.context.scene.objects.active = bpy.data.objects[nmpop]
                        # показываем имя в окне вида и группируем по имени объекта
                        bpy.context.object.show_name = True
                        bpy.ops.group.create(name=nmpop)
                        print(nmpop)
                        # снимаем выделение
                        obsl.select = False
                    self.report({'INFO'}, "Created of many groups")
                # ДАЛЕЕ присоединие к указанной группе
                if self.gset == 'Total group':
                    if self.gset2 == "Select a group name" or self.gset2 == "The list is empty":
                        nm2 = bpy.context.scene.objects.active.name
                        bpy.context.object.show_name = True
                        bpy.ops.group.create(name=nm2)
                        self.report({'INFO'}, "Created a public group: %s" % nm2)
                    else:
                        # bpy.ops.object.group_link(group=self.gset2)
                        # bpy.ops.group.create(name=self.gset2)
                        self.gstr = ''
                        self.gset = 'Total group'
                        for i in obj:
                            i.select = True
                            bpy.context.scene.objects.active = bpy.data.objects[i.name]
                            bpy.ops.object.group_link(group=self.gset2)
                        self.report({'INFO'}, "Objects are attached to: %s" % self.gset2)
                # if self.gset2 != 'The list is empty' or self.gset2 != 'Select a group name':
                #     self.gstr = ''
                #     self.gset = 'Total group'
                #     for i in obj:
                #         i.select = True
                #         bpy.context.scene.objects.active = bpy.data.objects[i.name]
                #         bpy.ops.object.group_link(group=self.gset2)
                #     self.report({'INFO'}, "Objects are attached to: %s" % self.gset2)
            else:
                bpy.ops.group.create(name=self.gstr)
                self.report({'INFO'}, "Created a total group: %s" % self.gstr)
        else:
            self.report({'INFO'}, "There is no selected object")
        return {"FINISHED"}
    def invoke(self, context, event):
        global gets, gstr, gr0
        return context.window_manager.invoke_props_dialog(self)

#-----> """Name Items For Dupli Group Name"""
class App_NmLink_ToEmpty(bpy.types.Operator):
    """Name dupltgruop + Replace name Empty"""
    bl_idname = "scene.rempty"
    bl_label = "App_NmLink_ToEmpty"
    bl_options = {"REGISTER", "UNDO"}

    gsz = bpy.props.FloatProperty(name="SIZE_SPHERE", description="chlst", default=1.45, min=0)

    def execute(self, context):
        """app_nameObj_to_Newgruop"""
        # bpy.ops.object.select_all(action='TOGGLE')
        for i in range(len(bpy.context.selected_objects)):
            n = bpy.context.selected_objects[i].name
            bpy.context.scene.objects.active = bpy.data.objects[n]
            e = bpy.context.active_object.dupli_group.name
            bpy.context.object.name = e
            bpy.context.object.show_name = True
            bpy.context.object.empty_draw_size = self.gsz
            bpy.context.object.empty_draw_type = 'SPHERE'

        # bpy.ops.script.python_file_run(filepath= p + "App_NmLink_ToEmpty.py")
        return {"FINISHED"}

#-----> """ReScale & normalOut"""
class Sacle_Nrml(bpy.types.Operator):
    """Aply sacle, outnormal"""
    bl_idname = "scene.rscnrm"
    bl_label = "ReScale & normalOut"
    bl_options = {"REGISTER", "UNDO"}

    unlo = bpy.props.BoolProperty(
        name="Unlink",
        description="To make a unique object",
        default=0
        )
    def execute(self, context):
        #   Here object make_single_user and transform_apply
        if self.unlo == 1:
            bpy.ops.object.make_single_user(
                object=True,
                obdata=True,
                material=False,
                texture=False,
                animation=False
                )
            bpy.ops.object.transform_apply(
                location=False,
                rotation=False,
                scale=True
                )
            self.unlo=0
        def strt():
            import bmesh
            mesh=bmesh.from_edit_mesh(bpy.context.object.data)
            for v in mesh.verts:
                v.select = False
            for v in mesh.edges:
                v.select = False
            for v in mesh.faces:
                v.select = False
            #   trigger viewport update
            bpy.context.scene.objects.active = bpy.context.scene.objects.active
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.context.object.data.show_normal_loop = False
            bpy.context.object.data.show_normal_vertex = False
            bpy.context.object.data.show_normal_face = False
            bpy.ops.mesh.select_all(action='TOGGLE')
            bpy.ops.object.editmode_toggle()
        #   Here object seleted all vertex
        sedt = bpy.context.mode
        scl = bpy.context.object.scale.xyz.to_tuple(1)
        if sedt == 'OBJECT':
            if scl == (1.0, 1.0, 1.0): # detect object scale Vector((1.0, 1.0, 1.0))
                bpy.ops.object.editmode_toggle() # edit mode
                strt()                           # run def strt()
            else:
                try:
                    bpy.ops.apply.transformscale()
                    bpy.ops.object.editmode_toggle()
                    strt()
                    print('scene.rscnrm_scale Edit', scl)
                except RuntimeError:
                    self.report({'ERROR'},"Cannot apply to a multi user. Click:''Unlink'' ")
                    if self.unlo == 1:
                        bpy.ops.object.editmode_toggle()  # edit mode
                        strt()  # run def strt()
        if sedt == 'EDIT_MESH':
            strt()
#        bpy.ops.script.python_file_run(filepath= p + "OutNorm.py")
        return {"FINISHED"}

bpy.types.Scene.mbvl = bpy.props.EnumProperty(name ='',
    description = 'BEVEL',
    items=[
    ('BVLn2','BVLn2','+'),
    ('BVLnSingl','BVLnSingl','+')]
    )
class BVLn2(bpy.types.Operator):
    """bevel(offset=0.2, segments=2)
    SELECT EDGE LOOP | | | | | | |
    """
    bl_idname = "scene.bvln"
    bl_label = "Bevel 0.2"
    bl_options = {"REGISTER", "UNDO"}
    bts = bpy.props.FloatProperty(name="Depth/height", description="shrink_fatten", default=0.2)
    bss = bpy.props.IntProperty(name="Subiv", description="subd", default=2, min=0)
    dmns = bpy.props.BoolProperty(name="Invert", description="INV", default=0)
    brx = bpy.props.BoolProperty(name="RELAX", description="looptools_relax", default=False)
    brd = bpy.props.FloatProperty(name="Remove_doubles", description="dbls", default=0.0)


    def execute(self, context):
#        bpy.ops.script.python_file_run(filepath= p + "Bvl0,2.py")
        Ob = bpy.context.object.select
        adtt = bpy.context.mode

        if Ob == True:
            if adtt == 'EDIT_MESH':
                bpy.ops.mesh.subdivide(smoothness=0)
                bpy.ops.mesh.select_less()
                bpy.ops.mesh.bevel(
                offset=0.1,
                segments=self.bss,
                vertex_only=False
                )
                bpy.ops.mesh.select_less()
                bpy.ops.transform.shrink_fatten(value=(self.bts * -1) if self.dmns == 1 else self.bts)
                bpy.ops.mesh.remove_doubles(threshold=self.brd)
                if self.brx == True:
                    try:
                        bpy.ops.mesh.looptools_relax(input='selected', interpolation='linear', iterations='3', regular=False)
                    except AttributeError:
                        self.report({'ERROR'},"I'm sorry the addon 'Looptools' is not active or not installed.")

        return {"FINISHED"}

#----->"""Bevel_0.2"""
class BVLnSingl(bpy.types.Operator):
    """bevel(offset=0.2, segments=2) Var 2
    SELECT EDGE LOOP ========
    """
    bl_idname = "scene.bvlntwo"
    bl_label = "BnS_Plus"
    bl_options = {"REGISTER", "UNDO"}

    bofs = bpy.props.FloatProperty(name="Offset", description="offset", default=0.2)
    bts = bpy.props.FloatProperty(name="Depth/Height", description="shrink_fatten", default=0.2)
    bss = bpy.props.IntProperty(name="Subiv", description="subd", default=2,min=0)
    brd = bpy.props.FloatProperty(name="Remove_doubles", description="dbls", default=0.0)
    dsp = bpy.props.BoolProperty(name="Super_Dept", description="SDPT", default=0)
    bvs = bpy.props.FloatProperty(name="Bevel", description="BVL", default=0)
    dms = bpy.props.BoolProperty(name="Invert", description="INV", default=0)
    brx = bpy.props.BoolProperty(name="Relax", description="looptlsrlx", default=0)
    btr = bpy.props.FloatProperty(name="Bevel_Slide", description="bevel_slide", default=0.0)
    def execute(self, context):
        def edbl():
            """
            Bevel(0.2, 2 - subd)
            loop multi_select(False) edges
            """
            bpy.ops.transform.edge_slide(value=self.btr, mirror=False, correct_uv=False)
            bpy.ops.mesh.bevel(offset=self.bofs/2 , segments=self.bss , vertex_only=False)
            bpy.ops.mesh.select_less()
            bpy.ops.transform.shrink_fatten(value=(self.bts * -1) if self.dms == 1 else self.bts)
            bpy.ops.mesh.remove_doubles(threshold=self.brd)
            if self.brx == True:
                try:
                    bpy.ops.mesh.looptools_relax(input='selected', interpolation='linear', iterations='3', regular=False)
                except AttributeError:
                    self.report({'ERROR'},"I'm sorry the addon 'Looptools' is not active or not installed.")
            if self.dsp == 1:
                bpy.ops.mesh.bevel(offset=0.1, segments=2, vertex_only=False)
                bpy.ops.mesh.select_less()
                bpy.ops.transform.shrink_fatten(value=0.2, use_even_offset=False, mirror=False, proportional='CONNECTED',
                                                proportional_edit_falloff='SMOOTH', proportional_size=0.0839017)
        Ob = bpy.context.object.select
        adtt = bpy.context.mode
        if Ob == True and adtt == 'EDIT_MESH':
            edbl()
        if self.dsp == 1:
            self.bss = 2
            bpy.ops.mesh.bevel(offset=self.bvs, segments=1, vertex_only=False)
        return {"FINISHED"}

#----->"""Normal out"""
class normshow(bpy.types.Operator):
    """Normal out, show normal(0.6mm)"""
    bl_idname = "scene.normshow"
    bl_label = "Nout"
    bl_options = {"REGISTER", "UNDO"}

    nr = bpy.props.FloatProperty(
        name = "normal size",
        description = "normal size",
        default = 0.6,
        min=0.000,
        max=0.9
        )
#    nrmu = bpy.props.BoolProperty(
#        name="out",
#        description="Out",
#        default = 1
#        )
    def execute(self, context):
        nr1 = bpy.context.scene.tool_settings.normal_size = self.nr
        bpy.context.object.data.show_normal_vertex = True
        bpy.context.object.data.show_normal_loop = True
        bpy.context.space_data.show_backface_culling = True

        edm = bpy.context.mode
        if edm == 'OBJECT':
            bpy.ops.object.editmode_toggle()
        import bmesh
        mesh=bmesh.from_edit_mesh(bpy.context.object.data)
        for v in mesh.verts:
            v.select = False
        for v in mesh.edges:
            v.select = False
        for v in mesh.faces:
            v.select = False
        #   trigger viewport update
        bpy.context.scene.objects.active = bpy.context.scene.objects.active
        bpy.ops.mesh.select_all(action='TOGGLE')
        bpy.ops.mesh.normals_make_consistent(inside = 1)
        nr1
        bpy.ops.mesh.select_all(action='TOGGLE')
#        bpy.ops.script.python_file_run(filepath= p + "Normal_out_0.6.py")

        return {"FINISHED"}

#-----> """Bevel UP"""
class B_UP(bpy.types.Operator):
    """Apply and remove the "Bevel" modifier\nto the selected edges."""
    bl_idname = "scene.bup"
    bl_label = "BVL_UP"
    bl_options = {"REGISTER", "UNDO"}

    mlst = bpy.props.BoolProperty(
        name = "UpModifier",
        description = "To move the last of the list\nof modifiers at the top of the list",
        default = 0
        )
    bm0 = bpy.props.EnumProperty(
        items=[('Clear', 'Clear', 'Clear'),
               ('All adges', 'All adges', 'All adges'),
               ('Click', 'Click', 'Click')],
        name = "Clear_eddge",
        description = "Clear_eddge",
        default = 'Click'
        )
    bclmp = bpy.props.BoolProperty(
        name = "Clamp",
        description = "Use clamp overlap",
        default = 0
        )
    bedt = bpy.props.BoolProperty(
        name = "EDIT MODE",
        description = "View Bevel",
        default = 1
        )
    lst = bpy.props.FloatProperty(
        name="Bevel Weight",
        description="Mean Bevel Weight",
        default=1.0,
        max = 1.0
        )
    lst2 = bpy.props.FloatProperty(
        name="Bevel Value",
        description="Bevel Value",
        default=0.5,
        min=0.0
        )
    def execute(self, context):
        slo = bpy.context.selected_objects[0].name
        edm = bpy.context.mode
        bmf = bpy.context.object.modifiers.items() # list modifrs
        bmf2 = [i[0] for i in bmf] # a list of the names of the modifiers
        # name a last modifrs
        def sel(SEL):
            import bmesh
            """Here second seleted all vertex"""
            if edm != 'EDIT_MESH':
                bpy.ops.object.editmode_toggle()
            mesh = bmesh.from_edit_mesh(bpy.context.object.data)
            for v in mesh.verts:
                v.select = SEL
            for v in mesh.edges:
                v.select = SEL
            for v in mesh.faces:
                v.select = SEL
        def bvlprms():
            """Bevel parametrs for 'BUP'"""
            # cretate modifrs "BEVEL"
            bpy.ops.transform.edge_bevelweight(value=1)
            bpy.ops.object.modifier_add(type='BEVEL')
            bnm = bpy.context.object.modifiers[- 1].name
            # my paramtrs a "BEVEL"
            bpy.context.object.modifiers[bnm].use_clamp_overlap = self.bclmp
            bpy.context.object.modifiers[bnm].limit_method = 'WEIGHT'
            bpy.context.object.modifiers[bnm].width = self.lst2
            bpy.context.object.modifiers[bnm].segments = 6
            bpy.context.object.modifiers[bnm].show_in_editmode = self.bedt
            bpy.context.scene.objects.active = bpy.context.scene.objects.active
        def up_mod():
            bmf = bpy.context.object.modifiers.items()
            """move up modifier on the length of the list"""
            bnm = bpy.context.object.modifiers[-1].name  # name a last modifrs
            if len(bmf) >= 2:
                for i in range(len(bmf) - 1):
                    bpy.ops.object.modifier_move_up(modifier=bnm)
            bpy.context.object.modifiers[bnm].show_expanded = False
            self.mlst = 0

        if 'Bevel' in bmf2:
            if self.bclmp == 1:
                bpy.context.object.modifiers["Bevel"].use_clamp_overlap = True
            else:
                bpy.context.object.modifiers["Bevel"].use_clamp_overlap = False
        # EDITE MODE_BEVEL
        if 'Bevel' in bmf2: # CHECK FOR MODIFIER in the list and select the display mode
            if self.bedt == 1:  # EDITE MODE_BEVEL
                bpy.context.object.modifiers["Bevel"].show_in_editmode = True
            else:
                bpy.context.object.modifiers["Bevel"].show_in_editmode = False
                ##  EDGE_BEVELWEIGHT == ON
                #  if edm == "EDIT_MESH" and self.bm0 !=1:
                #      bpy.ops.transform.edge_bevelweight(value=1)
                #      bpy.ops.mesh.select_mode(use_extend=False, use_expand=True, type='EDGE')
                # if self.mlst !=1: # and self.bstp != 1:
        # EDGE_BEVELWEIGHT == OFF
        if edm == "EDIT_MESH" and self.bm0 =='Clear':
            bpy.ops.transform.edge_bevelweight(value=-1)
            self.bm0 = 'Click'
            self.lst = 0.0
            self.report({'INFO'}, "Clear Edge")
        ee = 0
        if self.bm0 =='All adges':
            if edm != "EDIT_MESH":
                ee = 1
            sel(True)
            bpy.ops.transform.edge_bevelweight(value=-1)
            bpy.ops.mesh.select_all(action='TOGGLE')
            self.bm0 = 'Click'
            self.lst = 0.0
            self.report({'INFO'}, "Clear All Edge")
        if ee == 1:
            bpy.ops.object.editmode_toggle()
            ee = 0
        if edm == "EDIT_MESH" and 'Bevel' in bmf2:
            bpy.ops.transform.edge_bevelweight(value=self.lst)
            if bpy.context.object.modifiers[0].name == "Bevel":
                bpy.context.object.modifiers[bpy.context.object.modifiers[0].name].width = self.lst2
        bch = 0
        bct = 0
        if bmf ==[]: # если спискок пуст запускаем функцию сохдания бевела
            bvlprms()
            bct = 1
        while bct !=1: # create "BEVEL" and UP in steck Р вычисляем длину списка
            it = bmf[bch][1].type
            if it != 'BEVEL':
                bch = bch+1
            if it == 'BEVEL':
                bct = 1
                break
            if bch >= len(bmf):
                bvlprms()
                print('add bevel')
                up_mod()
                #            self.bstp = 0
                bct = 1
                break

        if self.mlst ==1:
            up_mod()
        return {"FINISHED"}

#-----> """Select_Dupli"""
def srchs(self, context):
    NULL = {}  # выдаёт случайный порядок ключей
    sel = bpy.context.selected_objects  # список выделенных обьектов
    bpy.ops.object.select_all(action='TOGGLE')  #
    #name_NULL = []
    for i in range(len(sel)):
        sel[i].select = True
        seloc = sel[i].location.to_tuple(1)  # Coord_locaton
        el = sel[i].rotation_euler # Coord_Rotation
        selrot = el[0], el[1], el[2]  # -------
        dt = {'loc': str(seloc), 'rot': str(selrot)}  # dict
        sel[i].select = False
        NULL[str(sel[i].name)] = dt
        #name_NULL.append(str(sel[i].name))
##        print('\n\n')
    dupli = {}
    # print(NULL)
    ig = ( )
    for i in NULL:  # выбираем один элемент из "главного" списка(1действие)
        bc = NULL.copy()  # копия "главного" словаря
        it = NULL[i]  # получение значения ключа "главного" списка
        # print(i)
        del bc[i]  # # удаление ключа("самого себя")"i". можно bc.pop(i)
        for k in bc:  # выбираем один элемент из копии "главного" списка(n-действий)
            if not dupli.get(k):
                itc = bc[k]  # получение значения ключа оригинального списка
                if it == itc:  # сравнение списков
                    # print('i',i)
                    dupli[i] = NULL[i]  # одно действие
    def locrot(): # функция выделения
        for i in dupli:
            # dupli[i]
            bpy.data.objects[i].select = True

    def loca():
        single = []  # не дублируемые обьекты
        coord = []  # координаты location выделенных
        # sel = bpy.context.selected_objects
        for i in range(len(sel)):
            sel[i].select = True
        for i in range(len(sel)):
            vec = sel[i].location.to_tuple(1)
            if vec not in coord:
                coord.append(vec)
                single.append(sel[i])  # добавляем в список имена обьектов для выделения
        bpy.ops.object.select_all(action='TOGGLE')
        for i in range(len(sel)):
            if sel[i] not in single:
                sel[i].select = True
    if bpy.context.scene.Sdup == 'LOCAL':
        loca()
        self.report({'INFO'}, "LOC_MODE: I found %d objects" % len(bpy.context.selected_objects))
        print("LOC_MODE: %d objects" % len(bpy.context.selected_objects))
    if bpy.context.scene.Sdup == 'LOCAL_ROTATE':
        locrot()
        self.report({'INFO'}, "COMB_MODE:I found %d objects" % len(bpy.context.selected_objects))
        print("COMB_MODE: %d objects" % len(bpy.context.selected_objects))
    ##        def fortune(): # функция перемещения дубликатов
##            bpy.ops.transform.translate(value=(0, 0, -1.97685), constraint_axis=(False, False, True),
##                                        constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED',
##                                        proportional_edit_falloff='SMOOTH', proportional_size=8.95431,
##                                        release_confirm=True)
##            bpy.ops.scene.changobj()
##            bpy.context.object.draw_type = 'WIRE'
##            bpy.ops.object.copy_obj_drw()
##        print('\n\n\n', len(dupli), '\n\n', dupli, '\n\n', it)
    return {"FINISHED"}

bpy.types.Scene.Sdup = bpy.props.EnumProperty(
        items=[('LOCAL', 'LOCAL', 'Location of the objectL'),
                ('LOCAL_ROTATE', 'LOCAL_ROTATE', 'Location of the object & Rotation in Eulers')],
        name = "Search parameter",
        description = "Location of the object\n& Rotation in Eulers",
        update=srchs)
def listmatcap(self, context):
    if bpy.context.space_data.use_matcap == True:
        LM=bpy.context.scene.ListMCScene
        if LM >= 10:
            bpy.context.space_data.matcap_icon = '%s' %LM
        else:
            bpy.context.space_data.matcap_icon = '0'+'%s' %LM
    return {"FINISHED"}

bpy.types.Scene.ListMCScene = IntProperty(
        name = "MatCap List", 
        description = "ListMCScene",
        default = 1,
        min = 1, max = 24,
        update = listmatcap
        )

#-----> """Export_STL"""
class ExpS(bpy.types.Operator):
    """The export button to the "STL" format"""
    bl_idname = "scene.expos"
    bl_label = "Export_STL"
    bl_options = {"REGISTER", "UNDO"}

    def grp(self, g):
        '''Gruops list'''
        g = [(i.name, i.name, i.name) for i in bpy.context.active_object.users_group] if bpy.context.active_object.users_group != () else [('The list is empty', 'The list is empty', 'The list is empty')]
        return g
    def fldr(self, dr):
        '''Folder list'''
        dr = [('Select folder', 'Select folder', 'Select folder')]
        if os.path.dirname(bpy.data.filepath) !='':
            for d, dirs, files in os.walk(os.path.dirname(bpy.data.filepath)):
                for f in dirs:
                    # f = u'%s' % f
                    # d2 = (f, f, str(d+'\\'+f))
                    d2 = (f, f, d+'\\'+f)
                    dr.append(d2)
            # print('dr', '\n')
        # d0 = ('select', 'select', 'select')
        # dr.append(d0)
        return dr
    esg = bpy.props.BoolProperty(
        name="Use selection",
        default=True
        )
    esp = bpy.props.EnumProperty(
        items = [('Self', 'Self', 'Self'),
                ('"File"(Group)', '"File"(Group)', '"File"(Group)'),
                ('Group_Name', 'Group_Name', 'Group_Name'),
                ('Object_Name', 'Object_Name', 'Object_Name')],
        name="Use selection",
        default="Self")
    ell = bpy.props.EnumProperty(
        items=grp,
        name="Groups")
    enm = bpy.props.StringProperty(
        name="Name",
        default='')
    epth = bpy.props.StringProperty(subtype='FILE_PATH',
        name="FILE_PATH",
        default = '')
    edir = bpy.props.EnumProperty(
        items= fldr,
        name="Folder"
        )
    erun = bpy.props.BoolProperty(
        name="RUN",
        default=0
        )
    def execute(self, context):
        def dikt(dt):  # словарь определения пути по имени папки
            dik0 = {}
            if os.path.dirname(bpy.data.filepath) != '':
                for d, dirs, files in os.walk(os.path.dirname(bpy.data.filepath) + '\\'):
                    for f in dirs:
                        # f = r'%s' % f
                        dik0[f] = d
                        # print(dik0)
            return dik0.get(dt)
        df = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        act = bpy.context.active_object.name
        if self.esp == 'Group_Name':
            self.enm = ''
            if self.ell != 'The list is empty':
                self.enm = self.ell
            else:
                self.enm = ''
        if self.esp == 'Object_Name':
            self.enm = act
        if self.esp == '"File"(Group)':
            self.enm = ''
            if self.ell != 'The list is empty':
                self.enm = df + '(' + self.ell + ')'
        try:
            if self.fldr != 'Select folder':
                # self.epth = ''
                self.epth = str(dikt(dt=self.edir))+ '\\'+str(self.edir) + '\\'
                print('path',  self.epth)
        except UnicodeDecodeError:
            self.epth == ''
        if self.erun == 1:
            if self.enm == '':
                if self.epth == '' or self.epth == 'NoneSelect folder\\': # исключение: пустой путь
                    self.epth = os.path.dirname(bpy.data.filepath)+'\\'
                    self.enm = df
                    print(self.epth)
                else:
                    self.enm = df
            if '//' in self.epth: # проверка на "//"
                rep = self.epth.replace('//', '')
                self.epth = os.path.dirname(bpy.data.filepath)+'\\'+rep
                # self.epth = pt # изаменяем строку оригинальнального пути
            bpy.ops.export_mesh.stl(filepath=self.epth+self.enm+'.stl', check_existing=True, axis_forward='Y', axis_up='Z',
                                filter_glob="*.stl", use_selection=self.esg, global_scale=1, use_scene_unit=False,
                                ascii=False, use_mesh_modifiers=True, batch_mode='OFF')
            self.report({'INFO'}, "name   %s   patn:  %s" % (self.enm.replace('.blend', '') if self.enm !='' else '""', self.epth))
            self.erun = 0    
                
        return {'FINISHED'}

#-----> """ORGANIZER"""
class Matrix(bpy.types.Operator):
    """Organize objects"""
    bl_idname = "scene.mtrx"
    bl_label = "Organizer"
    bl_options = {"REGISTER", "UNDO"}

    mtc = bpy.props.IntProperty(name = "Count", description = "Count", default = 4, min=2)
    mtx = bpy.props.FloatProperty(name="X", description="X", default=8.0, min = 0.0)
    mty = bpy.props.FloatProperty(name="Y", description="Y", default=10, min = 0.0)
    mtp = bpy.props.BoolProperty(name="Propotional", description="Propotional", default=True)

    def execute(self, context):
        sel = bpy.context.selected_objects
        nup=1
        csel = 0
        #xx=bpy.data.objects[sel[0].name].location[0]
        #yy=bpy.data.objects[sel[0].name].location[1]
        selNull = sel[0]
        pp = bpy.data.screens[bpy.context.screen.name].areas[3].spaces[0].pivot_point
        bpy.data.screens[bpy.context.screen.name].areas[3].spaces[0].pivot_point = 'ACTIVE_ELEMENT'
        if sel != []:
            bpy.data.screens[bpy.context.screen.name].areas[3].spaces[0].use_pivot_point_align = True
            bpy.ops.transform.resize(value=(0, 0, 0),
            constraint_axis=(False, False, False),
            constraint_orientation='GLOBAL', mirror=False,
            proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
            bpy.data.screens[bpy.context.screen.name].areas[3].spaces[0].use_pivot_point_align = False
            bpy.ops.object.scale_clear()
        for i in sel:
            selNull.select = False
            csel = csel+1
            if i != selNull:
                if nup <=self.mtc-1:
                    nup = nup+1
                    # propotional
                    if self.mtp == 1:
                        self.mty = self.mtx
                        bpy.ops.transform.translate(value=(self.mtx, 0, 0),
                            constraint_axis=(False, False, False),
                            constraint_orientation='GLOBAL',
                            mirror=False, proportional='DISABLED',
                            proportional_edit_falloff='SMOOTH', proportional_size=1
                            )
                    else:
                        bpy.ops.transform.translate(value=(self.mtx, 0, 0),
                            constraint_axis=(False, False, False),
                            constraint_orientation='GLOBAL',
                            mirror=False, proportional='DISABLED',
                            proportional_edit_falloff='SMOOTH', proportional_size=1
                            )
                i.select = False
                try:
                    if nup == self.mtc:
                        nup = 1
                        bpy.ops.transform.translate(value=(-(self.mtx*(self.mtc-1)), self.mty, 0), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
                        selNull = sel[csel]
                except IndexError:
##                    self.report({'INFO'}, "End of the list")
                        continue
        return {'FINISHED'}



class AUTPanel(bpy.types.Panel):

    bl_label = "MASC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

#-----> """menu Draw Render & Simply"""
    def draw_header(self, context):
#-----> """buttom simplify"""
        rd = context.scene.render
        view = context.space_data
        # sympli On_Off
        self.layout.prop(rd, "use_simplify",text="",
        icon='POSE_HLT' if bpy.context.scene.render.use_simplify == True else 'ARMATURE_DATA'
        )
#-----> """buttom RenderView"""
        # ViewRender On_Off
        self.layout.prop(view, "show_only_render", text="",
        icon='RESTRICT_VIEW_OFF' if bpy.context.space_data.show_only_render == True else 'RESTRICT_VIEW_ON'
        )

        self.layout.prop(view, "use_matcap", text="",
        icon='MATCAP_%s' % bpy.context.space_data.matcap_icon if  bpy.context.space_data.use_matcap == True else 'MATCAP_01')

# SSAO
        view = context.space_data
        scene = context.scene
        gs = scene.game_settings
        obj = context.object
        fx_settings = view.fx_settings

        self.layout.prop(fx_settings, "use_ssao", text="",
        icon='LINK' if fx_settings.use_ssao else 'INLINK'
        )
#-----> """Draw subdiwision menu"""s
    def draw(self, context):
        layout = self.layout
        rd = context.scene.render          # shade menu ))
#        layout.active = rd.use_simplify
        split = layout.split()
        col = split.column()
        #-----> """WIRE_ZONE"""
        layout = self.layout
        obj = bpy.context.object
# ПОКА ОСТАВИТЬ ЭТОТ КУСОК ДЛЯ ДАЛЬНЕЙШЕГО РАЗБИРАТЕЛЬСТВА С ОШИБКАМИ!!!
        if obj:
            obj_type = obj.type
            is_geometry = (obj_type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'})
            is_wire = (obj_type in {'CAMERA', 'EMPTY'})
            is_empty_image = (obj_type == 'EMPTY' and obj.empty_draw_type == 'IMAGE')
            is_dupli = (obj.dupli_type != 'NONE')
            split = layout.split()
            col = split.column()
            col.prop(obj, "draw_type", text="")
            col = split.column(align=True)
            # Makes no sense for cameras, armatures, etc.!
            # but these settings do apply to dupli instances
            if is_geometry or is_dupli:
                col.prop(obj, "show_wire", text="W",) # text="Wire"
                col = split.column(align=True)
            if obj_type == 'MESH' or is_dupli:
                col.prop(obj, "show_all_edges", text="A")
                col = split.column(align=True)
            if is_geometry:
                col.prop(obj, "show_x_ray", text="X") # text="X-Ray"
#-----> """Draw SSAO menu"""
        view = context.space_data
        scene = context.scene
        gs = scene.game_settings
        obj = context.object
        fx_settings = view.fx_settings
        if view.viewport_shade not in {'BOUNDBOX', 'WIREFRAME'}:
            sub = col.column()
            sub.active = view.region_3d.view_perspective == 'CAMERA'
            if fx_settings.use_ssao:
                ssao_settings = fx_settings.ssao
                col.column(align=True)
                subcol = split.column(align=True)
                subcol.prop(ssao_settings, "factor")
                subcol = split.column(align=True)
                subcol.prop(ssao_settings, "distance_max")
                subcol = split.column(align=True)
                subcol.prop(ssao_settings, "samples")


#-----> """Draw AUTO menu"""
        row = layout.row()
        layout = self.layout
        split = layout.split()
        col = split.column(align=True)
        slct = bpy.context.selected_objects
        edm = bpy.context.mode
        ob = context.object
        if bpy.context.scene.render.use_simplify == True:
            # if bpy.context.space_data.use_matcap != True:
            #     col = layout
            row.prop(rd, "simplify_subdivision", text="Subdivision")
            # col = split.column(align=False)
        if  bpy.context.space_data.use_matcap == True:
            row.prop(scene, 'ListMCScene')
        if edm != 'SCULPT':
            col.operator("scene.autorend", text="RL", icon="RENDERLAYERS")
            col = split.column(align=True)
            col.operator("scene.kursor", text="XYZ", icon="CURSOR")
            col = split.column(align=True)
#            col.operator("scene.gradobj", text="Grad", icon="DOTSUP")
#            cl.prop(scene, 'movebgr', icon='ZOOM_ALL')
            col.prop(scene, 'CurvBox', icon='IPO_BEZIER' if bpy.context.scene.CurvBox == 0 else 'DOWNARROW_HLT', text = 'SBox')
            split = layout.split()
            if edm == 'OBJECT':
                col = split.column(align=True)
        try:
            tp = bpy.context.selected_objects[0].type
        except IndexError:
            tp = 0
        if edm == 'SCULPT':
            split = layout.split()
            col = split.column(align=True)

        # Name Brush
        aname = bpy.context.scene.tool_settings.sculpt.brush.name
        # Create a pattern brush in quotes
        if slct != []:
            if tp == 'EMPTY':
                layout.operator("scene.rempty", text="Name", icon="OUTLINER_OB_EMPTY")
##                if ob.dupli_type == 'GROUP':
##                    layout.prop(ob, "dupli_group", text="Group")
                col.operator("scene.grpnmimts", text="Gruop", icon="GROUP")
            if tp != 'EMPTY' and edm!='EDIT_MESH'and edm !='EDIT_CURVE':
                Btool = "%s" % aname + ""
                if edm == 'SCULPT':
                    col = layout
                col.operator("scene.scdint", text="DIN" if edm != 'SCULPT' else Btool,
                            icon="BRUSH_FILL" if edm != 'SCULPT' else 'SCULPTMODE_HLT')
                if edm != 'SCULPT':
                    subcol = col.row(align=True)
                    subcol.operator("scene.normshow", text="Nout", icon="INLINK")
                    subcol.operator("scene.rscnrm", text="Restore", icon="MESH_ICOSPHERE")
                    col.operator("scene.grpnmimts", text="Gruop", icon="GROUP")
                    nmc=bpy.context.selected_objects[0].name
                    col.operator("scene.gradobj", text="Grad", icon="DOTSUP")
        if slct != []:
            col = split.column(align=True)

        if slct != [] and edm == 'OBJECT':
            if tp != 'EMPTY':
                row = layout.row(align=True)
                col.operator("scene.expos", text='STL' , icon="EXPORT")
                col.operator("scene.apjion", text="JO", icon="OBJECT_DATAMODE")
                col.prop(scene, 'Sdup', text="", icon="VIEWZOOM")
            subcol = col.row(align=True)
            subcol.operator("scene.robject", text="Rot&Dub", icon="FORCE_VORTEX")
            subcol.prop(scene, 'fastrnd')


#-----> """Block EDIT_MESH"""
        if edm == 'EDIT_MESH':
            # split = layout.split(percentage=0.0, align=True)
            col.operator("scene.rscnrm", text="Restore", icon="MESH_ICOSPHERE")
            col = split.column(align=True)
#            col.prop(scene, 'mbvl', text="Bv | |", icon="EDGESEL")
#            col = split.column(align=True)
            col.operator("scene.bvln", text="Bv | |", icon="EDGESEL")
            col = split.column(align=True)
            col.operator("scene.bvlntwo", text="Bv ==", icon="EDGESEL")
            col = split.column(align=True)
            col.operator("scene.dissol", text="DS", icon="SNAP_VERTEX")
            col = split.column(align=True)
            col.operator("scene.bup", text="BUP", icon="MOD_BEVEL")
# Panel_("Gruop")
        layout = self.layout
        ob = context.object

        layout.prop(ob, "dupli_type", expand=True)

        if ob.dupli_type == 'FRAMES':
            split = layout.split()

            col = split.column(align=True)
            col.prop(ob, "dupli_frames_start", text="Start")
            col.prop(ob, "dupli_frames_end", text="End")

            col = split.column(align=True)
            col.prop(ob, "dupli_frames_on", text="On")
            col.prop(ob, "dupli_frames_off", text="Off")

            layout.prop(ob, "use_dupli_frames_speed", text="Speed")

        elif ob.dupli_type == 'VERTS':
            layout.prop(ob, "use_dupli_vertices_rotation", text="Rotation")

        elif ob.dupli_type == 'FACES':
            row = layout.row()
            row.prop(ob, "use_dupli_faces_scale", text="Scale")
            sub = row.row()
            sub.active = ob.use_dupli_faces_scale
            sub.prop(ob, "dupli_faces_scale", text="Inherit Scale")

        elif ob.dupli_type == 'GROUP':
            layout.prop(ob, "dupli_group", text="Group")
#        layout.prop(scene, 'CurvBox', icon='IPO_BEZIER' if bpy.context.scene.CurvBox == 0 else 'DOWNARROW_HLT', text = 'SBox')
        if bpy.context.scene.CurvBox == True:
            layout.prop(scene, 'EdgConvert', icon='SNAP_EDGE', text='Curver')
            if bpy.context.selected_objects[0].type == 'CURVE':
                layout.prop(scene, 'SerSpline', icon='IPO_QUINT', text = 'Separator')
                layout.prop(scene, 'joincrv', icon='IPO_CIRC', text='Connector')
                if edm !='EDIT_MESH':
                    if edm != 'SCULPT':
                        layout.operator("scene.crlwo", text='CW' , icon="MESH_TORUS")
        
#-----> """End"""

def register():
    bpy.utils.register_class(QuickMirror)
    bpy.utils.register_class(QuickShrink)
    bpy.utils.register_class(Matrix)
    bpy.utils.register_class(ExpS)
    bpy.utils.register_class(Crlwo)
    bpy.utils.register_class(Robject)
    bpy.utils.register_class(Gradobj)
    bpy.utils.register_class(kurs)
    bpy.utils.register_class(AUTPanel)
    bpy.utils.register_class(SculptMyDint)
    bpy.utils.register_class(OpsRenderLrs)
    bpy.utils.register_class(GruopForNameItems)
    bpy.utils.register_class(App_NmLink_ToEmpty)
    bpy.utils.register_class(Sacle_Nrml)
    bpy.utils.register_class(BVLn2)
    bpy.utils.register_class(normshow)
    bpy.utils.register_class(AplyJion)
    bpy.utils.register_class(dissol)
    bpy.utils.register_class(changobj)
    bpy.utils.register_class(BVLnSingl)
    bpy.utils.register_class(B_UP)
    bpy.utils.register_class(MASCSelection)

def unregister():
    bpy.utils.unregister_class(QuickMirror)
    bpy.utils.unregister_class(QuickShrink)
    bpy.utils.unregister_class(MASCSelection)
    bpy.utils.unregister_class(B_UP)
    bpy.utils.unregister_class(BVLnSingl)
    bpy.utils.unregister_class(changobj)
    bpy.utils.unregister_class(dissol)
    bpy.utils.unregister_class(AplyJion)
    bpy.utils.unregister_class(normshow)
    bpy.utils.unregister_class(BVLn2)
    bpy.utils.unregister_class(Sacle_Nrml)
    bpy.utils.unregister_class(App_NmLink_ToEmpty)
    bpy.utils.unregister_class(GruopForNameItems)
    bpy.utils.unregister_class(OpsRenderLrs)
    bpy.utils.unregister_class(SculptMyDint)
    bpy.utils.unregister_class(AUTPanel)
    bpy.utils.unregister_class(kurs)
    bpy.utils.unregister_class(Gradobj)
    bpy.utils.unregister_class(Robject)
    bpy.utils.unregister_class(Crlwo)
    bpy.utils.unregister_class(ExpS)
    bpy.utils.unregister_class(Matrix)

if __name__ == "__main__":
   register()
