#!/usr/bin/env python3
"""
Optimized API Builder Launcher - Faster agent initialization
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class FastAPIBuilderLauncher:
    """Optimized launcher with faster Claude initialization"""
    
    def __init__(self):
        self.session_name = "api_builder"
        self.base_dir = Path(__file__).parent
        self.workspace_dir = self.base_dir / "workspace"
        self.prompts_dir = self.base_dir / "prompts"
        self.project_config = {}
        
        # Colors for terminal output
        self.GREEN = '\033[0;32m'
        self.YELLOW = '\033[1;33m'
        self.CYAN = '\033[0;36m'
        self.RED = '\033[0;31m'
        self.MAGENTA = '\033[0;35m'
        self.NC = '\033[0m'  # No Color
        
    def launch_claude_in_window_fast(self, window_num: int, agent_name: str, prompt_content: str):
        """Optimized Claude launch - much faster"""
        
        print(f"  🚀 Starting {agent_name}...", end="", flush=True)
        
        # Step 1: Setup directory and start Claude (combined)
        setup_commands = [
            f"cd {self.workspace_dir}",
            "clear",
            "claude"
        ]
        
        for cmd in setup_commands:
            subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                           cmd, "Enter"])
            time.sleep(0.3)  # Reduced wait time
        
        print(f" initializing...", end="", flush=True)
        time.sleep(1.5)  # Reduced Claude startup wait
        
        # Step 2: Send entire prompt at once (much faster!)
        print(f" briefing...", end="", flush=True)
        
        # Send the entire prompt as one block
        # This is MUCH faster than chunking
        escaped_prompt = prompt_content.replace("'", "'\\''")
        
        # Use printf to handle multi-line content properly
        tmux_cmd = [
            "tmux", "send-keys", "-t", f"{self.session_name}:{window_num}",
            f"printf '%s\\n' '{escaped_prompt}'", "Enter"
        ]
        
        try:
            subprocess.run(tmux_cmd, capture_output=True, text=True)
            time.sleep(0.5)  # Small wait for prompt to register
            
            # Send Enter to submit the prompt
            subprocess.run(["tmux", "send-keys", "-t", f"{self.session_name}:{window_num}", 
                           "Enter"])
            
        except Exception as e:
            print(f" {self.RED}Error: {e}{self.NC}")
            # Fallback to chunked sending if needed
            self.send_prompt_chunked(window_num, prompt_content)
            
        print(f" {self.GREEN}✅ Ready!{self.NC}")
        
    def send_prompt_chunked(self, window_num: int, prompt_content: str):
        """Fallback chunked sending if fast method fails"""
        lines = prompt_content.split('\n')
        chunk_size = 50  # Larger chunks for faster sending
        
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            if chunk.strip():
                subprocess.run(["tmux", "send-keys", "-t", 
                              f"{self.session_name}:{window_num}", 
                              chunk])
                time.sleep(0.2)  # Minimal wait between chunks
        
        subprocess.run(["tmux", "send-keys", "-t", 
                       f"{self.session_name}:{window_num}", "Enter"])
                       
    def launch_claude_in_window_parallel(self, agents_to_launch):
        """Launch multiple agents in parallel for even faster startup"""
        import concurrent.futures
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for window_num, prompt_file, agent_name, prompt_content in agents_to_launch:
                future = executor.submit(
                    self.launch_claude_in_window_fast, 
                    window_num, agent_name, prompt_content
                )
                futures.append(future)
                time.sleep(0.5)  # Small stagger to avoid overwhelming tmux
            
            # Wait for all to complete
            concurrent.futures.wait(futures)
            
    def create_fast_send_script(self):
        """Create an optimized send script that doesn't use sleep"""
        fast_script = self.base_dir.parent / "send-claude-message-fast.sh"
        
        script_content = '''#!/bin/bash
# Fast message sender - no sleep delays
WINDOW="$1"
shift
MESSAGE="$*"

# Send message and Enter in one go
tmux send-keys -t "$WINDOW" "$MESSAGE" Enter

echo "Message sent to $WINDOW"
'''
        
        with open(fast_script, 'w') as f:
            f.write(script_content)
        
        os.chmod(str(fast_script), 0o755)
        return fast_script

# Usage example showing the improvements:
if __name__ == "__main__":
    print("This is an optimized launcher with:")
    print("  • Faster Claude initialization (1.5s vs 2s)")
    print("  • Single-block prompt sending (no chunking)")
    print("  • Reduced sleep times (0.3s vs 0.5-1s)")
    print("  • Optional parallel agent launching")
    print("")
    print("Expected time savings:")
    print("  Old method: ~20-25 seconds per agent")
    print("  New method: ~3-5 seconds per agent")
    print("  Total savings: ~2-3 minutes for 8 agents!")