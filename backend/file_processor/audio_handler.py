from pathlib import Path
from faster_whisper import WhisperModel


class AudioTranscriber:
    """
    Transcribes audio files to text using faster-whisper (CTranslate2 backend).

    Supported formats: mp3, wav, flac, ogg, m4a, wma, aac
    (anything ffmpeg can decode — faster-whisper uses ffmpeg internally)
    """

    SUPPORTED_EXTENSIONS = {
        ".mp3", ".wav", ".flac", ".ogg", ".m4a", ".wma", ".aac", ".webm",
    }

    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8",
    ):
        """
        Args:
            model_size: Whisper model size — "tiny", "base", "small", "medium", "large-v3".
                        Bigger = more accurate but slower.
            device: "cpu" or "cuda".
            compute_type: "int8" (fastest on CPU), "float16" (GPU), "float32".
        """
        print(f"--- [LOG] Loading Whisper model: {model_size} ({device}/{compute_type}) ---")
        self.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to the audio file.
            language: ISO-639-1 code (e.g. "en", "zh"). None = auto-detect.

        Returns:
            str: Full transcription text.
        """
        path = Path(audio_path)
        if not path.exists():
            print(f"--- [ERROR] Audio file not found: {audio_path} ---")
            return ""

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            print(f"--- [ERROR] Unsupported audio format: {path.suffix} ---")
            return ""

        try:
            segments, info = self.model.transcribe(
                str(path),
                language=language,
                beam_size=5,
                vad_filter=True,  # skip silence
            )

            print(
                f"--- [LOG] Detected language: {info.language} "
                f"(probability {info.language_probability:.2f}) ---"
            )

            transcript_parts: list[str] = []
            for segment in segments:
                transcript_parts.append(segment.text.strip())

            transcript = " ".join(transcript_parts)
            print(
                f"--- [LOG] Transcribed {path.name}: "
                f"{len(transcript)} chars ---"
            )
            return transcript

        except Exception as e:
            print(f"--- [ERROR] Transcription failed for {audio_path}: {e} ---")
            return ""

    def transcribe_with_timestamps(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> list[dict]:
        """
        Transcribe with per-segment timestamps. Useful for long recordings.

        Returns:
            list[dict]: Each dict has 'start', 'end', 'text' keys.
        """
        path = Path(audio_path)
        if not path.exists():
            return []

        try:
            segments, info = self.model.transcribe(
                str(path),
                language=language,
                beam_size=5,
                vad_filter=True,
            )

            results = []
            for seg in segments:
                results.append({
                    "start": round(seg.start, 2),
                    "end": round(seg.end, 2),
                    "text": seg.text.strip(),
                })
            return results

        except Exception as e:
            print(f"--- [ERROR] Timestamped transcription failed: {e} ---")
            return []
