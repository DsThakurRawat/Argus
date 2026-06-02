# Copyright 2026 Divyansh Rawat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# argus/ingestion/adapters/__init__.py

"""
Log source adapters for the ingestion system.

This module provides adapters for different log sources including:
- Google Cloud Pub/Sub
- Google Cloud Logging
- File System
- AWS CloudWatch
- Kubernetes
- Syslog
"""

from .aws_cloudwatch import AWSCloudWatchAdapter
from .file_system import FileSystemAdapter
from .file_system_queued import QueuedFileSystemAdapter
from .gcp_logging import GCPLoggingAdapter
from .gcp_pubsub import GCPPubSubAdapter
from .kubernetes import KubernetesAdapter

__all__ = [
    "AWSCloudWatchAdapter",
    "FileSystemAdapter",
    "GCPLoggingAdapter",
    "GCPPubSubAdapter",
    "KubernetesAdapter",
    "QueuedFileSystemAdapter",
]
