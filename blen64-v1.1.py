import os
import bpy

#options
s = 100 #scale constan
tsize = 6 #texture size
loadlim = 32 #ammount of polgons the sytem will load at a time
offset = 0

bpy.ops.text.new()
bpy.data.texts["Text"].name = "out"
o = bpy.data.texts["out"]

obj = bpy.context.active_object
name = obj.name

vert = obj.data.vertices
poly = obj.data.polygons
uv = obj.data.uv_layers.active

#Info
o.write("/*\nModel: %s \n" % name)
o.write("Verts: %s \n" % len(vert))
o.write("Tris: %s \n" % len(poly))
o.write("Exported from blender using blen64.\n")
o.write("Github link.*/\n\n")

#Vertex List
o.write("Vtx %s_VertList[] = {\n" % name)
for i in range(len(vert)):
    vx = round(vert[i].co[0], 2)
    vy = round(vert[i].co[1], 2)
    vz = round(vert[i].co[2], 2)
    u = round(uv.data[i].uv[0], 2)
    v = round(uv.data[i].uv[1], 2)
    #vert pos: x,y,z, unused coord?, UVs: u, v, vertex colors: r,b,g,a)
    o.write("   { %.2f, %.2f, %.2f, 0, %i << 6, %i << 6, 255, 255, 255, 255},\n" % (vx*s, vy*s, vz*s, u*32, (1-v)*32))
o.write("};\n\n")

#Face List
o.write("Gfx %s_PolyList[] = {\n" % name)
o.write("   gsSPVertex(%s_VertList+%d,%d,0),\n" % (name, 0, loadlim)) #load the first x number of vertices
for i in range(len(poly)):
    v1 = poly[i].vertices[0]
    v2 = poly[i].vertices[1]
    v3 = poly[i].vertices[2]
    vl = [v1, v2, v3]

    #if the face being created contains a vert that has not been loaded into the buffer
    if max(vl) > offset+loadlim:
        offset = i
        o.write("   gsSPVertex(%s_VertList+%d,%d,0),\n" % (name, offset, loadlim))
    
    #build faces:
    o.write("   gsSP1Triangle(%d, %d, %d, %d),\n" % (v1, v2, v3, v1))
o.write("};\n\n")
