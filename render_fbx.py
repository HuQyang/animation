import bpy
import os

context = bpy.context

# models_path = "/Users/qiyang/Documents/SIGGRAPHAsia/fbx/mixamo/AJ/with_skin"
# render_path = "//"
# save_path = "/Users/qiyang/Documents/SIGGRAPHAsia/fbx/codes/"

# # models = [ "Agreeing yes.fbx"]

# models = ["2 People Shaking Hands Part 1 -  Female.fbx"]

#create a scene
scene = bpy.data.scenes.get("Scene")
# camera_data = bpy.data.cameras.new("Camera")

camera = bpy.data.objects.get("Camera")
camera.location = (0.0, -2.5, 1.2)
camera.rotation_euler = (1.5,0.0, 0)
# scene.objects.link(camera)

# Create new lamp datablock
lamp_data = bpy.data.lamps.new(name="New Lamp", type='HEMI')

# Create new object with our lamp datablock
lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
# lamp_object = bpy.data.objects.get("Lamp")
# lamp_object.type = 'SUN'
lamp_data.energy = 1.2
# Place lamp to a specified location
lamp_object.location = (-1.0, -5.0, 2.0)

# And finally select it make active
lamp_object.select = True
scene.objects.active = lamp_object

# Link lamp object to the scene so it'll appear in this scene
scene.objects.link(lamp_object)
# do the same for lights etc

scene.world = bpy.data.worlds.get("World")
scene.world.horizon_color = (1.0,1.0,1.0)
# world_data = bpy.data.worlds.new("World")
# world_object = bpy.data.objects.new("World", world_data)
# world_object.horizon_color = (255.0,255.0,255.0)
# scene.objects.link(world_object)
scene.update()


f = open('/Users/qiyang/Documents/SIGGRAPHAsia/fbx/codes/fbx_file.txt','r')
models = f.readlines()
f.close()

fn , tl = os.path.split(models[0])
render_path = fn+'_img'

for model_path in models:
    scene.camera = camera

    filename,tail = os.path.split(model_path)
    folder_name = tail.split('.')[0]
    save_path = os.path.join(render_path,folder_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    path = model_path.strip()
    
    # make a new scene with cam and lights linked
    context.screen.scene = scene
    bpy.ops.scene.new(type='LINK_OBJECTS')
    context.scene.name = model_path
    cams = [c for c in context.scene.objects if c.type == 'CAMERA']
    # bpy.ops.import_scene.fbc()
    bpy.ops.import_scene.fbx(filepath=path, axis_forward='-Z', axis_up='Y',\
     directory="", filter_glob="*.fbx", ui_tab='MAIN', use_manual_orientation=False,\
      global_scale=1, bake_space_transform=False, use_custom_normals=True, use_image_search=True,\
       use_alpha_decals=False, decal_offset=0, use_anim=True, anim_offset=1, use_custom_props=True, \
       use_custom_props_enum_as_string=True, ignore_leaf_bones=False, force_connect_children=False, \
       automatic_bone_orientation=False, primary_bone_axis='Y', secondary_bone_axis='X', use_prepost_rot=True)

    bpy.context.scene.render.resolution_x = 512*2
    bpy.context.scene.render.resolution_y = 512*2
    bpy.context.scene.frame_end = 60


    #import model
    # bpy.ops.import_scene.obj(filepath=path, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")
    

    for c in cams:
        context.scene.camera = c                                    
        # print("Render ", model_path, context.scene.name, c.name)
        context.scene.render.filepath = os.path.join(save_path,"")
        
        # bpy.data.scenes["test"].frame_end=100

        #bpy.ops.render.render(write_still=True,animation=True)
        bpy.ops.render.opengl(write_still=True,animation=True)

# filename = "/Users/qiyang/Documents/SIGGRAPHAsia/fbx/codes/render_fbx.py"
# exec(compile(open(filename).read(), filename, 'exec'))


