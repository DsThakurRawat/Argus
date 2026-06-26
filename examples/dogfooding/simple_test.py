#!/usr/bin/env python3

#

"""
Simple test to verify log processing without complex agent pipeline.
"""

import asyncio
from pathlib import Path
import sys
import time

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from argus.ingestion.adapters.file_system import FileSystemAdapter  # noqa: E402 - needs sys.path
from argus.ingestion.manager.log_manager import LogManager  # noqa: E402 - needs sys.path


async def simple_log_processor(log_entry):
    """Simple log processor that just prints the log entry."""
    print(f"📝 Processing log entry: {log_entry.id}")
    print(f"   Message: {log_entry.message}")
    print(f"   Severity: {log_entry.severity}")
    print(f"   Timestamp: {log_entry.timestamp}")
    print(f"   Source: {log_entry.source}")
    print("---")


async def main():
    """Test basic log processing without agents."""
    print("🧪 Simple Log Processing Test")
    print("=" * 50)

    # Clean up first
    log_dir = Path("/tmp/sre-dogfooding")
    if log_dir.exists():
        for file in log_dir.glob("*.log"):
            file.unlink()

    # Start the dogfood service
    print("🚀 Starting dogfood service...")
    import subprocess

    dogfood_process = subprocess.Popen(
        ["python", "dogfood_service/app.py"], cwd=Path(__file__).parent
    )

    # Wait for service to start
    time.sleep(3)

    # Create a simple log manager
    log_manager = LogManager(simple_log_processor)

    # Create a file system adapter
    from argus.config.ingestion_config import FileSystemConfig, SourceType

    config = FileSystemConfig(
        name="test_logs",
        type=SourceType.FILE_SYSTEM,
        file_path="/tmp/sre-dogfooding/agent_1.log",
        file_pattern="*.log",
        watch_mode=True,
        encoding="utf-8",
        buffer_size=1000,
        max_memory_mb=100,
    )

    adapter = FileSystemAdapter(config)
    await log_manager.add_source(adapter)

    # Start the log manager
    print("📊 Starting log manager...")
    await log_manager.start()

    # Check if file exists and has content
    log_file = Path("/tmp/sre-dogfooding/agent_1.log")
    if log_file.exists():
        print(f"📄 Log file exists, size: {log_file.stat().st_size} bytes")
        print(f"📄 First 200 chars: {log_file.read_text()[:200]}")
    else:
        print("❌ Log file does not exist")

    # Trigger some errors to generate logs
    print("🔥 Triggering errors...")
    import requests

    try:
        requests.get("http://127.0.0.1:5001/error/division", timeout=5)
        requests.get("http://127.0.0.1:5001/error/memory", timeout=5)
        requests.get("http://127.0.0.1:5001/error/connection", timeout=5)
        print("✅ Errors triggered")
    except Exception as e:
        print(f"⚠️  Error triggering requests: {e}")

    # Wait for some logs to be generated
    print("⏳ Waiting for logs...")
    await asyncio.sleep(10)  # Wait longer for logs to be processed

    # Check if tasks are running
    print(f"📊 LogManager tasks: {log_manager.tasks}")
    for i, task in enumerate(log_manager.tasks):
        print(f"   Task {i}: {task.done()}")
        if task.done():
            try:
                result = task.result()
                print(f"   Task {i} result: {result}")
            except Exception as e:
                print(f"   Task {i} exception: {e}")

    # Stop the log manager
    print("🛑 Stopping log manager...")
    await log_manager.stop()

    # Clean up
    dogfood_process.terminate()
    dogfood_process.wait()

    print("✅ Test completed!")


if __name__ == "__main__":
    asyncio.run(main())
