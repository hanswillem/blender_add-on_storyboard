# Blender Add-On Storyboard

### A simple add-on to make creating storyboards in Blender a little easier. To use it, the blendfile must be saved, there must be a camera in the scene and you need to place markers in the timeline to divide the scene into shots. Don't forget to place a marker at the end of the last shot.

### Blender 2.80 version

#### Export Single Image
Exports a single image to the folder where the blendfile is saved. 
The name of the image will be the same as the marker name of the shot.

#### Export All Images
Exports the images to the folder where the blendfile is saved. 
The names of the images will be the same as the marker names of the shot.

#### Export Audioclips
Exports the audio as clips based on the shots (i.e. the markers) to the folder where the blendfile is saved.

#### Export H264
Exports the full timeline as an mp4 (h264).

#### Open Folder
Opens the folder where the blendfile is saved.

---

### Blender 2.79 version

#### Setup Viewport
Creates a camera, sets the viewport display to *Only Render* and *World Background*.

#### Open Folder
Opens the folder where the blendfile is saved.

#### Images - Export Sequence
Exports the whole timeline (from the first to the last marker) as a png sequence to the folder where the blendfile is saved.

#### Images - Export Shots
Exports the images to the folder where the blendfile is saved. The length of the shot is stamped into the image.
Note that it does this based on the shots (i.e. the markers) and not on the keyframes!

#### Images - Export Current
Exports the image that is currently in the viewport to the folder where the blendfile is saved. 

#### Audio - Export Mixdown
Exports the whole timeline as audio mixdown to the folder where the blendfile is saved.

#### Audio - Export Shots
Exports the audio as clips based on the shots (i.e. the markers) to the folder where the blendfile is saved.

#### Audio - Export Current
Exports the audio clips based on the shot currently under the playhead to the folder where the blendfile is saved.
