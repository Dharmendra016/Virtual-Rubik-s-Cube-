from ursina import * 

app = Ursina() 

#initilization

global rot 

#screen/environment and camera 
window.fullscreen = True
Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
       color=color.light_gray)  # plane
Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)  # sky
EditorCamera()
camera.world_position = (0, 0, -15)
model, texture = 'models/custom_cube', 'textures/rubik_texture'

action_trigger = True

#cube position
LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
SIDE_POSITIONS =   LEFT |  BOTTOM |  FACE |  BACK |   RIGHT |   TOP

#cube 
CUBES = [Entity(model=model, texture=texture, position=pos) for pos in SIDE_POSITIONS]
parent = Entity()  
rotation_axes = {
    'LEFT':'x' , 
    'RIGHT':"x",
    'TOP':'y',
    'BOTTOM':'y',
    'FACE':'z',
    'BACK':'z'
}

cubes_side_positions = {
    'LEFT':LEFT , 
    'RIGHT':RIGHT,
    'BOTTOM':BOTTOM,
    'TOP':TOP , 
    'FACE':FACE,
    "BACK":BACK
}

animation_time= 0.5

def reparent_to_scene():
    global parent
    global cubes_side_positions , rotation_axes
    for cube in CUBES:
        if cube.parent == parent:
            world_pos , world_rot = round(cube.world_position , 1) , cube.world_rotation
            cube.parent = scene
            cube.position , cube.rotation = world_pos  , world_rot
    parent.rotation = 0

def toggle_animation_trigger():
    global action_trigger
    action_trigger = not action_trigger

def rotate_side(side_name):
    global action_trigger
    action_trigger = False
    global cubes_side_positions , rotation_axes
    cube_positions = cubes_side_positions[side_name]
    rotation_axis = rotation_axes[side_name]
    reparent_to_scene()

    for cube in CUBES:
        if cube.position in cube_positions:
            cube.parent = parent
            eval(f'parent.animate_rotation_{rotation_axis}(90, duration=animation_time)')
    global animation_time
    invoke(toggle_animation_trigger , delay = animation_time +0.11)

def input(key):
    global action_trigger
    if key == 'a' and action_trigger:
        rotate_side('LEFT')
    
    if key == 's' and action_trigger:
        rotate_side('BOTTOM')
    
    if key == 'd' and action_trigger:
        rotate_side('RIGHT')
        
    if key == 'w' and action_trigger:
        rotate_side('TOP')
    
    if key == 'q' and action_trigger:
        rotate_side('FACE')

    if key == 'e' and action_trigger:
        rotate_side('BACK')


app.run()