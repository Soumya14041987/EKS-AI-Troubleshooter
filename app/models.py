from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ClusterConfig(BaseModel):
    cluster_name: str
    region: str
    kubeconfig_path: Optional[str] = None

class AnalysisRequest(BaseModel):
    namespace: str = "default"
    include_logs: bool = False

class Issue(BaseModel):
    type: str
    severity: str
    resource: str
    description: str
    namespace: str

class Recommendation(BaseModel):
    issue_type: str
    action: str
    description: str
    command: Optional[str] = None

class AnalysisResponse(BaseModel):
    issues: List[Issue]
    recommendations: List[Recommendation]
    cluster_health: str
    insights: Optional[List[str]] = []

class PodInfo(BaseModel):
    name: str
    namespace: str
    status: str
    ready: str
    restarts: int
    age: str
    cpu_usage: Optional[str] = None
    memory_usage: Optional[str] = None

class RAGQuery(BaseModel):
    query: str
    max_results: int = 3

class RAGResult(BaseModel):
    content: str
    metadata: Dict[str, Any]
    relevance_score: float

class KnowledgeEntry(BaseModel):
    title: str
    content: str
    category: str = "custom"

class ClusterInsights(BaseModel):
    namespace: str
    total_pods: int
    running_pods: int
    problematic_pods: int
    high_restart_pods: int
    ai_insights: List[str]
    suggestions: List[str]