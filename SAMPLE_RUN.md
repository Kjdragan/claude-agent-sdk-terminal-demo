# Sample run

A real session, lightly edited (token, paths, and the login banner redacted).
It shows the one-time **subscription onboarding** on first launch, then the
agent answering questions and doing tasks — web searches and writing/running
code — all from the terminal.

```text
$ cd claude-agent-sdk-terminal-demo
$ source .venv/bin/activate
$ python main.py
Welcome! This demo runs on your Claude Pro/Max subscription.
First we'll authorize it — this happens once, then it's saved to .env.

Press Enter to open the login flow in your browser...
Welcome to Claude Code v2.1.195
[ a browser window opens — you approve access ]

 ✓ Long-lived authentication token created successfully!

 Your OAuth token (valid for 1 year):

 sk-ant-oat01-XXXXXXXXXXXX…REDACTED…XXXXXXXXXXXX

 Store this token securely. You won't be able to see it again.

 Use this token by setting: export CLAUDE_CODE_OAUTH_TOKEN=<token>


Paste the token it printed here:  sk-ant-oat01-XXXXXXXXXXXX…REDACTED…XXXXXXXXXXXX

Saved to .env. You're authorized — starting the agent.

Claude terminal agent. Ask a question or give it a task.
Type "exit" or press Ctrl-D to quit.

You: hello
Claude: Hello! What can I help you with today?

You: do something for me
Claude: What do you need? Give me a task — a bug to fix, code to write, something
to look up, a repo to work in — and I'll do it.

You: what is the weather in houston
  [using WebSearch]
Claude: Houston right now: partly cloudy, 82°F (feels like ~92°F — hot and humid,
80% humidity). Today's high ~92°F, low ~78°F.

You: anything fun to do today in houston
  [using WebSearch]
Claude: Plenty going on this Saturday — and since it's hot/humid (~92°F feel),
I'd lean toward indoor or evening options:

- Comedy — Craig Robinson at Houston Improv (multiple shows)
- Theater — Misery at Alley Theatre; Tamarie's Greatest Hits Vol. 3 at MATCH
- Baseball — Sugar Land Space Cowboys vs. El Paso Chihuahuas at Constellation Field
- Soccer watch party — free screenings at Shell Energy Stadium (RSVP), kid-friendly
- Morning, before the heat — Saturdays Yoga at Discovery Green (9–10 a.m.)

Want me to dig into any one of these — showtimes, tickets, or a full day plan?

You: write me a tic tac toe game
  [using Write]
  [using Bash]
Claude: ~/tic_tac_toe.py → 2-player hotseat, win/draw detection, self-check
passes. Verified: X took the top row and won.

skipped: computer opponent. Add when you want single-player — say so and I'll
bolt on a minimax AI (it's ~15 lines and unbeatable).

You: yes please
  [using Edit]
  [using Bash]
Claude: Done. Added a minimax AI to ~/tic_tac_toe.py — it plays perfectly.

- python3 tic_tac_toe.py        → you (X) vs computer (O)
- python3 tic_tac_toe.py --2p   → two-player hotseat

Self-checks now also verify the AI takes a win and blocks a loss. It's
unbeatable — best you'll get is a draw.

You: exit
```
