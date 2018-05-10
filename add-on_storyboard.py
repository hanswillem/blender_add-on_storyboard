# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    'name' : 'Storyboard',
    'author' : 'Hans Willem Gijzel',
    'version' : (1, 0),
    'blender' : (2, 79),
    'location' : 'View 3D > Tools > Storyboard',
    'description' : 'A collection of storyboard tools',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'Storyboard'
    }


#imports
import bpy
import math
import os


#------------------------------------------------------------------------------------------------------------------------------
# main functions - setup
#------------------------------------------------------------------------------------------------------------------------------


def main_setup():
    bpy.ops.object.camera_add(location=(0, -8, 0), rotation=(math.radians(90), 0, 0))
    bpy.context.space_data.show_only_render = True
    bpy.context.space_data.show_world = True
    bpy.context.scene.world.horizon_color = (0.6, 0.6, 0.6)
    #look through camera
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    area.spaces[0].region_3d.view_perspective = 'CAMERA'


def main_openFolder():
    os.system('open ' + (bpy.path.abspath('//')))


def main_getShotLength(f):
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    for i in range(len(mrks) - 1):
        if mrks[i] <= f < mrks[i + 1]:
            return mrks[i + 1] - mrks [i]


def main_getShotNumberOfFrame(f):
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    for i in range(len(mrks) - 1):
        if mrks[i] <= f < mrks[i + 1]:
            return i + 1


def main_renameMarkers():
    for i in bpy.context.scene.timeline_markers:
        s = main_getShotNumberOfFrame(i.frame)
        if s == None:
            i.name = 'end'
        else:
            i.name = 'sh_' + '%03d' % (main_getShotNumberOfFrame(i.frame),)


def main_getMarkerNameOfFrame(f):
    # make a dictionary of marker framenumbers and marker names
    d_mrks = {}
    for i in  bpy.context.scene.timeline_markers:
        d_mrks[i.frame] = i.name
    # make a list of the frame numbers and sort them
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    # get the marker name and return it
    for i in range(len(mrks) - 1):
        if mrks[i] <= f < mrks[i + 1]:
            return  d_mrks[mrks[i]];


#------------------------------------------------------------------------------------------------------------------------------
# main functions - images
#------------------------------------------------------------------------------------------------------------------------------


def main_stamp(s):
    bpy.context.scene.render.use_stamp = True
    bpy.context.scene.render.stamp_foreground = (1, 1, 1, 1)
    bpy.context.scene.render.stamp_background = (0, 0, 0, 1)
    bpy.context.scene.render.use_stamp_time = False
    bpy.context.scene.render.use_stamp_date = False
    bpy.context.scene.render.use_stamp_render_time = False
    bpy.context.scene.render.use_stamp_frame = False
    bpy.context.scene.render.use_stamp_scene = False
    bpy.context.scene.render.use_stamp_camera = False
    bpy.context.scene.render.use_stamp_filename = False
    bpy.context.scene.render.use_stamp_note = True
    bpy.context.scene.render.stamp_note_text = s


def main_exportImagesAll():
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    fp = bpy.context.scene.render.filepath
    f = bpy.context.scene.frame_current
    for i in mrks[:-1]:
        s = str(main_getMarkerNameOfFrame(i))
        bpy.context.scene.frame_set(i)
        main_stamp(s)
        bpy.context.scene.render.filepath = '//' + s
        bpy.ops.render.opengl(write_still = True)
    #reset path and playhead
    bpy.context.scene.render.filepath = fp
    bpy.context.scene.frame_set(f)
    bpy.context.scene.render.stamp_note_text = ''
    bpy.context.scene.render.use_stamp_note = False
    bpy.context.scene.render.use_stamp = False
    main_openFolder()


def main_exportImagesIndividual():
    fp = bpy.context.scene.render.filepath
    f = bpy.context.scene.frame_current
    s = str(main_getMarkerNameOfFrame(f))
    main_stamp(s)
    bpy.context.scene.render.filepath = '//' + s
    bpy.ops.render.opengl(write_still = True)
    bpy.context.scene.render.filepath = fp
    main_openFolder()


def main_exportImagesSequence():
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    bpy.context.scene.render.use_stamp = False
    fp = bpy.context.scene.render.filepath
    bpy.context.scene.render.filepath = '//seq_' 
    bpy.context.scene.frame_start = mrks[0]
    bpy.context.scene.frame_end = mrks[-1]  
    bpy.ops.render.opengl(animation = True)
    #reset
    bpy.context.scene.render.filepath = fp
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end


def main_checkStuffImages():
    #check if there are markers
    if len(bpy.context.scene.timeline_markers) == 0:
        return False
    #check if the blend file is saved
    if bpy.data.is_saved == False:
        return False

    #return true if all the above conditions are met
    else:
        return True
    

