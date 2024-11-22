# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:03:27 2024

@author: gowtham.balachan
"""

import asyncio
import streamlit as st
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

class TranscriptionHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                st.write(alt.transcript)
                st.session_state.transcript_text.append(alt.transcript)

class TranscriptionService:
    def __init__(self):
        self.stop_transcription = False

    async def write_chunks(self, stream, audio_stream):
        async for chunk, status in audio_stream:
            if self.stop_transcription:
                break
            await stream.input_stream.send_audio_event(audio_chunk=chunk)
        await stream.input_stream.end_stream()

    def stop(self):
        self.stop_transcription = True