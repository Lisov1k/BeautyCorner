bl_info = {
    "name": "BeautyCorner Mirror Tool",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > BeautyCorner",
    "description": "Simplifies the creation of mirror cuts at custom angles.",
    "warning": "",
    "category": "Object",
}

import importlib
import bpy
from . import beauty_corner_mirror

def register():
    importlib.reload(beauty_corner_mirror)
    beauty_corner_mirror.register()

def unregister():
    beauty_corner_mirror.unregister()

if __name__ == "__main__":
    register()
