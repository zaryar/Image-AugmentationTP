import os
import cv2 as cv
import numpy as np
import torch
from torch.autograd import Variable

from net import Net
from option import Options
import utils
from utils import StyleLoader


def load_models(model_string):
    cuda = True ## if we somehow can't use a GPU we can set this to false
    style_model = Net(ngf=128)
    model_dict = torch.load("models\21styles.model") ##maybe i should train a new model here
    model_dict_clone = model_dict.copy()
    for key, value in model_dict_clone.items():
	    if key.endswith(('running_mean', 'running_var')):
                 del model_dict[key]
    style_model.load_state_dict(model_dict, False)
    style_model.eval()
    paths = {
    "starry_night": "local_version/back/fast-ns/experiments/images/starry_night",
    "the_scream": "local_version/back/fast-ns/experiments/images/starry_night"
}

        
    
    if cuda: 
         style_loader = StyleLoader(paths(model_string), 512)
         style_model.cuda()
    else:
         style_loader = StyleLoader(paths(model_string), 512, False)

    style_v = style_loader.get(0)
    style_v = Variable(style_v.data)
    style_model.setTarget(style_v)

    return style_model

	
         
         


def stylize_image(image_path,style_model,ouput_path):
    cuda = True
    img = cv.imread(image_path,cv.IMREAD_COLOR)
    img = np.array(img).transpose(2, 0, 1)
    img=torch.from_numpy(img).unsqueeze(0).float()
    if cuda:
          img=img.cuda()
          

    img = Variable(img)
    img = style_model(img)

    if cuda:
                img = img.cpu().clamp(0, 255).data[0].numpy()
    else:
          img = img.clamp(0, 255).data[0].numpy()
    cv.imwrite(ouput_path,img)
print("hello")


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
    return style_model,style

def evaluate_img(style_model,style, content_path,  output_path):
        cuda = True
        content_image = utils.tensor_load_rgbimage(content_path, size=512, keep_asp=True)
        content_image = content_image.unsqueeze(0)
        
        

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

model, style = do_model("local_version/back/fast-ns/experiments/images/9styles/candy.jpg")

evaluate_img(model,style,"local_version/back/fast-ns/experiments/images/content/flowers.jpg","local_version/back/fast-ns/experiments/output.jpg")