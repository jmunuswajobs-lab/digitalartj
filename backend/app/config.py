
import os

class Settings:
    API_PREFIX: str = "/api"
    SD_API_URL: str = os.getenv("SD_API_URL", "http://localhost:7860")
    SD_API_MODE: str = os.getenv("SD_API_MODE", "automatic1111")  # or "comfyui", "mock"

    # where to save generated files
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "./outputs")

settings = Settings()