#------------------------------------------------------------------------------------------------------------------------------
# main functions - audio
#------------------------------------------------------------------------------------------------------------------------------


def main_exportAudioMixdown():
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    bpy.context.scene.frame_start = mrks[0]
    bpy.context.scene.frame_end = mrks[-1]
    bpy.ops.sound.mixdown(filepath = bpy.path.abspath('//mixdown') + '.wav',  container='WAV', codec = 'PCM')
    #reset frame range
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end
    main_openFolder() 


def main_exportAudioShots():
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    mrks.sort()
    for i in range(len(mrks) - 1):
        bpy.context.scene.frame_start = mrks[i]
        bpy.context.scene.frame_end = mrks[i + 1] - 1  
        bpy.ops.sound.mixdown(filepath = bpy.path.abspath('//sh_') + '%03d' % (i + 1,) + '.wav',  container='WAV', codec = 'PCM')
    #reset frame range
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end
    main_openFolder()


def main_exportAudioIndividual():
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers] 
    mrks.sort()
    f = bpy.context.scene.frame_current
    for i in range(len(mrks) - 1):
        if mrks[i] <= f < mrks[i + 1]:
            bpy.context.scene.frame_start = mrks[i]
            bpy.context.scene.frame_end = mrks[i + 1] - 1 
            bpy.ops.sound.mixdown(filepath = bpy.path.abspath('//sh_') + '%03d' % (i + 1,) + '.wav', container='WAV', codec = 'PCM')
    #reset frame range
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end
    main_openFolder()


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

    #return true if all the above conditions are met
    else:
        return True


#------------------------------------------------------------------------------------------------------------------------------
# panel & operators - setup
#------------------------------------------------------------------------------------------------------------------------------


#panel setup
class Panel_setup(bpy.types.Panel):
    
    #panel attributes
    '''Info.'''
    bl_label = 'Setup'
    bl_idname = 'tools_storyboard_setup'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Storyboard'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        col.operator('script.operator_setup', text = 'Setup Viewport')
        col.operator('script.operator_rename_markers', text = 'Rename Markers')
        col.operator('script.operator_open_folder', text = 'Open Folder')
        

#operator class
class Operator_setup(bpy.types.Operator):
    
    #operator attributes
    '''Setup the viewport'''
    bl_label = 'Operator Setup'
    bl_idname = 'script.operator_setup'
    bl_options = {'REGISTER', 'UNDO'}

    #execute
    def execute(self, context):
        main_setup()
        
        return {'FINISHED'}


#operator class
class Operator_renameMarkers(bpy.types.Operator):
    
    #operator attributes
    '''Open folder where the blend file is saved'''
    bl_label = 'Operator Rename Markers'
    bl_idname = 'script.operator_rename_markers'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return len(bpy.context.scene.timeline_markers) > 1

    #execute
    def execute(self, context):
        main_renameMarkers()
        
        return {'FINISHED'}


#operator class
class Operator_openFolder(bpy.types.Operator):
    
    #operator attributes
    '''Open folder where the blend file is saved'''
    bl_label = 'Operator Open Folder'
    bl_idname = 'script.operator_open_folder'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    #execute
    def execute(self, context):
        main_openFolder()
        
        return {'FINISHED'}


#------------------------------------------------------------------------------------------------------------------------------
# panel & operators - images
#------------------------------------------------------------------------------------------------------------------------------


#panel images
class Panel_images(bpy.types.Panel):
    
    #panel attributes
    '''Images.'''
    bl_label = 'Images'
    bl_idname = 'tools_storyboard_images'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Storyboard'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        #layout.label('My Label')
        col = layout.column(align = True)
        col.operator('script.operator_export_images_sequence', text = 'Export Sequence')
        col.operator('script.operator_export_images_all', text = 'Export Shots')
        col.operator('script.operator_export_images_individual', text = 'Export Current')


#operator class
class Operator_exportImagesSequence(bpy.types.Operator):
    
    #operator attributes
    '''Export the timeline as a png sequence'''
    bl_label = 'Operator Export Images Sequence'
    bl_idname = 'script.operator_export_images_sequence'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return main_checkStuffImages()

    #execute
    def execute(self, context):
        main_exportImagesSequence()
        
        return {'FINISHED'}


#operator class
class Operator_exportImagesAll(bpy.types.Operator):
    
    #operator attributes
    '''Export all images as png's cut at markers'''
    bl_label = 'Operator Export Images All'
    bl_idname = 'script.operator_export_images_all'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return main_checkStuffImages()

    #execute
    def execute(self, context):
        main_exportImagesAll()
        
        return {'FINISHED'}
    

#operator class
class Operator_exportImagesIndividual(bpy.types.Operator):
    
    #operator attributes
    '''Export image under playhead as png'''
    bl_label = 'Operator Export Images Individual'
    bl_idname = 'script.operator_export_images_individual'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    #execute
    def execute(self, context):
        main_exportImagesIndividual()
        
        return {'FINISHED'}


