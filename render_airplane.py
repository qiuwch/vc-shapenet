import os, sys, tempfile, shutil
sys.path.append('rendercnn')
import global_variables as G
import os.path as osp

# set debug mode
debug_mode = 0
if debug_mode:
    io_redirect = ''
else:
    io_redirect = ' > /dev/null 2>&1'

# import blender configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR,'../'))
# from global_variables import *

def call_blender(modelfile, azimuth, elevation, tilt, distance, output_img):
    '''
    This function is modified from render_class_view.py
    '''
    blank_file = osp.join(G.g_blank_blend_file_path)
    # render_code = osp.join(g_render4cnn_root_folder, 'render_pipeline/render_model_views.py')
    # The render code is customized from render_model_view.py
    render_code = 'blender_script.py'
    
    
    temp_dirname = tempfile.mkdtemp()
    view_file = osp.join(temp_dirname, 'view.txt')
    view_fout = open(view_file,'w')
    view_fout.write(' '.join([azimuth, elevation, tilt, distance]))
    view_fout.close()
    
    render_cmd = '%s %s --background --python %s -- %s %s %s %s %s' % (
        G.g_blender_executable_path, 
        blank_file, 
        render_code, 
        modelfile, 
        'xxx', 
        'xxx', 
        view_file, 
        temp_dirname
    )
    try:
        print render_cmd
        os.system('%s %s' % (render_cmd, io_redirect))
        imgs = glob.glob(temp_dirname+'/*.png')
        shutil.move(imgs[0], output_img)
    except Exception as e:
        print e
        print('render failed. render_cmd: %s' % (render_cmd))
    
    # CLEAN UP
    shutil.rmtree(temp_dirname)
    

def render(model_file, viewpoints):
    # Lighting is controlled in render_opt.py file
    syn_images_folder = os.path.join(BASE_DIR, 'images')
    # model_name = 'chair001'
    # image_name = 'demo_img.png'
    image_name = model_file.replace('/model.obj', '').split('/')[-1] + '.png'
    print model_file, image_name
    if not os.path.exists(syn_images_folder):
        os.mkdir(syn_images_folder)
        # os.mkdir(os.path.join(syn_images_folder, model_name))


    # run code
    for v in viewpoints:
    # v = viewpoint_samples[0] # The viewpoint index
        print ">> Selected view: ", v
        script = os.path.join(BASE_DIR, 'rendercnn/demo_render/render_class_view.py')
        azimuth = str(v[0])
        elevation = str(v[1])
        tilt = str(v[2])
        distance = str(v[3])
        output_img = os.path.join(syn_images_folder, '%s_%s_%s' % (azimuth, elevation, image_name))
        
        call_blender(model_file, azimuth, elevation, tilt, distance, output_img)
        # python_cmd = 'python %s -a %s -e %s -t %s -d %s -o %s -m %s' % \
        # (script, azimuth, elevation, tilt, distance, output_img, model_file)
        # print ">> Running rendering command: \n \t %s" % (python_cmd)
        # os.system('%s %s' % (python_cmd, io_redirect))

    # show result
    # print(">> Displaying rendered image ...")
    # im = Image.open(os.path.join(syn_images_folder, model_name, image_name))
    # im.show()

if __name__ == '__main__':
    # List models
    import glob
    model_dir = 'ShapeNetCore.v1/02691156/*/model.obj'
    # 02691156 is the id for airplane
    print model_dir
    models = glob.glob(model_dir)
    print len(models)
    
    # viewpoint
    viewpoint_file = 'viewpoints/topdown.txt' 
    viewpoints = [[float(x) for x in line.rstrip().split(' ')] for line in open(viewpoint_file,'r')]
    
    if debug_mode:
        render(models[0], viewpoints)
    else:
        for model_file in models:
            render(model_file, viewpoints)
