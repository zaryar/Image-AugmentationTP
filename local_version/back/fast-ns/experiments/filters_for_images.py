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



    #Test 
    model = load_models("starry_night")
    stylize_image("local_version/back/fast-ns/experiments/images/content/flowers.jpg",model,"local_version/back/fast-ns/experiments/test.jpg")
			
	