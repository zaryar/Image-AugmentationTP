import os
import cv2 as cv
import numpy as np
import torch
from torch.autograd import Variable
from fast_ns.experiments.net import Net
import fast_ns.experiments.utils as utils



#this function takes one of the pretrained style images and returns the correct style transfer model for it
def do_model(style_path):
    cuda = True
    style = utils.tensor_load_rgbimage(style_path, size=512)
    style = style.unsqueeze(0)    
    style = utils.preprocess_batch(style) #preprocessing for the style image

    style_model = Net(ngf=128)
    model_dict = torch.load("local_version/back/fast_ns/experiments/models/21styles.model")
    model_dict_clone = model_dict.copy()
    for key, value in model_dict_clone.items():
        if key.endswith(('running_mean', 'running_var')):
            del model_dict[key]
    style_model.load_state_dict(model_dict, False)


    if cuda:
            style_model.cuda()
            style = style.cuda()
    style_v = Variable(style)
    style_model.setTarget(style_v)
    return style_model

#this function takes an image , a ready to use model and writes the stylized image jpg to the output_path 
def evaluate_img(style_model,content_path,  output_path):
        cuda = True
        content_image = utils.tensor_load_rgbimage(content_path, size=512, keep_asp=True) #transfer the picture to a tensor
        content_image = content_image.unsqueeze(0)
        
        

        if cuda:
            #style_model.cuda()
            content_image = content_image.cuda()
           # style = style.cuda()

        

        content_image = Variable(utils.preprocess_batch(content_image))
        

        output = style_model(content_image) #actual style transfer
        
        utils.tensor_save_bgrimage(output.data[0], output_path, cuda)
