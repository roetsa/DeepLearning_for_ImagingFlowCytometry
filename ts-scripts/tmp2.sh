#!/bin/bash
cd /home/maximl/workdir/basic_nn

source venv/bin/activate
python main.py cv configs/cv-pbc-8-resnet18.json ~/runs/simple_nn/pbc/resnet18/9-color_d23_early_lowepslr_longrun ~/IFC/data/