#------------------------------------------------------------------------------------------------------------------------------
# panel & operators - audio
#------------------------------------------------------------------------------------------------------------------------------


#panel audio
class Panel_audio(bpy.types.Panel):
    
    #panel attributes
    '''Audio.'''
    bl_label = 'Audio'
    bl_idname = 'tools_storyboard_audio'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Storyboard'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        #layout.label('My Label')
        col = layout.column(align = True)
        col.operator('script.operator_export_audio_mixdown', text = 'Export Mixdown')
        col.operator('script.operator_export_audio_all', text = 'Export Shots')
        col.operator('script.operator_export_audio_individual', text = 'Export Current')


#operator class
class Operator_exportMixdownAudio(bpy.types.Operator):
    
    #operator attributes
    '''Export audio mixdown'''
    bl_label = 'Operator Export Audio Mixdown'
    bl_idname = 'script.operator_export_audio_mixdown'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return main_checkStuffAudio()

    #execute
    def execute(self, context):
        main_exportAudioMixdown()
        
        return {'FINISHED'}


#operator class
class Operator_exportAllAudio(bpy.types.Operator):
    
    #operator attributes
    '''Export all audio as clips cut at markers'''
    bl_label = 'Operator Export Audio All'
    bl_idname = 'script.operator_export_audio_all'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return main_checkStuffAudio()

    #execute
    def execute(self, context):
        main_exportAudioShots()
        
        return {'FINISHED'}


#operator class
class Operator_exportAudioIndividual(bpy.types.Operator):
    
    #operator attributes
    '''Export audio clip under playhead cut by markers'''
    bl_label = 'Operator Export Audio Individual'
    bl_idname = 'script.operator_export_audio_individual'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return main_checkStuffAudio()

    #execute
    def execute(self, context):
        main_exportAudioIndividual()
        
        return {'FINISHED'}


#------------------------------------------------------------------------------------------------------------------------------
# panel & operators - info
#------------------------------------------------------------------------------------------------------------------------------

#panel setup
class Panel_info(bpy.types.Panel):
    
    #panel attributes
    '''Info.'''
    bl_label = 'Info'
    bl_idname = 'tools_storyboard_info'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Storyboard'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        col = layout.column(align = True)
        sh_amnt = len(bpy.context.scene.timeline_markers) - 1
        if sh_amnt > 0:
            sh_amnt = str(sh_amnt)
            layout.label('Total Shots: ' + sh_amnt)
            if main_getShotNumberOfFrame(bpy.context.scene.frame_current) != None:
                sh = str(main_getShotNumberOfFrame(bpy.context.scene.frame_current))
                sh_len_f = str(main_getShotLength(bpy.context.scene.frame_current))
                sh_len_s = ("%.2f" % (main_getShotLength(bpy.context.scene.frame_current) / bpy.context.scene.render.fps))
                layout.label('Shot: ' + sh)
                layout.label('Length: ' + sh_len_f + ' (' + sh_len_s + ')')
        else:
            layout.label('No Shots')


#------------------------------------------------------------------------------------------------------------------------------
# registration
#------------------------------------------------------------------------------------------------------------------------------


def register():
    bpy.utils.register_class(Panel_setup)
    bpy.utils.register_class(Panel_images)
    bpy.utils.register_class(Panel_audio)
    bpy.utils.register_class(Panel_info)

    bpy.utils.register_class(Operator_setup)
    bpy.utils.register_class(Operator_renameMarkers)
    bpy.utils.register_class(Operator_openFolder)
    bpy.utils.register_class(Operator_exportImagesSequence)
    bpy.utils.register_class(Operator_exportImagesAll)
    bpy.utils.register_class(Operator_exportImagesIndividual)
    bpy.utils.register_class(Operator_exportMixdownAudio)
    bpy.utils.register_class(Operator_exportAllAudio)
    bpy.utils.register_class(Operator_exportAudioIndividual)
    

def unregister():
    bpy.utils.unregister_class(Panel_setup)
    bpy.utils.unregister_class(Panel_images)
    bpy.utils.unregister_class(Panel_audio)
    bpy.utils.unregister_class(Panel_info)

    bpy.utils.unregister_class(Operator_setup)
    bpy.utils.unregister_class(Operator_openFolder)
    bpy.utils.unregister_class(Operator_exportImagesSequence)
    bpy.utils.unregister_class(Operator_renameMarkers)
    bpy.utils.unregister_class(Operator_exportImagesAll)
    bpy.utils.unregister_class(Operator_exportImagesIndividual)
    bpy.utils.unregister_class(Operator_exportMixdownAudio)
    bpy.utils.unregister_class(Operator_exportAllAudio)
    bpy.utils.unregister_class(Operator_exportAudioIndividual)
    

#enable to test the addon by running this script
if __name__ == '__main__':
    register()
