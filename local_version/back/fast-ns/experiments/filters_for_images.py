import os
import cv2 as cv
import numpy as np
import torch
from torch.autograd import Variable

from net import Net
from option import Options
import utils
from utils import StyleLoader


def load_models():
    style_model = Net(ngf=128)
    model_dict = torch.load("models\21styles.model") ##maybe i should train a new model here


def stylize_image(model):
    pass