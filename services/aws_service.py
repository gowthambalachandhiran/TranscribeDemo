# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 19:01:01 2024

@author: gowtham.balachan
"""

# services/aws_service.py
import asyncio
from amazon_transcribe.client import TranscribeStreamingClient
from config.settings import Settings

class AWSService:
    @classmethod
    async def create_transcribe_stream(cls):
        """
        Create and return a transcription stream
        
        Returns:
            TranscribeStreamingClient stream
        """
        try:
            client = TranscribeStreamingClient(region=Settings.AWS_REGION)
            stream = await client.start_stream_transcription(
                language_code=Settings.LANGUAGE_CODE,
                media_sample_rate_hz=Settings.SAMPLE_RATE,
                media_encoding="pcm"
            )
            return stream
        except Exception as e:
            print(f"Error creating transcription stream: {e}")
            raise