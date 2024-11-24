import os
import asyncio
import sounddevice
import streamlit as st
import boto3

from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

# Access credentials from Streamlit secrets
AWS_ACCESS_KEY_ID = st.secrets["aws"]["access_key"]
AWS_SECRET_ACCESS_KEY = st.secrets["aws"]["secret_key"]
AWS_REGION = st.secrets["aws"]["region"]

# Set environment variables for AWS credentials
os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
os.environ['AWS_DEFAULT_REGION'] = AWS_REGION

# Create boto3 session 
boto3_session = boto3.Session(region_name=AWS_REGION)

class MyEventHandler(TranscriptResultStreamHandler):
    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                st.write(alt.transcript)

async def mic_stream():
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()
    
    def callback(indata, frame_count, time_info, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, (bytes(indata), status))
    
    stream = sounddevice.RawInputStream(
        channels=1,
        samplerate=16000,
        callback=callback,
        blocksize=1024 * 2,
        dtype="int16",
    )
    
    with stream:
        while True:
            indata, status = await input_queue.get()
            yield indata, status

async def write_chunks(stream):
    async for chunk, status in mic_stream():
        await stream.input_stream.send_audio_event(audio_chunk=chunk)
    await stream.input_stream.end_stream()

async def basic_transcribe():
    try:
        # Create TranscribeStreamingClient 
        client = TranscribeStreamingClient(region=AWS_REGION)
        
        stream = await client.start_stream_transcription(
            language_code="en-US",
            media_sample_rate_hz=16000,
            media_encoding="pcm"
        )
        
        handler = MyEventHandler(stream.output_stream)
        await asyncio.gather(write_chunks(stream), handler.handle_events())
    
    except Exception as e:
        st.error(f"Transcription error: {e}")

def main():
    st.title("Live Audio Transcription")
    
    # Add a button to start transcription
    if st.button("Start Transcription"):
        asyncio.run(basic_transcribe())

if __name__ == "__main__":
    main()