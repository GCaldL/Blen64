bl_info = {
  "name": "N64 Display List exporter",
  "description": "Export to N64 Display List",
  "author": "GCaldL",
  "version": (2, 2, 0),
  "blender": (2, 79, 0),
  "warning": "",
  "location": "File > Import-Export",
  "wiki_url": "",
  "tracker_url": "",
  "support": "COMMUNITY",
  "category": "Import-Export" }
    
# Blen64 v2.2
# now with vetex colors!!

import bpy
import os
import random
import string
import math

def descends(parents, child):
  while child and child not in parents:
    child = child.parent
  return child != None

class ExportDL(bpy.types.Operator):
  bl_idname = "export.n64_dl"
  bl_label = "Export N64 DL"
  
  scale = bpy.props.FloatProperty(
    name        = "Scale",
    description = "Scalar multiplier.",
    default     = 100.0,
    min         = 0.01,
    max         = 1000.0,
    precision   = 2)
  twidth = bpy.props.FloatProperty(
    name        = "Texture Width",
    description = "Texture width in texels.",
    default     = 32.0,
    min         = 1.0,
    max         = 1024.0,
    precision   = 1
  )
  theight = bpy.props.FloatProperty(
    name        = "Texture Height",
    description = "Texture height in texels.",
    default     = 32.0,
    min         = 1.0,
    max         = 1024.0,
    precision   = 1
  )
  
  filepath = bpy.props.StringProperty(subtype="FILE_PATH")
  
  names = {}
  def clean_name(self, name):
    # Only take the characters from the name that are valid for C identifiers.
    # Note that this makes it possible to have a duplicate, so we test against all
    # previous names before using.
  
    name = "".join(c for c in name if
      c in string.ascii_letters or
      c in string.digits or
      c == '_')
    if len(name) == 0 or name[0] in string.digits:
      name = "_" + name
  
    if name in self.names:
      self.names[name] += 1
      name += "_" + str(self.names[name])
    else:
      self.names[name] = 1
    return name

  def export(self, o, obj):
    bitshift = 6 # Bitshift mod
    loadlim = 15 # Ammount of verts the sytem will load at a time 32 max limit
    
    trans = bpy.context.object.matrix_world
    
    name = self.clean_name(obj.name)
    vert = obj.data.vertices
    poly = obj.data.polygons
    uv = obj.data.uv_layers.active

    ###Triangulate
    #Check for polys w/ more than 3 verts
    for p in poly:
        if len(p.vertices) > 3:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
            bpy.ops.object.mode_set(mode='OBJECT')
            break
    
    #Info
    o.write("/*\nModel: %s \n" % name)
    o.write("Verts: %s \n" % len(vert))
    o.write("Tris: %s \n" % len(poly))
    o.write("Exported from blender using blen64.\n")
    o.write("github.com/GCaldL/Blen64/\n*/\n")

    #Vertex List
    o.write("Vtx %s_VertList[] = {\n" % name)
    for face in poly:
        for vert, loop in zip(face.vertices, face.loop_indices):
            coord = obj.data.vertices[vert].co * obj.matrix_world
            uv = obj.data.uv_layers.active.data[loop].uv if obj.data.uv_layers.active else (0,0)
            vcol = obj.data.vertex_colors.active.data[loop].color if obj.data.vertex_colors.active else (1,1,1,1)
            o.write("   { %.2f, %.2f, %.2f, %i, %i << 6, %i << 6, %i, %i, %i, %i},\n"
              % (coord.x*self.scale, coord.y*self.scale, coord.z*self.scale, 1,
                 uv[0]*self.twidth, (1-uv[1])*self.theight,
                 vcol[0]*255, vcol[1]*255, vcol[2]*255, 255))
    o.write("};\n\n")

    #Face List
    o.write("Gfx %s_PolyList[] = {\n" % name)
    o.write("   gsSPVertex(%s_VertList+%d,%d,0),\n" % (name, 0, loadlim)) #load the first x number of vertices
    i = 0
    offset = 0
    for face in poly:
        #if the face being created contains a vert that has not been loaded into the buffer
        if i*3+2 > offset+loadlim:
            offset = i*3
            o.write("   gsSPVertex(%s_VertList+%i,%i,%i),\n" % (name, offset, loadlim, 0))
    
        #build faces:
        o.write("   gsSP1Triangle(%d, %d, %d, %d),\n" % (i*3-offset, i*3+1-offset, i*3+2-offset, i*3-offset))
        i += 1
    o.write("   gsDPPipeSync(),\n")
    o.write("   gsSPEndDisplayList(),\n")
    o.write("};\n\n")

  def execute(self, context):
    names = {}
    bpy.ops.object.mode_set(mode='OBJECT')
    file = open(self.filepath, 'w')
    for obj in bpy.context.scene.objects:
      if obj.type == 'MESH' and descends(bpy.context.selected_objects, obj):
        self.export(file, obj)
    return {'FINISHED'}
    
  def invoke(self, context, event):
    context.window_manager.fileselect_add(self)
    return {'RUNNING_MODAL'}
  
def menu_func(self, context):
  self.layout.operator_context = 'INVOKE_DEFAULT'
  self.layout.operator(ExportDL.bl_idname, text="N64 DL Export")
  
def register():
  bpy.utils.register_class(ExportDL)
  bpy.types.INFO_MT_file_export.append(menu_func)
  
def unregister():
  bpy.types.INFO_MT_file_export.remove(menu_func)
