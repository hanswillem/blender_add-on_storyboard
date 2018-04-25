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


#the main functions
def main_exportImagesAll():
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    fp = bpy.context.scene.render.filepath
    f = bpy.context.scene.frame_current
    for i in range(len(mrks) - 1):
        bpy.context.scene.frame_set(mrks[i])
        bpy.context.scene.render.filepath = "//sh_" + "%03d" % (i + 1,)
        bpy.ops.render.opengl(write_still=True)
    #reset path and playhead
    bpy.context.scene.render.filepath = fp
    bpy.context.scene.frame_set(f)

def main_exportAudioAll():
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    for i in range(len(mrks) - 1):
        bpy.context.scene.frame_start = mrks[i]
        bpy.context.scene.frame_end = mrks[i + 1] - 1  
        bpy.ops.sound.mixdown(filepath = bpy.path.abspath("//sh_") + "%03d" % (i + 1,) + ".wav", codec='PCM')
    #reset frame range
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end


def main_exportAudioIndividual():
    rng_start = bpy.context.scene.frame_start
    rng_end = bpy.context.scene.frame_end
    mrks = [marker.frame for marker in bpy.context.scene.timeline_markers]
    f = bpy.context.scene.frame_current
    for i in range(len(mrks) - 1):
        if mrks[i] <= f < mrks[i + 1]:
            bpy.context.scene.frame_start = mrks[i]
            bpy.context.scene.frame_end = mrks[i + 1] - 1 
            bpy.ops.sound.mixdown(filepath = bpy.path.abspath("//sh_") + "%03d" % (i + 1,) + ".wav", codec='PCM')
    #reset frame range
    bpy.context.scene.frame_start = rng_start
    bpy.context.scene.frame_end = rng_end


def checkStuffImages():
    #check if there are markers
    if len(bpy.context.scene.timeline_markers) == 0:
        return False
    #check if the blend file is saved
    if bpy.data.is_saved == False:
        return False


    #return true if all the above conditions are met
    else:
        return True


def checkStuffAudio():
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


#panel images
class Panel_images(bpy.types.Panel):
    
    #panel attributes
    """Images."""
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
        col.operator('script.operator_export_images_all', text="Export All Images")


#panel audio
class Panel_audio(bpy.types.Panel):
    
    #panel attributes
    """Audio."""
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
        col.operator('script.operator_export_audio_all', text="Export All Audio CLips")
        col.operator('script.operator_export_audio_individual', text="Export Current Audio Clip")



#panel info
class Panel_info(bpy.types.Panel):
    
    #panel attributes
    """Info."""
    bl_label = 'Info'
    bl_idname = 'tools_storyboard_info'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Storyboard'
    
    #draw loop
    def draw(self, context):
        layout = self.layout
        layout.label('Shots: ' +str(len([marker.frame for marker in bpy.context.scene.timeline_markers]) - 1))
        layout.label('Length Current Shot: ')


#operator class
class Operator_exportImagesAll(bpy.types.Operator):
    
    #operator attributes
    """Export all images as png's cut at markers"""
    bl_label = 'Operator Export Images All'
    bl_idname = 'script.operator_export_images_all'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return checkStuffImages()

    #execute
    def execute(self, context):
        main_exportImagesAll()
        
        return {'FINISHED'}
    

#operator class
class Operator_exportAllAudio(bpy.types.Operator):
    
    #operator attributes
    """Export all audio as clips cut at markers"""
    bl_label = 'Operator Export Audio All'
    bl_idname = 'script.operator_export_audio_all'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return checkStuffAudio()

    #execute
    def execute(self, context):
        main_exportAudioAll()
        
        return {'FINISHED'}


#operator class
class Operator_exportAudioIndividual(bpy.types.Operator):
    
    #operator attributes
    """Export audio clip under playhead cut by markers"""
    bl_label = 'Operator Export Audio Individual'
    bl_idname = 'script.operator_export_audio_individual'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return checkStuffAudio()

    #execute
    def execute(self, context):
        main_exportAudioIndividual()
        
        return {'FINISHED'}


#registration
def register():
    bpy.utils.register_class(Panel_images)
    bpy.utils.register_class(Panel_audio)
    bpy.utils.register_class(Panel_info)
    bpy.utils.register_class(Operator_exportImagesAll)
    bpy.utils.register_class(Operator_exportAllAudio)
    bpy.utils.register_class(Operator_exportAudioIndividual)
    

def unregister():
    bpy.utils.register_class(Panel_images)
    bpy.utils.register_class(Panel_audio)
    bpy.utils.register_class(Panel_info)
    bpy.utils.register_class(Operator_exportImagesAll)
    bpy.utils.register_class(Operator_exportAllAudio)
    bpy.utils.register_class(Operator_exportAudioIndividual)
    

#enable to test the addon by running this script
if __name__ == '__main__':
    register()
