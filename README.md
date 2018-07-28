# Blen64
Blender scripts to convert and export mesh objects to draw lists as C header files for use with the n64 SDK
![Mesh output example](https://cdn.discordapp.com/attachments/445463417797738496/472802908803563540/unknown.png "BrickWall")

# V2.1 - beta
# Change log:
- Added UV support(seams)
- Fixed poly buffer limit issues
- Completely rewritten algorithm that generates the Vert and Face lists from UV poly loop indices allowing for more complex sorting.
- Totally messed up shading :P
Cautionary Note: Blen64 in it's current state is extremely unequipped to optimize for poly count, that is to say IT WILL EAT UP YOUR VETEX BUDGET, in short it because we are building draw lists from poly loop indices we end up with duplicate vertices, essentially there are duplicate vertices for every face connected to a point, in turn faces aren't technically connected(hence the weird shading effect since surfaces cant be smoothed). This shouldn't be a problem for long and I have a couple different solutions in the works.
