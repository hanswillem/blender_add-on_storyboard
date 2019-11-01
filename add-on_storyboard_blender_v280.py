
bl_info = {
    'name' : 'Storyboard',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 1),
    'blender' : (2, 81, 0  ),
    'location' : 'View 3D > Tools > Storyboard',
    'description' : 'Tools for storyboarding',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Storyboard'
    }
 
#imports
import bpy
import subprocess

def main_openFolder():
    subprocess.Popen('explorer ' + bpy.path.abspath('//'))
    
def main_getLeadingZeroes():
    l = len(bpy.context.scene.timeline_markers)
    lz = len(str(l))
    if lz == 1:
        lz = 2
    return str(lz)

def main_getShotNumberOfFrame(f):
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()

    for i in range(len(mrks) - 1):
        if f >= mrks[-1]:
            return len(mrks)
        if mrks[i] <= f < mrks[i + 1]:
            return i + 1

def main_getMarkerNameOfFrame(f):
    # make a dictionary of marker framenumbers and markernames
    d_mrks = {}
    for i in  bpy.context.scene.timeline_markers:
        d_mrks[i.frame] = i.name
    # make a list of the framenumbers and sort them
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    # get the marker name and return it
    for i in range(len(mrks) - 1):
        if f >= mrks[-1]:
            return d_mrks[mrks[-1]]
        if mrks[i] <= f < mrks[i + 1]:
            return  d_mrks[mrks[i]]

#PNG settings
def main_setPNG():
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.use_file_extension = True

#h264 settings
def main_setH264():
    bpy.context.scene.render.use_file_extension = False
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.ffmpeg.gopsize = 1
    #turn on the audio
    bpy.context.scene.render.ffmpeg.audio_codec = 'AAC'

def main_checkStuffImages():
    #check if there is a cam
    if not bpy.context.scene.camera:
        return False
    #check if there are markers
    if len(bpy.context.scene.timeline_markers) < 2:
        return False
    #check if the blend file is saved
    if bpy.data.is_saved == False:
        return False
    else:
        return True

def main_checkStuffSingleImage():
    #check if there is a cam
    if not bpy.context.scene.camera:
        return False
    #check if there are markers
    if len(bpy.context.scene.timeline_markers) < 2:
        return False
    #check if current frame is before first marker
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    if bpy.context.scene.frame_current < mrks[0]:
        return False
    #check if the blend file is saved
    if bpy.data.is_saved == False:
        return False
    else:
        return True

def main_checkStuffAudio():
    #check if there are markers
    if len(bpy.context.scene.timeline_markers) < 2:
        return False
    #check if the blend file is saved
    if bpy.data.is_saved == False:
        return False
    #check if there is audio
    if len(bpy.data.sounds) < 1:
        return False
    #check if the audio has users
    if len(bpy.data.sounds) > 0:
        for i in bpy.data.sounds:
            if i.users > 0:
                return True
        return False

    else:
        return True

def main_checkStuffExport():
    #check if the blend file is saved
    if bpy.data.is_saved == False:
        return False
    if not bpy.context.scene.camera:
        return False
    else:
        return True

def main_exportAudioShots():
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    for i in range(len(mrks) - 1):
        bpy.context.scene.frame_start = mrks[i]
        bpy.context.scene.frame_end = mrks[i + 1] - 1  
        lz = main_getLeadingZeroes()
        n = ('%0' + lz + 'd') % (main_getShotNumberOfFrame(mrks[i]),)
        bpy.ops.sound.mixdown(filepath = bpy.path.abspath('//') + n + '_' + str(main_getMarkerNameOfFrame(mrks[i])) + '.wav', container='WAV', codec = 'PCM')
    #reset frame range
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end
    main_openFolder()
    
