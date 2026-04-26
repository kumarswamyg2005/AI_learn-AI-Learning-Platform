"""Speech-to-text and text-to-speech"""

import os
import io
from typing import Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False

openai.api_key = openai.api_key  # Uses env var


class SpeechProcessor:
    """Handle speech-to-text and text-to-speech conversion"""

    def __init__(self):
        self.google_client = None
        if GOOGLE_TTS_AVAILABLE and os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            try:
                self.google_client = texttospeech.TextToSpeechClient()
            except Exception as e:
                print(f"Warning: Could not initialize Google TTS client: {e}")

    def speech_to_text(self, audio_file) -> str:
        """
        Convert audio to text using OpenAI Whisper (base model).

        Args:
            audio_file: File object or path to audio file (mp3, mp4, mpeg, mpga, m4a, wav, webm)

        Returns:
            Transcribed text
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed")

        try:
            # Handle both file paths and file objects
            if isinstance(audio_file, str):
                with open(audio_file, 'rb') as f:
                    transcript = openai.Audio.transcribe(
                        model="whisper-1",
                        file=f
                    )
            else:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file
                )

            return transcript.get("text", "")

        except Exception as e:
            print(f"❌ Speech-to-text error: {e}")
            return ""

    def text_to_speech(
        self,
        text: str,
        language: str = "en",
        output_path: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Convert text to speech.

        Tries in order: Google Cloud TTS → gTTS → fallback

        Args:
            text: Text to convert
            language: Language code (en, hi, te, etc.)
            output_path: Optional path to save audio file

        Returns:
            Audio bytes or None if failed
        """
        if not text:
            return None

        # Try Google Cloud TTS first (highest quality)
        if self.google_client:
            try:
                return self._google_text_to_speech(text, language, output_path)
            except Exception as e:
                print(f"Google TTS error: {e}")

        # Fallback to gTTS
        if GTTS_AVAILABLE:
            try:
                return self._gtts_text_to_speech(text, language, output_path)
            except Exception as e:
                print(f"gTTS error: {e}")

        print("❌ No text-to-speech service available")
        return None

    def _google_text_to_speech(
        self,
        text: str,
        language: str,
        output_path: Optional[str]
    ) -> bytes:
        """Convert using Google Cloud Text-to-Speech"""
        # Language to voice mapping
        language_voices = {
            "en": ("en-US", "en-US-Neural2-C"),
            "hi": ("hi-IN", "hi-IN-Neural2-A"),
            "te": ("te-IN", "te-IN-Standard-A"),
            "kn": ("kn-IN", "kn-IN-Standard-A"),
            "ml": ("ml-IN", "ml-IN-Standard-A"),
        }

        lang_code, voice = language_voices.get(language, ("en-US", "en-US-Neural2-C"))

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code,
            name=voice
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.google_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        audio_bytes = response.audio_content

        if output_path:
            with open(output_path, 'wb') as f:
                f.write(audio_bytes)

        return audio_bytes

    def _gtts_text_to_speech(
        self,
        text: str,
        language: str,
        output_path: Optional[str]
    ) -> bytes:
        """Convert using Google Text-to-Speech (gTTS)"""
        tts = gTTS(text=text, lang=language, slow=False)

        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_bytes = audio_buffer.getvalue()

        if output_path:
            with open(output_path, 'wb') as f:
                f.write(audio_bytes)

        return audio_bytes

    def process_voice_input(self, audio_file) -> str:
        """
        Process voice input and return transcribed text.

        Args:
            audio_file: Audio file

        Returns:
            Transcribed text
        """
        return self.speech_to_text(audio_file)

    def process_voice_output(
        self,
        text: str,
        language: str = "en",
        output_path: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Process voice output from text.

        Args:
            text: Text to speak
            language: Language
            output_path: Optional save path

        Returns:
            Audio bytes
        """
        return self.text_to_speech(text, language, output_path)
