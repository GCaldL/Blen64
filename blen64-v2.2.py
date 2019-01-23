# Blen64 v2.2
# now with vetex colors!!

import bpy
import os
import random
import string

s =  100 #scale constant
bitshift = 6 #bitshift mod
tsize = 32 #texture size in pixels
loadlim = 30 #ammount of verts the sytem will load at a time 32 max limit

bpy.ops.text.new()
o = bpy.data.texts["Text"]
o.name = "meshout"

def clean_name(name):
  # Only take the characters from the name that are valid for C identifiers.
  # Note that this makes it possible to have a duplicate, so we test against all
  # previous names before using.
  
  name = "".join(c for c in obj.name if
    c in string.ascii_letters or
    c in string.digits or
    c == '_')
  if len(name) == 0 or name[0] in string.digits:
    name = "_" + name
  return name

def export(obj):
  name = clean_name(obj.name)
  vert = obj.data.vertices
  poly = obj.data.polygons
  uv = obj.data.uv_layers.active

  #Info
  o.write("/*\nModel: %s \n" % name)
  o.write("Verts: %s \n" % len(vert))
  o.write("Tris: %s \n" % len(poly))
  o.write("Exported from blender using blen64.\n")
  o.write("github.com/GCaldL/Blen64/\n*/\n")

  ###Triangulate
  #Check for polys w/ more than 3 verts
  for p in poly:
      if len(p.vertices) > 3:
          bpy.ops.object.editmode_toggle()
          bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
          bpy.ops.object.editmode_toggle()
          break

  #Vertex List
  o.write("Vtx %s_VertList[] = {\n" % name)
  for face in poly:
      for vert, loop in zip(face.vertices, face.loop_indices):
          coord = obj.data.vertices[vert].co
          uv = obj.data.uv_layers.active.data[loop].uv if obj.data.uv_layers.active else (0,0)
          vcol = obj.data.vertex_colors.active.data[loop].color if obj.data.vertex_colors.active else (1,1,1,1)
          o.write("   { %.2f, %.2f, %.2f, %i, %i << 6, %i << 6, %i, %i, %i, %i},\n" % (coord.x*s, coord.y*s, coord.z*s, random.randint(0,255), uv[0]*tsize, (1-uv[1])*tsize, vcol[0]*255, vcol[1]*255, vcol[2]*255,random.randint(0,255)))
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
          o.write("   gsSPVertex(%s_VertList+%i,%i,%i),\n" % (name, offset, loadlim, offset))
    
      #build faces:
      o.write("   gsSP1Triangle(%d, %d, %d, %d),\n" % (i*3, i*3+1, i*3+2, i*3))
      i += 1
  o.write("};\n\n")


for obj in bpy.context.selected_objects:
  export(obj)