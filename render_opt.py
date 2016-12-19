import os, sys, random, math
import bpy
import numpy as np
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dep_paths = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'rendercnn')
]
for p in dep_paths:
    sys.path.append(p)

import global_variables as G

def obj_centened_camera_pos(dist, azimuth_deg, elevation_deg):
    phi = float(elevation_deg) / 180 * math.pi
    theta = float(azimuth_deg) / 180 * math.pi
    x = (dist * math.cos(theta) * math.cos(phi))
    y = (dist * math.sin(theta) * math.cos(phi))
    z = (dist * math.sin(phi))
    return (x, y, z)

def setup_lighting():
    # is_random_env_lighting = True
    light_num_lowbound = 5
    light_num_highbound = 5
    is_random_env_lighting = False
    
    light_num_lowbound = G.g_syn_light_num_lowbound
    light_num_highbound = G.g_syn_light_num_highbound
    light_dist_lowbound = G.g_syn_light_dist_lowbound
    light_dist_highbound = G.g_syn_light_dist_highbound
    
    bpy.context.scene.world.light_settings.use_environment_light = False
    
    use_environment_light = False
    use_sun_light = True
    use_point_light = False
    
    if use_environment_light:
        bpy.context.scene.world.light_settings.use_environment_light = True
        env_lighting = np.random.uniform(G.g_syn_light_environment_energy_lowbound, G.g_syn_light_environment_energy_highbound)
        bpy.context.scene.world.light_settings.environment_energy = env_lighting
        bpy.context.scene.world.light_settings.environment_color = 'PLAIN'
    
    if use_sun_light:
        # Add a sky lighting
        bpy.ops.object.lamp_add(type='SUN', view_align = False, location=(0, 0, 1))
        bpy.data.objects['Sun'].data.energy = 0.5 

    if use_point_light:
        # set point lights
        for i in range(random.randint(light_num_lowbound,light_num_highbound)):
            light_azimuth_deg = np.random.uniform(G.g_syn_light_azimuth_degree_lowbound, G.g_syn_light_azimuth_degree_highbound)
            light_elevation_deg  = np.random.uniform(G.g_syn_light_elevation_degree_lowbound, G.g_syn_light_elevation_degree_highbound)
            light_dist = np.random.uniform(light_dist_lowbound, light_dist_highbound)
            lx, ly, lz = obj_centened_camera_pos(light_dist, light_azimuth_deg, light_elevation_deg)
            bpy.ops.object.lamp_add(type='POINT', view_align = False, location=(lx, ly, lz))
            bpy.data.objects['Point'].data.energy = np.random.normal(G.g_syn_light_energy_mean, G.g_syn_light_energy_std)
