# -*- coding: utf-8 -*-
import warnings
from Sign_in_script import sign_main
warnings.filterwarnings("ignore")

def handler(event, context):

    sign_main()
    