# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:04:46 2024

@author: gowtham.balachan
"""

import streamlit as st
from datetime import datetime

class TranscriptManager:
    @staticmethod
    def save_transcript():
        if st.session_state.transcript_text:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            content = "\n".join(st.session_state.transcript_text)
            
            st.download_button(
                label="Download Transcript",
                data=content,
                file_name=f"transcript_{timestamp}.txt",
                mime="text/plain"
            )

    @staticmethod
    def clear_transcript():
        st.session_state.transcript_text = []
        st.success("Transcript cleared!")