import os
import cv2 as cv
import numpy as np
import torch
from torch.autograd import Variable

from net import Net
from option import Options
import utils
from utils import StyleLoader
import timeit





def evaluate(content_path, style_path, output_path):
        cuda = True
        content_image = utils.tensor_load_rgbimage(content_path, size=512, keep_asp=True)
        content_image = content_image.unsqueeze(0)
        style = utils.tensor_load_rgbimage(style_path, size=512)
        style = style.unsqueeze(0)    
        style = utils.preprocess_batch(style)

        style_model = Net(ngf=128)
        model_dict = torch.load("local_version/back/fast-ns/experiments/models/21styles.model")
        model_dict_clone = model_dict.copy()
        for key, value in model_dict_clone.items():
            if key.endswith(('running_mean', 'running_var')):
                del model_dict[key]
        style_model.load_state_dict(model_dict, False)

        if cuda:
            style_model.cuda()
            content_image = content_image.cuda()
            style = style.cuda()

        style_v = Variable(style)

        content_image = Variable(utils.preprocess_batch(content_image))
        style_model.setTarget(style_v)

        output = style_model(content_image)
        #output = utils.color_match(output, style_v)
        utils.tensor_save_bgrimage(output.data[0], output_path, cuda)

    
#evaluate("local_version/back/fast-ns/experiments/images/content/flowers.jpg","local_version/back/fast-ns/experiments/images/9styles/candy.jpg","local_version/back/fast-ns/experiments/output.jpg")
    
#okay let's try it with 2 functions

def do_model(style_path):
    cuda = True
    style = utils.tensor_load_rgbimage(style_path, size=512)
    style = style.unsqueeze(0)    
    style = utils.preprocess_batch(style)

    style_model = Net(ngf=128)
    model_dict = torch.load("local_version/back/fast-ns/experiments/models/21styles.model")
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
    return style_model,style

def evaluate_img(style_model,style, content_path,  output_path):
        cuda = True
        content_image = utils.tensor_load_rgbimage(content_path, size=512, keep_asp=True)
        content_image = content_image.unsqueeze(0)
        
        

        if cuda:
            #style_model.cuda()
            content_image = content_image.cuda()
           # style = style.cuda()

        

        content_image = Variable(utils.preprocess_batch(content_image))
        

        output = style_model(content_image)
        #output = utils.color_match(output, style_v)
        utils.tensor_save_bgrimage(output.data[0], output_path, cuda)

model, style = do_model("local_version/back/fast-ns/experiments/images/9styles/candy.jpg")



#Please leave this for testing 
#evaluate_img(model,style,"local_version/back/fast-ns/experiments/images/content/flowers.jpg","local_version/back/fast-ns/experiments/output.jpg")
#print(timeit.timeit(lambda: evaluate_img(model,style,"local_version/back/fast-ns/experiments/images/content/flowers.jpg","local_version/back/fast-ns/experiments/output.jpg"), number =1))