def main_exportImages():
    main_setPNG()
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    lz = main_getLeadingZeroes()
    fp = bpy.context.scene.render.filepath
    f = bpy.context.scene.frame_current
    for i in mrks:
        n = ('%0' + lz + 'd') % (main_getShotNumberOfFrame(i),)
        n = str(n)
        s = main_getMarkerNameOfFrame(i)
        bpy.context.scene.frame_set(i)
        bpy.context.scene.render.filepath = '//' + n + '_' + s 
        bpy.ops.render.render(write_still = True)
    #reset path and playhead
    bpy.context.scene.render.filepath = fp
    bpy.context.scene.frame_set(f)
    main_openFolder()
    
def main_exportSingleImage():
    main_setPNG()
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    lz = main_getLeadingZeroes()
    fp = bpy.context.scene.render.filepath
    f = bpy.context.scene.frame_current
    n = ('%0' + lz + 'd') % (main_getShotNumberOfFrame(f),)
    n = str(n)
    s = main_getMarkerNameOfFrame(f)
    bpy.context.scene.render.filepath = '//' + n + '_' + s 
    bpy.ops.render.render(write_still = True)
    #reset path and playhead
    bpy.context.scene.render.filepath = fp
    main_openFolder()
    
def main_exportH264():
    bpy.context.scene.render.filepath = '//export.mp4'
    main_setH264()
    bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
    main_openFolder()

# --------------------------------------------------------------------------------------------------------------------------------------------

#panel class
class STORYBOARDPANEL_PT_Panel(bpy.types.Panel):
    #panel attributes
    """Tooltip"""
    bl_label = 'Storyboard'
    bl_idname = 'MYPANEL_PT_Panel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Storyboard'
    
    #poll - if the poll function returns False, the panel will not be visible
    @classmethod
    def poll(cls, context):
        return 2 > 1
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.operator('script.storyboard_export_single_image', text = 'Export Single Image')
        col.operator('script.storyboard_export_images', text = 'Export All Images')
        col.operator('script.storyboard_export_audioclips', text = 'Export All Audioclips')
        col.operator('script.storyboard_export_h264', text = 'Export H264')
        
#operator class
class STORYBOARDEXPORTIMAGES_OT_Operator(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Export Storyboard Images'
    bl_idname = 'script.storyboard_export_images'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return main_checkStuffImages()
    
    #execute
    def execute(self, context):
        main_exportImages()
        return {'FINISHED'}

#operator class
class STORYBOARDEXPORTSINGLEIMAGE_OT_Operator(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Export Storyboard Single Image'
    bl_idname = 'script.storyboard_export_single_image'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return main_checkStuffSingleImage()
    
    #execute
    def execute(self, context):
        main_exportSingleImage()
        return {'FINISHED'}
    
#operator class
class STORYBOARDEXPORTAUDIOCLIPS_OT_Operator(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Export Storyboard Audioclips'
    bl_idname = 'script.storyboard_export_audioclips'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return main_checkStuffAudio()
    
    #execute
    def execute(self, context):
        main_exportAudioShots()
        return {'FINISHED'}

#operator class
class STORYBOARDEXPORTH264_OT_Operator(bpy.types.Operator):
    #operator attributes
    """Tooltip"""
    bl_label = 'Export Storyboard H264'
    bl_idname = 'script.storyboard_export_h264'
    
    #poll - if the poll function returns False, the button will be greyed out
    @classmethod
    def poll(cls, context):
        return main_checkStuffExport()
    
    #execute
    def execute(self, context):
        main_exportH264()
        return {'FINISHED'}

#registration
classes = (
    STORYBOARDPANEL_PT_Panel,
    STORYBOARDEXPORTIMAGES_OT_Operator,
    STORYBOARDEXPORTSINGLEIMAGE_OT_Operator,
    STORYBOARDEXPORTAUDIOCLIPS_OT_Operator,
    STORYBOARDEXPORTH264_OT_Operator
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

#enable to test the addon by running this script
if __name__ == '__main__':
    register()
