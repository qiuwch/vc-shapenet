# Weichao Qiu @ 2018
# Demo how to render a model from 3D warehouse in dae format
# using blender.
# It will call warehouse_blender.py inside blender and do the rendering.
import os, subprocess


def render(model_filename, viewpoint_filename, output_folder):
    blender_path = '/home/qiuwch/Downloads/blender-2.79b-linux-glibc219-x86_64/blender'
    # blender_path = r'C:\Program Files\Blender Foundation\Blender\blender.exe'
    abs_blank_filename = os.path.abspath('./blank.blend')
    abs_blender_script = os.path.abspath('./warehouse_blender.py')

    abs_model_filename = os.path.abspath(model_filename)
    abs_viewpoint_filename = os.path.abspath(viewpoint_filename)
    abs_output_folder = os.path.abspath(output_folder)

    render_cmd = '"{blender_path}" {abs_blank_filename} --background \
        --python {abs_blender_script} \
        -- {abs_model_filename} \
           {abs_viewpoint_filename} \
           {abs_output_folder}'''.format(**locals())

    # os.system('%s %s' % (render_cmd, io_redirect))
    print('Call blender with command "%s"' % render_cmd)
    subprocess.call(render_cmd, shell=True)


if __name__ == '__main__':
    # viewpoint_filename = 'viewpoints/topdown.txt' 
    viewpoint_filename = 'viewpoints/circle_viewpoints.txt'
    for i in [1, 3, 4, 5]:
        model_filename = './examples/book/%d/model.dae' % i
        output_folder = './images/%d/' % i

        render(model_filename, viewpoint_filename, output_folder)