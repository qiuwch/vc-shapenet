#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
This is a script designed to be run within blender
Call not call it directly, call in using warehouse_demo.py
No dependency on rendercnn code.

Usage: blender blank.blend --background --python warehouse_blender.py -- [model_filename] [viewpoint_filename] [output_folder]

Modified by Weichao Qiu
Original author: hao su, charles r. qi, yangyan li
'''

import os,sys,math,random
import bpy
import numpy as np

class ObjectView(object):
    def __init__(self, d):
        self.__dict__ = d

# Scene options copied from RenderForCNN project
render_opt = ObjectView(dict(
    g_syn_light_num_lowbound = 0,
    g_syn_light_num_highbound = 6,
    g_syn_light_dist_lowbound = 8,
    g_syn_light_dist_highbound = 20,
    g_syn_light_azimuth_degree_lowbound = 0,
    g_syn_light_azimuth_degree_highbound = 360,
    g_syn_light_elevation_degree_lowbound = -90,
    g_syn_light_elevation_degree_highbound = 90,
    g_syn_light_energy_mean = 2,
    g_syn_light_energy_std = 2,
    g_syn_light_environment_energy_lowbound = 0,
    g_syn_light_environment_energy_highbound = 1,
))

def camPosToQuaternion(cx, cy, cz):
    camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
    cx = cx / camDist
    cy = cy / camDist
    cz = cz / camDist
    axis = (-cz, 0, cx)
    angle = math.acos(cy)
    a = math.sqrt(2) / 2
    b = math.sqrt(2) / 2
    w1 = axis[0]
    w2 = axis[1]
    w3 = axis[2]
    c = math.cos(angle / 2)
    d = math.sin(angle / 2)
    q1 = a * c - b * d * w1
    q2 = b * c + a * d * w1
    q3 = a * d * w2 + b * d * w3
    q4 = -b * d * w2 + a * d * w3
    return (q1, q2, q3, q4)

def quaternionFromYawPitchRoll(yaw, pitch, roll):
    c1 = math.cos(yaw / 2.0)
    c2 = math.cos(pitch / 2.0)
    c3 = math.cos(roll / 2.0)    
    s1 = math.sin(yaw / 2.0)
    s2 = math.sin(pitch / 2.0)
    s3 = math.sin(roll / 2.0)    
    q1 = c1 * c2 * c3 + s1 * s2 * s3
    q2 = c1 * c2 * s3 - s1 * s2 * c3
    q3 = c1 * s2 * c3 + s1 * c2 * s3
    q4 = s1 * c2 * c3 - c1 * s2 * s3
    return (q1, q2, q3, q4)


def camPosToQuaternion(cx, cy, cz):
    q1a = 0
    q1b = 0
    q1c = math.sqrt(2) / 2
    q1d = math.sqrt(2) / 2
    camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
    cx = cx / camDist
    cy = cy / camDist
    cz = cz / camDist    
    t = math.sqrt(cx * cx + cy * cy) 
    tx = cx / t
    ty = cy / t
    yaw = math.acos(ty)
    if tx > 0:
        yaw = 2 * math.pi - yaw
    pitch = 0
    tmp = min(max(tx*cx + ty*cy, -1),1)
    #roll = math.acos(tx * cx + ty * cy)
    roll = math.acos(tmp)
    if cz < 0:
        roll = -roll    
    print("%f %f %f" % (yaw, pitch, roll))
    q2a, q2b, q2c, q2d = quaternionFromYawPitchRoll(yaw, pitch, roll)    
    q1 = q1a * q2a - q1b * q2b - q1c * q2c - q1d * q2d
    q2 = q1b * q2a + q1a * q2b + q1d * q2c - q1c * q2d
    q3 = q1c * q2a - q1d * q2b + q1a * q2c + q1b * q2d
    q4 = q1d * q2a + q1c * q2b - q1b * q2c + q1a * q2d
    return (q1, q2, q3, q4)

def camRotQuaternion(cx, cy, cz, theta): 
    theta = theta / 180.0 * math.pi
    camDist = math.sqrt(cx * cx + cy * cy + cz * cz)
    cx = -cx / camDist
    cy = -cy / camDist
    cz = -cz / camDist
    q1 = math.cos(theta * 0.5)
    q2 = -cx * math.sin(theta * 0.5)
    q3 = -cy * math.sin(theta * 0.5)
    q4 = -cz * math.sin(theta * 0.5)
    return (q1, q2, q3, q4)

def quaternionProduct(qx, qy): 
    a = qx[0]
    b = qx[1]
    c = qx[2]
    d = qx[3]
    e = qy[0]
    f = qy[1]
    g = qy[2]
    h = qy[3]
    q1 = a * e - b * f - c * g - d * h
    q2 = a * f + b * e + c * h - d * g
    q3 = a * g - b * h + c * e + d * f
    q4 = a * h + b * g - c * f + d * e    
    return (q1, q2, q3, q4)

def obj_centened_camera_pos(dist, azimuth_deg, elevation_deg):
    ''' Assume object is placed at (0, 0, 0) '''
    phi = float(elevation_deg) / 180 * math.pi
    theta = float(azimuth_deg) / 180 * math.pi
    x = (dist * math.cos(theta) * math.cos(phi))
    y = (dist * math.sin(theta) * math.cos(phi))
    z = (dist * math.sin(phi))
    return (x, y, z)

def random_lighting():
    # is_random_env_lighting = True
    light_num_lowbound = 5
    light_num_highbound = 5
    is_random_env_lighting = False
    
    light_num_lowbound = render_opt.g_syn_light_num_lowbound
    light_num_highbound = render_opt.g_syn_light_num_highbound
    light_dist_lowbound = render_opt.g_syn_light_dist_lowbound
    light_dist_highbound = render_opt.g_syn_light_dist_highbound
    
    bpy.context.scene.world.light_settings.use_environment_light = False
    
    use_environment_light = False
    use_sun_light = True
    use_point_light = False
    
    if use_environment_light:
        bpy.context.scene.world.light_settings.use_environment_light = True
        env_lighting = np.random.uniform(render_opt.g_syn_light_environment_energy_lowbound, render_opt.g_syn_light_environment_energy_highbound)
        bpy.context.scene.world.light_settings.environment_energy = env_lighting
        bpy.context.scene.world.light_settings.environment_color = 'PLAIN'
    
    if use_sun_light:
        # Add a sky lighting
        bpy.ops.object.lamp_add(type='SUN', view_align = False, location=(0, 0, 1))
        bpy.data.objects['Sun'].data.energy = 0.5 

    if use_point_light:
        # set point lights
        for i in range(random.randint(light_num_lowbound,light_num_highbound)):
            light_azimuth_deg = np.random.uniform(render_opt.g_syn_light_azimuth_degree_lowbound, render_opt.g_syn_light_azimuth_degree_highbound)
            light_elevation_deg  = np.random.uniform(render_opt.g_syn_light_elevation_degree_lowbound, render_opt.g_syn_light_elevation_degree_highbound)
            light_dist = np.random.uniform(light_dist_lowbound, light_dist_highbound)
            lx, ly, lz = obj_centened_camera_pos(light_dist, light_azimuth_deg, light_elevation_deg)
            bpy.ops.object.lamp_add(type='POINT', view_align = False, location=(lx, ly, lz))
            bpy.data.objects['Point'].data.energy = np.random.normal(render_opt.g_syn_light_energy_mean, render_opt.g_syn_light_energy_std)

def clear_scene():
    ''' Setup lighting etc.'''
    bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
    #bpy.context.scene.render.use_shadows = False
    #bpy.context.scene.render.use_raytrace = False

    bpy.data.objects['Lamp'].data.energy = 0

    #m.subsurface_scattering.use = True
    # set lights
    bpy.ops.object.select_all(action='TOGGLE')
    if 'Lamp' in list(bpy.data.objects.keys()):
        bpy.data.objects['Lamp'].select = True # remove default light
    bpy.ops.object.delete()

    # clear default lights
    bpy.ops.object.select_by_type(type='LAMP')
    bpy.ops.object.delete(use_global=False)


def read_viewpoints(abs_viewpoint_filename):
    with open(abs_viewpoint_filename,'r') as f:
        # Each line is four number split by space
        lines = [l.strip() for l in f.readlines()] 
        
    viewpoints = []
    for l in lines:
        vs = l.split(' ')
        viewpoint = dict(
            az = float(vs[0]),
            el = float(vs[1]),
            tilt = float(vs[2]),
            dist = float(vs[3]),
        )
        viewpoints.append(viewpoint)
    return viewpoints

def set_camera_viewpoint(cam_obj, viewpoint):
    azimuth_deg = viewpoint['az']
    elevation_deg = viewpoint['el'] 
    theta_deg = viewpoint['tilt'] 
    dist = viewpoint['dist'] 

    cx, cy, cz = obj_centened_camera_pos(dist, azimuth_deg, elevation_deg)
    q1 = camPosToQuaternion(cx, cy, cz)
    q2 = camRotQuaternion(cx, cy, cz, theta_deg)
    q = quaternionProduct(q2, q1)
    cam_obj.location[0] = cx
    cam_obj.location[1] = cy 
    cam_obj.location[2] = cz
    cam_obj.rotation_mode = 'QUATERNION'
    cam_obj.rotation_quaternion[0] = q[0]
    cam_obj.rotation_quaternion[1] = q[1]
    cam_obj.rotation_quaternion[2] = q[2]
    cam_obj.rotation_quaternion[3] = q[3]

def main():
    # Input parameters, read in reverse order because the first few are used by blender
    abs_model_filename = sys.argv[-3]
    abs_viewpoint_filename = sys.argv[-2]
    abs_output_folder = sys.argv[-1]
    if not os.path.exists(abs_output_folder):
        os.makedirs(abs_output_folder)

    viewpoints = read_viewpoints(abs_viewpoint_filename)

    bpy.ops.wm.collada_import(filepath="")
    # bpy.ops.import_scene.obj(filepath=abs_model_filename)
    camObj = bpy.data.objects['Camera']
    # camObj.data.lens_unit = 'FOV'
    # camObj.data.angle = 0.2

    # clear_scene() # Remove lighting from this scene to allow randomization

    for viewpoint in viewpoints:
        # set environment lighting
        #bpy.context.space_data.context = 'WORLD'

        # random_lighting()
        set_camera_viewpoint(camObj, viewpoint)

        image_filename = os.path.join(abs_output_folder,
            '{az}_{el}_{tilt}_{dist}.png'.format(**viewpoint)
        )
        bpy.data.scenes['Scene'].render.filepath = image_filename 
        bpy.ops.render.render( write_still=True )

main()