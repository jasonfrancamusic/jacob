from __future__ import annotations

import base64
import os

import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


@dataclass
class VoiceResult:
    audio_base64: str | None
    provider: str
    voice: str
    used_fallback: bool
    text: str

    def as_dict(self) -> dict:
        return {
            "audio_base64": self.audio_base64,
            "provider": self.provider,
            "voice": self.voice,
            "used_fallback": self.used_fallback,
            "text": self.text,
        }


class VoiceEngine:
    """Premium voice layer for Jacob.

    Provider order:
    1. ElevenLabs, for the most natural Jacob voice.
    2. OpenAI TTS, as premium fallback.
    3. Browser speechSynthesis, as development fallback.
    """

    def __init__(self) -> None:
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("JACOB_TTS_MODEL", "gpt-4o-mini-tts")
        self.openai_voice = os.getenv("JACOB_TTS_VOICE", "onyx")
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None

        self.eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.eleven_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
        self.eleven_model = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
        self.eleven_output_format = os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128")

    def prepare_text(self, text: str) -> str:
        """Keep Brazilian Portuguese, only guide Jacob/Jason pronunciation."""
        return (
            text.replace("Jacob", "Jay-cub")
            .replace("JACOB", "Jay-cub")
            .replace("Jason", "Jay-son")
            .replace("JASON", "Jay-son")
        )

    def synthesize(self, text: str) -> VoiceResult:
        prepared = self.prepare_text(text)

        eleven = self._synthesize_elevenlabs(prepared)
        if eleven:
            return eleven

        openai = self._synthesize_openai(prepared)
        if openai:
            return openai

        return VoiceResult(
            audio_base64=None,
            provider="browser-fallback",
            voice="system",
            used_fallback=True,
            text=prepared,
        )

    def _synthesize_elevenlabs(self, prepared: str) -> VoiceResult | None:
        if not self.eleven_api_key:
            return None

        url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.eleven_voice_id}"
            f"?output_format={self.eleven_output_format}"
        )
        headers = {
            "xi-api-key": self.eleven_api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }
        payload = {
            "text": prepared,
            "model_id": self.eleven_model,
            "voice_settings": {
                "stability": 0.44,
                "similarity_boost": 0.82,
                "style": 0.36,
                "use_speaker_boost": True,
            },
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            response.raise_for_status()
            return VoiceResult(
                audio_base64=base64.b64encode(response.content).decode("utf-8"),
                provider="elevenlabs",
                voice=self.eleven_voice_id,
                used_fallback=False,
                text=prepared,
            )
        except Exception:
            return None

    def _synthesize_openai(self, prepared: str) -> VoiceResult | None:
        if not self.openai_client:
            return None

        try:
            response = self.openai_client.audio.speech.create(
                model=self.openai_model,
                voice=self.openai_voice,
                input=prepared,
                instructions=(
                    "Fale em português brasileiro natural, calmo e premium. "
                    "Apenas os nomes Jay-cub e Jay-son devem soar como nomes em inglês. "
                    "Use pausas naturais e não seja robótico."
                ),
                response_format="mp3",
            )
            audio_bytes = response.read()
            return VoiceResult(
                audio_base64=base64.b64encode(audio_bytes).decode("utf-8"),
                provider="openai-tts",
                voice=self.openai_voice,
                used_fallback=False,
                text=prepared,
            )
        except Exception:
            return None
