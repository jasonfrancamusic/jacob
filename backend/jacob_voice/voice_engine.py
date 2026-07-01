from __future__ import annotations

import base64
import os
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

    Browser speechSynthesis remains only a fallback.
    Official Jacob voice should come from a neural voice provider.
    """

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("JACOB_TTS_MODEL", "gpt-4o-mini-tts")
        self.voice = os.getenv("JACOB_TTS_VOICE", "onyx")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def prepare_text(self, text: str) -> str:
        return (
            text.replace("Jacob", "Jay-cub")
            .replace("JACOB", "Jay-cub")
            .replace("Jason", "Jay-son")
            .replace("JASON", "Jay-son")
        )

    def synthesize(self, text: str) -> VoiceResult:
        prepared = self.prepare_text(text)

        if not self.client:
            return VoiceResult(
                audio_base64=None,
                provider="browser-fallback",
                voice="system",
                used_fallback=True,
                text=prepared,
            )

        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=self.voice,
                input=prepared,
                instructions=(
                    "Speak like a calm, premium digital partner. "
                    "Use natural pacing, short pauses, warm confidence, and no exaggerated emotion. "
                    "Pronounce Jacob like the English name Jay-cub and Jason like Jay-son."
                ),
                response_format="mp3",
            )
            audio_bytes = response.read()
            return VoiceResult(
                audio_base64=base64.b64encode(audio_bytes).decode("utf-8"),
                provider="openai-tts",
                voice=self.voice,
                used_fallback=False,
                text=prepared,
            )
        except Exception:
            return VoiceResult(
                audio_base64=None,
                provider="browser-fallback",
                voice="system",
                used_fallback=True,
                text=prepared,
            )
