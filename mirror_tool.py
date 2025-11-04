import bpy
import math

bl_info = {
    "name": "BeautyCorner",
    "author": "Lisovik Alexandr",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > BeautyCorner",
    "description": "Creates a Mirror modifier with the correct slice angle and the Flip Y button.",
    "category": "Object",
}


# ---------------------- PROPERTIES ----------------------
class BeautyCornerProperties(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty(
        name="Angle (°)",
        description="The entered value is the rotation angle. The cut will be made at (angle/2). For example: visual rotation by 90° corresponds to 45° of cutting angle.",
        default=45.0,
        min=-180.0,
        max=180.0,
        step=1,
        precision=1,
    )


# ---------------------- OPERATORS ----------------------
class OBJECT_OT_BeautyCreateMirror(bpy.types.Operator):
    bl_idname = "object.beauty_create_mirror"
    bl_label = "Create Mirror"
    bl_description = "Create Empty and Mirror modifier"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.beauty_corner_props
        angle = props.angle
        obj = context.active_object

        if not obj:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}

        # Создаём пустышку
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=obj.location)
        empty = context.active_object

        angle_name = int(round(angle))
        empty.name = f"Beauty_{angle_name}_Empty"

        # Поворачиваем пустышку
        empty.rotation_euler[2] = math.radians(angle / 2.0)

        # Возвращаем активный объект
        context.view_layer.objects.active = obj

        # Удаляем старый модификатор, если есть
        mod_name = f"Beauty_{angle_name}"
        if mod_name in obj.modifiers:
            obj.modifiers.remove(obj.modifiers[mod_name])

        # Создаём Mirror
        mirror_mod = obj.modifiers.new(name=mod_name, type='MIRROR')
        mirror_mod.use_axis = (False, True, False)       # только Y
        mirror_mod.use_bisect_axis[1] = True             # разрез по Y
        mirror_mod.use_mirror_merge = True
        mirror_mod.use_bisect_flip_axis[1] = False       # Flip Y выключен по умолчанию
        mirror_mod.mirror_object = empty

        self.report({'INFO'}, f"Created modifier: {mod_name} and empty: {empty.name}")
        return {'FINISHED'}


class OBJECT_OT_BeautyFlip(bpy.types.Operator):
    bl_idname = "object.beauty_flip"
    bl_label = "Flip (Toggle Flip Y)"
    bl_description = "Switches Flip Y in mirror modifier Beauty_*"

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}

        target_mod = None
        for mod in obj.modifiers:
            if mod.name.startswith("Beauty_") and mod.type == 'MIRROR':
                target_mod = mod
                break

        if not target_mod:
            self.report({'ERROR'}, "Mirror Beauty_* not found")
            return {'CANCELLED'}

        # Переключаем Flip Y (use_bisect_flip_axis)
        current_state = target_mod.use_bisect_flip_axis[1]
        target_mod.use_bisect_flip_axis[1] = not current_state
        new_state = target_mod.use_bisect_flip_axis[1]

        state_text = "ВКЛ" if new_state else "ВЫКЛ"
        self.report({'INFO'}, f"Flip Y: {state_text}")
        return {'FINISHED'}


class OBJECT_OT_BeautyApplyMirror(bpy.types.Operator):
    bl_idname = "object.beauty_apply_mirror"
    bl_label = "Apply Mirror"
    bl_description = "Applies a mirror (Beauty*) and removes the auxiliary Empty."

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}

        target_mod = None
        for mod in obj.modifiers:
            if mod.name.startswith("Beauty_") and mod.type == 'MIRROR':
                target_mod = mod
                break

        if not target_mod:
            self.report({'ERROR'}, "Mirror modifier not found")
            return {'CANCELLED'}

        empty = target_mod.mirror_object

        try:
            bpy.ops.object.modifier_apply(modifier=target_mod.name)
        except RuntimeError as e:
            self.report({'ERROR'}, f"Couldn't apply modifier: {e}")
            return {'CANCELLED'}

        if empty and empty.name in bpy.data.objects:
            if context.view_layer.objects.active == empty:
                context.view_layer.objects.active = obj
            bpy.data.objects.remove(empty, do_unlink=True)

        self.report({'INFO'}, "Mirror applied, Empty removed")
        return {'FINISHED'}


# ---------------------- UI PANEL ----------------------
class VIEW3D_PT_BeautyCornerPanel(bpy.types.Panel):
    bl_label = "Mirror Tool"
    bl_idname = "VIEW3D_PT_beauty_corner_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BeautyCorner"

    def draw(self, context):
        layout = self.layout
        props = context.scene.beauty_corner_props

        layout.prop(props, "angle")
        row = layout.row(align=True)
        row.operator("object.beauty_create_mirror", icon='MOD_MIRROR')
        row.operator("object.beauty_flip", icon='ARROW_LEFTRIGHT')
        layout.operator("object.beauty_apply_mirror", icon='CHECKMARK')


# ---------------------- REGISTER ----------------------
classes = (
    BeautyCornerProperties,
    OBJECT_OT_BeautyCreateMirror,
    OBJECT_OT_BeautyFlip,
    OBJECT_OT_BeautyApplyMirror,
    VIEW3D_PT_BeautyCornerPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.beauty_corner_props = bpy.props.PointerProperty(type=BeautyCornerProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.beauty_corner_props


if __name__ == "__main__":
    register()
