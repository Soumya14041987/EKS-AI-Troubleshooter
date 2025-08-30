from typing import List, Dict, Any
from models import Issue, Recommendation
from rag_knowledge_base import RAGKnowledgeBase
import re
import logging
import asyncio

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self):
        self.rag_kb = RAGKnowledgeBase()
        self.issue_patterns = {
            "CrashLoopBackOff": {
                "severity": "high",
                "description": "Pod is crashing repeatedly",
                "remediation": "Check pod logs and fix application issues"
            },
            "OOMKilled": {
                "severity": "high", 
                "description": "Pod killed due to out of memory",
                "remediation": "Increase memory limits or optimize application"
            },
            "ImagePullBackOff": {
                "severity": "medium",
                "description": "Cannot pull container image",
                "remediation": "Check image name, registry access, and credentials"
            },
            "Pending": {
                "severity": "medium",
                "description": "Pod cannot be scheduled",
                "remediation": "Check resource requests and node capacity"
            }
        }
        # Initialize RAG knowledge base
        asyncio.create_task(self._initialize_rag())
    
    async def _initialize_rag(self):
        """Initialize RAG knowledge base"""
        try:
            await self.rag_kb.initialize_knowledge_base()
            logger.info("RAG knowledge base initialized")
        except Exception as e:
            logger.error(f"Failed to initialize RAG: {e}")
    
    def detect_issues(self, pods: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> List[Issue]:
        issues = []
        
        # Analyze pod status
        for pod in pods:
            if pod["status"] in self.issue_patterns:
                issue = Issue(
                    type=pod["status"],
                    severity=self.issue_patterns[pod["status"]]["severity"],
                    resource=f"Pod/{pod['name']}",
                    description=self.issue_patterns[pod["status"]]["description"],
                    namespace=pod["namespace"]
                )
                issues.append(issue)
            
            # Check restart count
            if pod["restarts"] > 5:
                issue = Issue(
                    type="HighRestartCount",
                    severity="medium",
                    resource=f"Pod/{pod['name']}",
                    description=f"Pod has restarted {pod['restarts']} times",
                    namespace=pod["namespace"]
                )
                issues.append(issue)
        
        # Analyze events
        for event in events:
            if event["type"] == "Warning":
                if "OOMKilled" in event["reason"]:
                    issue = Issue(
                        type="OOMKilled",
                        severity="high",
                        resource=event["object"],
                        description=event["message"],
                        namespace="default"
                    )
                    issues.append(issue)
                elif "Failed" in event["reason"]:
                    issue = Issue(
                        type="FailedEvent",
                        severity="medium",
                        resource=event["object"],
                        description=event["message"],
                        namespace="default"
                    )
                    issues.append(issue)
        
        return issues
    
    async def generate_recommendations(self, issues: List[Issue]) -> List[Recommendation]:
        recommendations = []
        
        for issue in issues:
            # Get RAG-enhanced recommendations
            try:
                rag_solution = await self.rag_kb.get_contextual_solution(
                    issue.type, 
                    {"status": issue.type, "namespace": issue.namespace}
                )
                
                # Create enhanced recommendation with RAG content
                if issue.type == "OOMKilled":
                    rec = Recommendation(
                        issue_type=issue.type,
                        action="Increase Memory Limits (RAG-Enhanced)",
                        description=f"AI Analysis: {rag_solution[:200]}...",
                        command="kubectl patch deployment <deployment-name> -p '{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"<container-name>\",\"resources\":{\"limits\":{\"memory\":\"512Mi\"}}}]}}}}'"
                    )
                    recommendations.append(rec)
                
                elif issue.type == "CrashLoopBackOff":
                    rec = Recommendation(
                        issue_type=issue.type,
                        action="Diagnose Crash Loop (RAG-Enhanced)",
                        description=f"AI Analysis: {rag_solution[:200]}...",
                        command=f"kubectl logs {issue.resource.split('/')[-1]} -n {issue.namespace} --previous"
                    )
                    recommendations.append(rec)
                
                elif issue.type == "ImagePullBackOff":
                    rec = Recommendation(
                        issue_type=issue.type,
                        action="Fix Image Pull Issues (RAG-Enhanced)",
                        description=f"AI Analysis: {rag_solution[:200]}...",
                        command=f"kubectl describe pod {issue.resource.split('/')[-1]} -n {issue.namespace}"
                    )
                    recommendations.append(rec)
                
                elif issue.type == "Pending":
                    rec = Recommendation(
                        issue_type=issue.type,
                        action="Resolve Scheduling Issues (RAG-Enhanced)",
                        description=f"AI Analysis: {rag_solution[:200]}...",
                        command=f"kubectl describe pod {issue.resource.split('/')[-1]} -n {issue.namespace}"
                    )
                    recommendations.append(rec)
                
                elif issue.type == "HighRestartCount":
                    rec = Recommendation(
                        issue_type=issue.type,
                        action="Investigate Frequent Restarts (RAG-Enhanced)",
                        description=f"AI Analysis: {rag_solution[:200]}...",
                        command=f"kubectl describe pod {issue.resource.split('/')[-1]} -n {issue.namespace}"
                    )
                    recommendations.append(rec)
                
            except Exception as e:
                logger.error(f"Error generating RAG recommendation for {issue.type}: {e}")
                # Fallback to basic recommendations
                rec = self._get_basic_recommendation(issue)
                if rec:
                    recommendations.append(rec)
        
        # Add general RAG-enhanced recommendations
        if any(issue.type in ["OOMKilled", "HighRestartCount"] for issue in issues):
            try:
                general_advice = await self.rag_kb.query_knowledge_base(
                    "resource optimization kubernetes best practices", n_results=1
                )
                if general_advice:
                    rec = Recommendation(
                        issue_type="ResourceOptimization",
                        action="Apply Resource Best Practices (RAG-Enhanced)",
                        description=f"AI Guidance: {general_advice[0]['content'][:200]}...",
                        command="kubectl top pods --all-namespaces"
                    )
                    recommendations.append(rec)
            except Exception as e:
                logger.error(f"Error generating general RAG recommendation: {e}")
        
        return recommendations
    
    def _get_basic_recommendation(self, issue: Issue) -> Recommendation:
        """Fallback basic recommendations when RAG fails"""
        basic_recs = {
            "OOMKilled": Recommendation(
                issue_type=issue.type,
                action="Increase Memory Limits",
                description="Pod was killed due to memory constraints. Increase memory limits.",
                command="kubectl patch deployment <deployment-name> -p '{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"<container-name>\",\"resources\":{\"limits\":{\"memory\":\"512Mi\"}}}]}}}}'"
            ),
            "CrashLoopBackOff": Recommendation(
                issue_type=issue.type,
                action="Check Application Logs",
                description="Pod is crashing repeatedly. Check logs for application errors.",
                command=f"kubectl logs {issue.resource.split('/')[-1]} -n {issue.namespace}"
            ),
            "ImagePullBackOff": Recommendation(
                issue_type=issue.type,
                action="Verify Image and Registry Access",
                description="Cannot pull container image. Check image name and registry credentials.",
                command=f"kubectl describe pod {issue.resource.split('/')[-1]} -n {issue.namespace}"
            )
        }
        return basic_recs.get(issue.type)
    
    async def get_intelligent_insights(self, cluster_data: Dict[str, Any]) -> List[str]:
        """Get AI-powered insights about cluster health"""
        insights = []
        
        try:
            # Query RAG for general cluster health insights
            health_query = f"kubernetes cluster health monitoring best practices"
            rag_results = await self.rag_kb.query_knowledge_base(health_query, n_results=2)
            
            for result in rag_results:
                if result['relevance_score'] > 0.6:
                    insights.append(f"💡 AI Insight: {result['content'][:150]}...")
            
            # Add specific insights based on cluster data
            if cluster_data.get('problematic_pods', 0) > 0:
                insights.append(f"⚠️ {cluster_data['problematic_pods']} pods need attention")
            
            if cluster_data.get('high_restart_pods', 0) > 0:
                insights.append(f"🔄 {cluster_data['high_restart_pods']} pods have high restart counts")
            
        except Exception as e:
            logger.error(f"Error generating intelligent insights: {e}")
            insights.append("💡 Enable detailed monitoring for better insights")
        
        return insights
    
    def analyze_resource_usage(self, pods: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze resource usage patterns and provide optimization suggestions"""
        analysis = {
            "total_pods": len(pods),
            "running_pods": len([p for p in pods if p["status"] == "Running"]),
            "problematic_pods": len([p for p in pods if p["status"] not in ["Running", "Succeeded"]]),
            "high_restart_pods": len([p for p in pods if p["restarts"] > 3]),
            "suggestions": []
        }
        
        if analysis["problematic_pods"] > 0:
            analysis["suggestions"].append("Investigate non-running pods for potential issues")
        
        if analysis["high_restart_pods"] > 0:
            analysis["suggestions"].append("Review pods with high restart counts for stability issues")
        
        # Add cost optimization suggestions
        if analysis["total_pods"] > 10:
            analysis["suggestions"].append("Consider implementing horizontal pod autoscaling")
        
        return analysis
    
    async def get_rag_stats(self) -> Dict[str, Any]:
        """Get RAG knowledge base statistics"""
        return self.rag_kb.get_stats()