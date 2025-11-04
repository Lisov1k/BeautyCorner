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
from . import Beauty_Corner

def register():
    importlib.reload(Beauty_Corner)
    Beauty_Corner.register()

def unregister():
    Beauty_Corner.unregister()

if __name__ == "__main__":
    register()
