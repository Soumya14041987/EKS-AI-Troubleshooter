import os
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import chromadb
from typing import List, Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class RAGKnowledgeBase:
    def __init__(self, persist_directory: str = "./knowledge_base"):
        self.persist_directory = persist_directory
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="k8s_troubleshooting",
            metadata={"description": "Kubernetes and AWS troubleshooting knowledge"}
        )
        self.knowledge_sources = {
            "kubernetes": [
                "https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/",
                "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/",
                "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/",
                "https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/",
            ],
            "aws_eks": [
                "https://docs.aws.amazon.com/eks/latest/userguide/troubleshooting.html",
                "https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html",
                "https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html",
            ]
        }
        self.error_patterns = {
            "CrashLoopBackOff": {
                "description": "Pod is crashing repeatedly and Kubernetes is backing off restart attempts",
                "common_causes": [
                    "Application startup failure",
                    "Missing configuration or secrets",
                    "Resource constraints",
                    "Health check failures"
                ],
                "solutions": [
                    "Check pod logs: kubectl logs <pod-name> --previous",
                    "Verify resource limits and requests",
                    "Check environment variables and secrets",
                    "Review application startup sequence"
                ]
            },
            "OOMKilled": {
                "description": "Pod was killed due to out-of-memory condition",
                "common_causes": [
                    "Memory limit too low",
                    "Memory leak in application",
                    "Insufficient node memory",
                    "No memory limits set"
                ],
                "solutions": [
                    "Increase memory limits in deployment",
                    "Add memory requests to prevent overcommit",
                    "Profile application memory usage",
                    "Consider horizontal pod autoscaling"
                ]
            },
            "ImagePullBackOff": {
                "description": "Kubernetes cannot pull the container image",
                "common_causes": [
                    "Image doesn't exist",
                    "Registry authentication failure",
                    "Network connectivity issues",
                    "Image tag not found"
                ],
                "solutions": [
                    "Verify image name and tag",
                    "Check registry credentials",
                    "Test network connectivity to registry",
                    "Use imagePullSecrets if needed"
                ]
            }
        }
    
    async def initialize_knowledge_base(self):
        """Initialize the knowledge base with curated content"""
        try:
            # Check if knowledge base already exists
            if self.collection.count() > 0:
                logger.info("Knowledge base already initialized")
                return
            
            logger.info("Initializing knowledge base...")
            
            # Add error patterns
            await self._add_error_patterns()
            
            # Add curated troubleshooting content
            await self._add_curated_content()
            
            logger.info("Knowledge base initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}")
    
    async def _add_error_patterns(self):
        """Add error patterns to knowledge base"""
        for error_type, info in self.error_patterns.items():
            content = f"""
            Error Type: {error_type}
            Description: {info['description']}
            
            Common Causes:
            {chr(10).join(f"- {cause}" for cause in info['common_causes'])}
            
            Solutions:
            {chr(10).join(f"- {solution}" for solution in info['solutions'])}
            """
            
            embedding = self.model.encode([content])[0].tolist()
            
            self.collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[{
                    "type": "error_pattern",
                    "error_type": error_type,
                    "source": "curated"
                }],
                ids=[f"error_pattern_{error_type}"]
            )
    
    async def _add_curated_content(self):
        """Add curated troubleshooting content"""
        curated_content = [
            {
                "title": "Pod Troubleshooting Checklist",
                "content": """
                Pod Troubleshooting Steps:
                1. Check pod status: kubectl get pods
                2. Describe pod: kubectl describe pod <pod-name>
                3. Check logs: kubectl logs <pod-name>
                4. Check events: kubectl get events --sort-by=.metadata.creationTimestamp
                5. Verify resource limits and requests
                6. Check node resources: kubectl top nodes
                7. Verify image availability
                8. Check service account permissions
                """,
                "category": "troubleshooting"
            },
            {
                "title": "Resource Optimization Best Practices",
                "content": """
                Resource Optimization Guidelines:
                1. Always set resource requests and limits
                2. Use horizontal pod autoscaling for variable workloads
                3. Monitor actual resource usage vs requests
                4. Use vertical pod autoscaling for right-sizing
                5. Implement resource quotas at namespace level
                6. Use node affinity for workload placement
                7. Consider spot instances for cost optimization
                """,
                "category": "optimization"
            },
            {
                "title": "EKS Specific Troubleshooting",
                "content": """
                EKS Troubleshooting Tips:
                1. Check IAM roles and policies
                2. Verify VPC and subnet configuration
                3. Check security group rules
                4. Validate cluster endpoint access
                5. Review CloudWatch logs
                6. Check node group health
                7. Verify add-on compatibility
                8. Monitor cluster autoscaler logs
                """,
                "category": "eks"
            }
        ]
        
        for idx, item in enumerate(curated_content):
            content = f"Title: {item['title']}\n\n{item['content']}"
            embedding = self.model.encode([content])[0].tolist()
            
            self.collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[{
                    "type": "curated_content",
                    "category": item['category'],
                    "title": item['title'],
                    "source": "curated"
                }],
                ids=[f"curated_{idx}"]
            )
    
    async def query_knowledge_base(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Query the knowledge base for relevant information"""
        try:
            query_embedding = self.model.encode([query])[0].tolist()
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            formatted_results = []
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "relevance_score": 1 - results['distances'][0][i]  # Convert distance to similarity
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying knowledge base: {e}")
            return []
    
    async def get_contextual_solution(self, issue_type: str, pod_info: Dict[str, Any] = None) -> str:
        """Get contextual solution for a specific issue"""
        try:
            # Create context-aware query
            query = f"{issue_type} kubernetes pod troubleshooting"
            if pod_info:
                query += f" {pod_info.get('status', '')} {pod_info.get('namespace', '')}"
            
            results = await self.query_knowledge_base(query, n_results=2)
            
            if not results:
                return f"No specific guidance found for {issue_type}. Please check pod logs and events."
            
            # Combine results into comprehensive solution
            solution = f"## Troubleshooting {issue_type}\n\n"
            
            for result in results:
                if result['relevance_score'] > 0.7:  # Only include highly relevant results
                    solution += f"{result['content']}\n\n"
            
            return solution
            
        except Exception as e:
            logger.error(f"Error getting contextual solution: {e}")
            return f"Error retrieving solution for {issue_type}. Please check logs manually."
    
    async def add_custom_knowledge(self, title: str, content: str, category: str = "custom"):
        """Add custom knowledge to the base"""
        try:
            embedding = self.model.encode([content])[0].tolist()
            doc_id = f"custom_{title.lower().replace(' ', '_')}"
            
            self.collection.add(
                documents=[f"Title: {title}\n\n{content}"],
                embeddings=[embedding],
                metadatas=[{
                    "type": "custom",
                    "category": category,
                    "title": title,
                    "source": "user_added"
                }],
                ids=[doc_id]
            )
            
            logger.info(f"Added custom knowledge: {title}")
            
        except Exception as e:
            logger.error(f"Error adding custom knowledge: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        try:
            count = self.collection.count()
            return {
                "total_documents": count,
                "status": "ready" if count > 0 else "empty",
                "model": "all-MiniLM-L6-v2",
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"status": "error", "error": str(e)}