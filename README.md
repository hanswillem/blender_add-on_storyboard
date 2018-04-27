# Blender Add-on Storyboard

A simple add-on to make creating storyboards in Blender a little easier. 

To use it:
1. Create a storyboard with grease pencil (if necessary import audio).
2. Place markers to divide the storyboard into shots (don't forget to place a marker at the end of the last shot).
3. Save the blendfile to disk.
4. Now you can use the buttons of the add-on to export images and sound.

### Setup Viewport
Creates a camera, sets the viewport display to *Only Render* and *World Background*.

### Open Folder
Opens the folder where the blendile is saved in the finder.

### Images - Export All
Exports the images to the folder where the blendfile is saved.
Note that it does this based on the shots (i.e. the markers) and not on the keyframes!

### Images - Export Individual
Exports the image that is currently in the viewport to folder where the blendfile is saved.

### Audio - Export All
Exports the audio as clips based on the shots to the folder where the blendfile is saved.

### Audio - Export Individual
Exports the audio clips based on the shot currently under the playhead to the folder where the blendfile is saved.
