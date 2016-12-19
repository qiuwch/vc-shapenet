# vc-shapenet
ShapeNet rendering scripts for visual concept

## Install
- Download `ShapeNetCore.v1.zip` to this folder. 

    Unzip the zip file, the folder structure will looks like `ShapeNetCore.v1/02691156/[model_id]`. `model_id` is a very long string and is the unique id for a model.
    
- Setup code from RenderForCNN

    - `git submodule init` and `git submodule update` to get `RenderForCNN` code into the `rendercnn` folder.
    
    - mv `global_variables.py.example` to `global_variables.py` and change the configuration for blender
    
    Notice: The dependency on RenderForCNN is quite heavy and not necessary at all. we can consider get rid of it.

## Scripts in this repository 

- render_airplane.py

    Batch script to render all airplane model, use the viewpoint file in `viewpoints` folder
        
- view_3d_model.py
    
    Take `[model_id]` as its input argument. Show this 3D model in blender. 
    
    

    
    
    
