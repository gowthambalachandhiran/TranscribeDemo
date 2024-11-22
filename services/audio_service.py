# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:01:10 2024

@author: gowtham.balachan
"""

import asyncio
import sounddevice
from config.settings import Settings

class AudioService:
    @staticmethod
    async def create_mic_stream():
        loop = asyncio.get_event_loop()
        input_queue = asyncio.Queue()
        
        def callback(indata, frame_count, time_info, status):
            loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))
        
        stream = sounddevice.RawInputStream(
            channels=Settings.CHANNELS,
            samplerate=Settings.SAMPLE_RATE,
            callback=callback,
            blocksize=Settings.BLOCK_SIZE,
            dtype=Settings.DTYPE,
        )
        
        return stream, input_queue

    @staticmethod
    async def process_audio_stream(stream, input_queue):
        with stream:
            while True:
                indata, status = await input_queue.get()
                yield indata, status
