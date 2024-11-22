import asyncio
import time
import streamlit as st
from config.settings import Settings
from services.aws_service import AWSService
from services.audio_service import AudioService
from handlers.transcription_handler import TranscriptionHandler, TranscriptionService
from utils.transcript_utils import TranscriptManager

class TranscriptionApp:
    def __init__(self):
        self.setup_session_state()
        Settings.setup_aws_credentials()
        self.transcription_service = TranscriptionService()

    @staticmethod
    def setup_session_state():
        if 'transcript_text' not in st.session_state:
            st.session_state.transcript_text = []

    async def run_transcription(self):
        try:
            start_time = time.time()
            stream = await AWSService.create_transcribe_stream()
            handler = TranscriptionHandler(stream.output_stream)
            
            audio_service = AudioService()
            audio_stream, input_queue = await audio_service.create_mic_stream()
            audio_stream = audio_service.process_audio_stream(audio_stream, input_queue)

            while not self.transcription_service.stop_transcription:
                if time.time() - start_time >= Settings.MAX_DURATION:
                    st.warning("30-minute time limit reached")
                    break
                
                await asyncio.gather(
                    self.transcription_service.write_chunks(stream, audio_stream),
                    handler.handle_events()
                )
            
            await stream.input_stream.end_stream()

        except Exception as e:
            st.error(f"Transcription error: {e}")

    def render(self):
        st.title("Live Audio Transcription")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Start Transcription"):
                asyncio.run(self.run_transcription())
        
        with col2:
            if st.button("Stop Transcription"):
                self.transcription_service.stop()
                st.warning("Transcription stopped")
        
        with col3:
            if st.button("Clear Transcript"):
                TranscriptManager.clear_transcript()
        
        if st.session_state.transcript_text:
            st.subheader("Transcript Download")
            TranscriptManager.save_transcript()

def main():
    app = TranscriptionApp()
    app.render()

if __name__ == "__main__":
    main()