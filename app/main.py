from fastapi import FastAPI, HTTPException, Depends, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from kubernetes_client import KubernetesClient
from ai_analyzer import AIAnalyzer
from models import ClusterConfig, AnalysisRequest, AnalysisResponse
import asyncio
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EKS AI Troubleshooter", 
    version="1.0.0",
    description="🤖 Intelligent EKS Troubleshooter with RAG-enhanced knowledge base"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global instances
k8s_client = KubernetesClient()
ai_analyzer = AIAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 Starting EKS AI Troubleshooter...")
    # RAG initialization happens in AIAnalyzer constructor

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    try:
        with open("templates/dashboard.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html><body>
        <h1>🤖 EKS AI Troubleshooter</h1>
        <p>Dashboard template not found. Please ensure templates/dashboard.html exists.</p>
        </body></html>
        """)

@app.post("/api/connect")
async def connect_cluster(config: ClusterConfig):
    """Connect to an EKS cluster"""
    try:
        success = await k8s_client.connect(config.cluster_name, config.region)
        if success:
            return {
                "status": "connected", 
                "cluster": config.cluster_name,
                "region": config.region,
                "message": f"Successfully connected to {config.cluster_name}"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to connect to cluster")
    except Exception as e:
        logger.error(f"Connection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_cluster(request: AnalysisRequest):
    """Analyze cluster with RAG-enhanced AI recommendations"""
    try:
        # Get cluster data
        pods = await k8s_client.get_pods(request.namespace)
        events = await k8s_client.get_events(request.namespace)
        
        # Analyze issues
        issues = ai_analyzer.detect_issues(pods, events)
        
        # Generate RAG-enhanced recommendations
        recommendations = await ai_analyzer.generate_recommendations(issues)
        
        # Get intelligent insights
        cluster_data = ai_analyzer.analyze_resource_usage(pods)
        insights = await ai_analyzer.get_intelligent_insights(cluster_data)
        
        return AnalysisResponse(
            issues=issues,
            recommendations=recommendations,
            cluster_health="healthy" if not issues else "issues_detected",
            insights=insights
        )
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/logs/{namespace}/{pod_name}")
async def websocket_logs(websocket: WebSocket, namespace: str, pod_name: str):
    """Stream pod logs via WebSocket"""
    await websocket.accept()
    try:
        async for log_line in k8s_client.stream_logs(namespace, pod_name):
            await websocket.send_text(log_line)
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()

@app.get("/api/pods/{namespace}")
async def get_pods(namespace: str = "default"):
    """Get pods in a namespace"""
    try:
        pods = await k8s_client.get_pods(namespace)
        return {"pods": pods, "namespace": namespace, "count": len(pods)}
    except Exception as e:
        logger.error(f"Error getting pods: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        rag_stats = await ai_analyzer.get_rag_stats()
        return {
            "status": "healthy",
            "cluster_connected": k8s_client.current_cluster is not None,
            "current_cluster": k8s_client.current_cluster,
            "rag_knowledge_base": rag_stats,
            "version": "1.0.0"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/api/rag/query")
async def query_knowledge_base(q: str, limit: int = 3):
    """Query the RAG knowledge base directly"""
    try:
        if not q:
            raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
        
        results = await ai_analyzer.rag_kb.query_knowledge_base(q, n_results=limit)
        return {
            "query": q,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"RAG query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rag/add-knowledge")
async def add_custom_knowledge(title: str, content: str, category: str = "custom"):
    """Add custom knowledge to the RAG system"""
    try:
        await ai_analyzer.rag_kb.add_custom_knowledge(title, content, category)
        return {
            "status": "success",
            "message": f"Added knowledge: {title}",
            "category": category
        }
    except Exception as e:
        logger.error(f"Error adding knowledge: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/insights/{namespace}")
async def get_cluster_insights(namespace: str = "default"):
    """Get AI-powered cluster insights"""
    try:
        pods = await k8s_client.get_pods(namespace)
        cluster_data = ai_analyzer.analyze_resource_usage(pods)
        insights = await ai_analyzer.get_intelligent_insights(cluster_data)
        
        return {
            "namespace": namespace,
            "cluster_data": cluster_data,
            "ai_insights": insights,
            "timestamp": asyncio.get_event_loop().time()
        }
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cost-optimization")
async def get_cost_optimization_tips():
    """Get cost optimization recommendations"""
    try:
        cost_tips = await ai_analyzer.rag_kb.query_knowledge_base(
            "kubernetes cost optimization spot instances resource limits", 
            n_results=3
        )
        
        return {
            "tips": cost_tips,
            "estimated_savings": "Up to 70% with spot instances",
            "current_setup": "Optimized for <$15/month"
        }
    except Exception as e:
        logger.error(f"Error getting cost tips: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=False  # Set to True for development
    )