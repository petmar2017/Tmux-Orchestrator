#!/usr/bin/env python3
"""Test script for tmux send-keys fix"""

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
    test_lines = [
        'Line 1 with normal text',
        'Line 2 with -flags and --options',
        'Line 3 with "quotes" and special chars',
        "Line 4 with 'single quotes'",
        'Line 5 with $variables and #symbols',
        '## MARKDOWN HEADER',
        '- Bullet point with dash',
        ''  # Empty line
    ]

    print('Testing tmux send-keys with multiple lines...\n')

    # Send each line using the fixed approach
    for i, line in enumerate(test_lines):
        # Escape single quotes
        escaped_line = line.replace("'", "'\\''")
        
        # Send the line wrapped in single quotes
        if escaped_line or i == 0:  # Send non-empty lines or preserve first empty line
            result = subprocess.run(['tmux', 'send-keys', '-t', f'{session}:{window}', 
                                   f"'{escaped_line}'"], 
                                   capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f'❌ Error on line {i+1}: {result.stderr}')
                return False
            else:
                print(f'✅ Line {i+1} sent successfully')
        
        # Send newline except for last line
        if i < len(test_lines) - 1:
            subprocess.run(['tmux', 'send-keys', '-t', f'{session}:{window}', 'C-m'])

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