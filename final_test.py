#!/usr/bin/env python3
"""Final test of tmux fix"""

import subprocess
import time

session = 'final_test'
window = 0

# Kill any existing test session
subprocess.run(['tmux', 'kill-session', '-t', session], stderr=subprocess.DEVNULL)

# Create test session
subprocess.run(['tmux', 'new-session', '-d', '-s', session])

test_content = """## PROJECT CONTEXT
- Build REST API with --options
- Use PostgreSQL for data
- Implement JWT auth
Features: Rate Limiting, Caching

## TASKS
1. Create API endpoints
2. Add authentication
- Test everything"""

lines = test_content.split('\n')
print(f'Sending {len(lines)} lines to tmux...')

for i, line in enumerate(lines):
    if line.startswith('-'):
        cmd = ['tmux', 'send-keys', '-t', f'{session}:{window}', '--', line]
    else:
        cmd = ['tmux', 'send-keys', '-t', f'{session}:{window}', '-l', line]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f'❌ Error on line {i+1}: {result.stderr}')
    
    if i < len(lines) - 1:
        subprocess.run(['tmux', 'send-keys', '-t', f'{session}:{window}', 'C-m'])

subprocess.run(['tmux', 'send-keys', '-t', f'{session}:{window}', 'Enter'])
time.sleep(0.5)

# Capture result
result = subprocess.run(['tmux', 'capture-pane', '-t', f'{session}:{window}', '-p'], 
                       capture_output=True, text=True)
print('\n✅ Successfully sent all lines!')
print('\nContent in tmux:')
print('=' * 40)
print(result.stdout)
print('=' * 40)

# Cleanup
subprocess.run(['tmux', 'kill-session', '-t', session])
print('\n✅ Test completed!')