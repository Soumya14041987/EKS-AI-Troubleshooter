import os
from typing import List

class Settings:
    # Application settings
    APP_NAME: str = "EKS AI Troubleshooter"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # AWS settings
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    
    # Kubernetes settings
    KUBECONFIG_PATH: str = os.getenv("KUBECONFIG", "~/.kube/config")
    
    # Analysis settings
    MAX_PODS_PER_ANALYSIS: int = int(os.getenv("MAX_PODS_PER_ANALYSIS", "100"))
    MAX_EVENTS_PER_ANALYSIS: int = int(os.getenv("MAX_EVENTS_PER_ANALYSIS", "50"))
    
    # Log streaming settings
    LOG_TAIL_LINES: int = int(os.getenv("LOG_TAIL_LINES", "100"))
    LOG_STREAM_TIMEOUT: int = int(os.getenv("LOG_STREAM_TIMEOUT", "300"))
    
    # Security settings
    API_TOKEN: str = os.getenv("API_TOKEN", "")
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    
    # Issue detection thresholds
    HIGH_RESTART_THRESHOLD: int = int(os.getenv("HIGH_RESTART_THRESHOLD", "5"))
    MEMORY_USAGE_THRESHOLD: float = float(os.getenv("MEMORY_USAGE_THRESHOLD", "80.0"))
    CPU_USAGE_THRESHOLD: float = float(os.getenv("CPU_USAGE_THRESHOLD", "80.0"))
    
    # RAG settings
    ENABLE_RAG: bool = os.getenv("ENABLE_RAG", "true").lower() == "true"
    KNOWLEDGE_BASE_PATH: str = os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

settings = Settings()