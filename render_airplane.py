import os, sys

# set debug mode
debug_mode = 1
if debug_mode:
    io_redirect = ''
else:
    io_redirect = ' > /dev/null 2>&1'

# import blender configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR,'../'))
from global_variables import *

def render(model_file):
    syn_images_folder = os.path.join(BASE_DIR, 'demo_images')
    # model_name = 'chair001'
    # image_name = 'demo_img.png'
    image_name = model_file.replace('/model.obj', '').split('/')[-1] + '.png'
    print model_file, image_name
    if not os.path.exists(syn_images_folder):
        os.mkdir(syn_images_folder)
        # os.mkdir(os.path.join(syn_images_folder, model_name))

    # viewpoint
    viewpoint_samples_file = os.path.join(BASE_DIR, 'sample_viewpoints.txt')
    viewpoint_samples = [[float(x) for x in line.rstrip().split(' ')] for line in open(viewpoint_samples_file,'r')]

    # run code
    for v in viewpoint_samples:
    # v = viewpoint_samples[0] # The viewpoint index
        print ">> Selected view: ", v
        script = os.path.join(BASE_DIR, 'render_class_view.py')
        azimuth = str(v[0])
        elevation = str(v[1])
        tilt = str(v[2])
        distance = str(v[3])
        output_img = os.path.join(syn_images_folder, '%s_%s_%s' % (azimuth, elevation, image_name))
        python_cmd = 'python %s -a %s -e %s -t %s -d %s -o %s -m %s' % \
        (script, azimuth, elevation, tilt, distance, output_img, model_file)
        print ">> Running rendering command: \n \t %s" % (python_cmd)
        os.system('%s %s' % (python_cmd, io_redirect))

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
    # main(models[0])
    for model_file in models:
        render(model_file)
