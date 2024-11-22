# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:56:29 2024

@author: gowtham.balachan
"""

import os
import streamlit as st

class Settings:
    AWS_ACCESS_KEY_ID = st.secrets["aws"]["access_key"]
    AWS_SECRET_ACCESS_KEY = st.secrets["aws"]["secret_key"]
    AWS_REGION = st.secrets["aws"]["region"]
    
    # Audio settings
    CHANNELS = 1
    SAMPLE_RATE = 16000
    BLOCK_SIZE = 1024 * 2
    DTYPE = "int16"
    
    # Transcription settings
    LANGUAGE_CODE = "en-IN"
    MAX_DURATION = 1800  # 30 minutes in seconds

    @classmethod
    def setup_aws_credentials(cls):
        os.environ['AWS_ACCESS_KEY_ID'] = cls.AWS_ACCESS_KEY_ID
        os.environ['AWS_SECRET_ACCESS_KEY'] = cls.AWS_SECRET_ACCESS_KEY
        os.environ['AWS_DEFAULT_REGION'] = cls.AWS_REGION