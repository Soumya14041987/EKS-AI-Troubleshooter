from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
import boto3
import asyncio
from typing import List, Dict, Any, AsyncGenerator
from models import PodInfo, Issue
import logging

logger = logging.getLogger(__name__)

class KubernetesClient:
    def __init__(self):
        self.v1 = None
        self.current_cluster = None
    
    async def connect(self, cluster_name: str, region: str) -> bool:
        try:
            # Update kubeconfig for EKS cluster
            eks_client = boto3.client('eks', region_name=region)
            
            # Get cluster info
            cluster_info = eks_client.describe_cluster(name=cluster_name)
            
            # Configure kubectl
            import subprocess
            subprocess.run([
                'aws', 'eks', 'update-kubeconfig',
                '--region', region,
                '--name', cluster_name
            ], check=True)
            
            # Load kubeconfig
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            self.current_cluster = cluster_name
            
            # Test connection
            await self._test_connection()
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to cluster {cluster_name}: {e}")
            return False
    
    async def _test_connection(self):
        try:
            self.v1.list_namespace(limit=1)
        except ApiException as e:
            raise Exception(f"Cannot connect to cluster: {e}")
    
    async def get_pods(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            pods = self.v1.list_namespaced_pod(namespace=namespace)
            pod_list = []
            
            for pod in pods.items:
                pod_info = {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "status": pod.status.phase,
                    "ready": self._get_ready_status(pod),
                    "restarts": self._get_restart_count(pod),
                    "age": self._calculate_age(pod.metadata.creation_timestamp),
                    "node": pod.spec.node_name or "N/A"
                }
                pod_list.append(pod_info)
            
            return pod_list
            
        except ApiException as e:
            logger.error(f"Error getting pods: {e}")
            return []
    
    async def get_events(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            events = self.v1.list_namespaced_event(namespace=namespace)
            event_list = []
            
            for event in events.items:
                event_info = {
                    "type": event.type,
                    "reason": event.reason,
                    "message": event.message,
                    "object": f"{event.involved_object.kind}/{event.involved_object.name}",
                    "timestamp": event.first_timestamp,
                    "count": event.count or 1
                }
                event_list.append(event_info)
            
            return event_list
            
        except ApiException as e:
            logger.error(f"Error getting events: {e}")
            return []
    
    async def stream_logs(self, namespace: str, pod_name: str) -> AsyncGenerator[str, None]:
        try:
            w = watch.Watch()
            for event in w.stream(
                self.v1.read_namespaced_pod_log,
                name=pod_name,
                namespace=namespace,
                follow=True,
                _preload_content=False
            ):
                yield event
                
        except ApiException as e:
            yield f"Error streaming logs: {e}"
    
    def _get_ready_status(self, pod) -> str:
        if not pod.status.container_statuses:
            return "0/0"
        
        ready_count = sum(1 for cs in pod.status.container_statuses if cs.ready)
        total_count = len(pod.status.container_statuses)
        return f"{ready_count}/{total_count}"
    
    def _get_restart_count(self, pod) -> int:
        if not pod.status.container_statuses:
            return 0
        
        return sum(cs.restart_count for cs in pod.status.container_statuses)
    
    def _calculate_age(self, creation_timestamp) -> str:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        age = now - creation_timestamp
        
        days = age.days
        hours, remainder = divmod(age.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"