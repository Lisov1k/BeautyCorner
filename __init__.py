bl_info = {
    "name": "BeautyCorner",
    "author": "Lisovik Alexandr",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > BeautyCorner",
    "description": "Simplifies the creation of mirror cuts at custom angles.",
    "warning": "",
    "category": "Object",
}

import importlib
import bpy
from . import mirror_tool

def register():
    importlib.reload(mirror_tool)
    mirror_tool.register()

def unregister():
    mirror_tool.unregister()

if __name__ == "__main__":
    register()
