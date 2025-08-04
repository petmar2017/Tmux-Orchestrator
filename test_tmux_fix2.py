#!/usr/bin/env python3
"""Test script for tmux send-keys fix - version 2"""

import subprocess
import time

def test_tmux_send():
    # Test the fixed send-keys approach
    session = 'test_session'
    window = 0

    # Kill any existing test session
    subprocess.run(['tmux', 'kill-session', '-t', session], 
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Create a test session  
    subprocess.run(['tmux', 'new-session', '-d', '-s', session, '-n', 'test'])

    # Test sending multi-line content with special characters
    test_content = """## PROJECT SPECIFIC CONTEXT

Project: my-api
Description: Test API with special chars
API Type: REST API with -flags and --options
Features: User Management, Rate Limiting
MCP Tools: Database Query, API Testing

## YOUR IMMEDIATE TASKS

- Build REST API
- Use PostgreSQL for data persistence  
- Implement JWT authentication
"""

    lines = test_content.split('\n')
    
    print('Testing improved tmux send-keys...\n')

    # Send each line using the fixed approach
    for i, line in enumerate(lines):
        # Build command as single list
        cmd = ["tmux", "send-keys", "-t", f"{session}:{window}", "-l", line]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f'❌ Error on line {i+1}: {result.stderr}')
            print(f'   Command was: {cmd}')
            return False
        else:
            print(f'✅ Line {i+1} sent')
        
        # Send newline except for last line
        if i < len(lines) - 1:
            cmd_newline = ["tmux", "send-keys", "-t", f"{session}:{window}", "C-m"]
            subprocess.run(cmd_newline)

    # Send final Enter
    subprocess.run(['tmux', 'send-keys', '-t', f'{session}:{window}', 'Enter'])

    time.sleep(0.5)

    # Capture and display what was sent
    result = subprocess.run(['tmux', 'capture-pane', '-t', f'{session}:{window}', '-p'], 
                           capture_output=True, text=True)

    print('\n📋 Content sent to tmux:')
    print('=' * 50)
    print(result.stdout)
    print('=' * 50)

    # Clean up
    subprocess.run(['tmux', 'kill-session', '-t', session])
    print('\n✅ Test completed successfully!')
    return True

if __name__ == "__main__":
    test_tmux_send()