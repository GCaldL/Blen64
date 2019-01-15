# Blen64
Blender scripts to convert and export mesh objects to draw lists as C header files for use with the n64 SDK
![Mesh output example](https://cdn.discordapp.com/attachments/445463417797738496/473893698539618314/unknown.png "Room")

# V2.2 - beta
# Change log:
- Added options to export panel
- Apply transformations
- Descend heirarchies of objects
- Only converts selected objects that are meshes
- No longer crashes when UVMap/Vertex Colors are not present
- Always outputs valid C identifiers
- Exports all objects selected in the scene
- Uses Export Menu now instead of requiring the user to run a script
- Fixed poly buffer limit issues
- Added Vertex Color Support
- Fixed missing vert/face disarray issue
- Cleaned up some code

# Usage:
1.<Setup>
Copy the io\_scene\_n64dl folder to your Blender installation's addons folder. Then enable the addon under settings. To run the script, select the objects you wish to export and choose N64 DL from the export menu. ![Setup](https://media.discordapp.net/attachments/434689798817579008/473758873191448576/unknown.png?width=1435&height=898 "Blender")

# Cautionary Note:
Blen64 in it's current state is extremely unequipped to optimize for poly count, that is to say IT WILL EAT UP YOUR VETEX BUDGET, in short it because we are building draw lists from poly loop indices we end up with duplicate vertices, essentially there are duplicate vertices for every face connected to a point, in turn faces aren't technically connected(hence the weird shading effect since surfaces cant be smoothed). This shouldn't be a problem for long and I have a couple different solutions in the works.

# Feature Roadmap:
- Fix the last of the SAIFAV(super annoying incorrect faces and vertices) bugs.
- integrate render modes(opaque, translucent, cutout etc.)
- possible auto save to header
- Triangulate non-destructively :)