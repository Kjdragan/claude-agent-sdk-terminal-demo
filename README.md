# Claude Terminal Agent — a minimal Agent SDK demo

A ~90-line Python program that gives you a Claude agent in your terminal. Ask it
a question, give it a task, and it keeps looping — ready for the next prompt —
until you quit. It's the smallest useful thing you can build with the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), meant as
a first look for someone who has never used the SDK before.

```
You: what files are in this folder?
  [using Bash]
Claude: There are 5 files: main.py, requirements.txt, README.md, .env.example, and .gitignore.

You: create notes.txt with three ideas for a weekend project
  [using Write]
Claude: Done — I wrote notes.txt with three project ideas.

You: exit
```

## What is the Agent SDK?

The same engine that powers Claude Code, available as a library. You hand Claude
a prompt; it can **read files, write files, run shell commands, and search the
web on its own** to carry out the request, then report back. You don't write a
tool-calling loop — the SDK runs the agent loop for you.

This demo shows the two ideas that make it an *agent* and not just a chatbot:

- **One persistent conversation.** `ClaudeSDKClient` keeps the session alive, so
  Claude remembers earlier turns. Ask a follow-up — "now do the same for the
  other file" — and it knows what you mean.
- **An allow-list of tools.** `allowed_tools` lists the built-in tools Claude may
  use *without stopping to ask you*. That's what lets it actually do things on
  your machine instead of only talking about them.

The whole thing is in [`main.py`](./main.py) — read it, it's short.

## Requirements

- **Python 3.10+**
- **A Claude Pro or Max subscription** — this demo runs on your subscription, no
  API key or per-token billing.
- **The Claude Code CLI**, used once to mint a login token. If you already use
  Claude Code you have it. If not:
  ```bash
  curl -fsSL https://claude.ai/install.sh | bash      # or: npm install -g @anthropic-ai/claude-code
  ```

## Setup

```bash
# 1. Clone and enter the project
git clone https://github.com/Kjdragan/claude-agent-sdk-terminal-demo.git
cd claude-agent-sdk-terminal-demo

# 2. Create a simple virtual environment and install the one dependency
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Get a subscription token and put it in .env
claude setup-token                 # prints a token (logs you in via browser)
cp .env.example .env               # then paste the token into .env
```

Open `.env` and set:

```
CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat...your-token...
```

> If `ANTHROPIC_API_KEY` is set in your shell, it takes precedence over the
> subscription token. Run `unset ANTHROPIC_API_KEY` to use your subscription.

## Run

```bash
python main.py
```

Type a question or a task, press Enter, and Claude responds. The `[using Bash]`
lines show it reaching for a tool. Type `exit` (or Ctrl-D) to quit.

## Don't want to type the commands? Let Claude do it

You don't have to run any of the setup by hand. Open the **Claude desktop app**
(Mac or Windows), go to the **Code tab**, point it at a folder, and paste one of
the prompts below. The Code tab *is* Claude Code — the same agent this demo is
built on — so it will run the commands for you.

**Install and run this project from GitHub** — paste into an empty folder:

```
Clone https://github.com/Kjdragan/claude-agent-sdk-terminal-demo into this
folder. Create a Python virtual environment, install requirements.txt into it,
then walk me through running `claude setup-token` and pasting the token into a
new .env file. When that's done, run `python main.py` so I can try it.
```

**Just provision the environment** — if you already have the files and only need
the venv set up:

```
Set up this project for me: create a Python virtual environment in .venv,
install everything in requirements.txt, and create a .env file from
.env.example. Tell me exactly what to paste into .env to finish.
```

**Build the whole thing from scratch** — the best way to see how little code this
takes. Paste this into an empty folder and watch Claude write it:

```
Build a minimal terminal app in Python using the Claude Agent SDK
(`claude-agent-sdk`). It should be a loop that reads a line from stdin, sends it
to Claude, prints the reply, and waits for the next prompt until I type "exit".
Use ClaudeSDKClient so the conversation keeps its memory across turns, and
pre-approve the Read, Write, Edit, Bash, Glob, Grep, WebSearch, and WebFetch
tools so it can actually do tasks without asking permission each time.
Authenticate with my Claude subscription via a CLAUDE_CODE_OAUTH_TOKEN read from
a .env file (load the .env yourself with a few lines of standard library — no
extra dependency). Add a requirements.txt, a .env.example, a .gitignore that
excludes .env and .venv, and a short README. Then set up the virtual
environment, install it, and help me get my token so I can run it.
```

## A note on what it's allowed to do

The agent is pre-approved to use `Read`, `Write`, `Edit`, `Bash`, `Glob`,
`Grep`, `WebSearch`, and `WebFetch` — meaning it can run shell commands and
change files in the folder you launch it from, without asking first. That's what
makes the demo able to *do tasks*. Run it somewhere you're comfortable with that,
and trim the `ALLOWED_TOOLS` list in `main.py` if you want it more restricted
(e.g. drop `Bash` and `Write` for a read-only, answer-only assistant).

## Where to go next

- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python)
- Try changing the `system_prompt` in `main.py`, or add a custom tool via MCP.
