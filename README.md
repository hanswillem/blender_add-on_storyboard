# Blender Add-On Storyboard

A simple add-on to make creating storyboards in Blender a little easier. 
To use it, the blendfile must be saved, and you need to place markers in the timeline to divide the scene into shots. Don't forget to place a marker at the end of the last shot.

### Setup Viewport
Creates a camera, sets the viewport display to *Only Render* and *World Background*.

### Open Folder
Opens the folder where the blendfile is saved in the finder.

### Images - Export All
Exports the images to the folder where the blendfile is saved. The length of the shot is stamped into the image.
Note that it does this based on the shots (i.e. the markers) and not on the keyframes!

### Images - Export Individual
Exports the image that is currently in the viewport to the folder where the blendfile is saved. 

### Audio - Export All
Exports the audio as clips based on the shots to the folder where the blendfile is saved.

### Audio - Export Individual
Exports the audio clips based on the shot currently under the playhead to the folder where the blendfile is saved.
