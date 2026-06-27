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
```

That's the whole setup. **You don't need to create `.env` yourself** — the first
time you run the demo it onboards you (see below).

> If `ANTHROPIC_API_KEY` is set in your shell, it takes precedence over the
> subscription token. Run `unset ANTHROPIC_API_KEY` to use your subscription.

## First run: subscription onboarding

The very first time you start the demo with no token saved, it walks you through
authorizing your Claude subscription — automatically:

```
$ python main.py
Welcome! This demo runs on your Claude Pro/Max subscription.
First we'll authorize it — this happens once, then it's saved to .env.

Press Enter to open the login flow in your browser...
   ... (you approve access in the browser, the CLI prints a token) ...
Paste the token it printed here: sk-ant-oat...

Saved to .env. You're authorized — starting the agent.
```

It runs `claude setup-token` for you, saves the result to `.env`, and drops
straight into the chat. Every run after that finds the token in `.env` and skips
onboarding. (Prefer to do it by hand? Run `claude setup-token`, then
`cp .env.example .env` and paste the token in.)

**See [`SAMPLE_RUN.md`](./SAMPLE_RUN.md)** for a full example session — the
onboarding above, followed by the agent answering questions, searching the web,
and writing and running a small program.

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

## Next steps: have the agent upgrade itself

Here's the fun part. Because the agent runs in this folder with the `Write`,
`Edit`, and `Bash` tools, it can **edit its own `main.py`**. So you grow the app
by *talking to it* — paste one of the prompts below at the `You:` prompt, let it
make the change, then **exit and rerun `python main.py`** so the new code loads.
(Some upgrades add a dependency or need Node installed — that's expected once you
go past the bare-bones base.)

Each prompt below teaches one real Agent SDK extension point.

**1. Teach it a Skill (research → written report).** A
[Skill](https://code.claude.com/docs/en/agent-sdk/skills) is a reusable
capability Claude invokes on its own.

```
Create a Claude Skill at .claude/skills/report-writer/SKILL.md. When I ask for a
report on a topic, it should research the topic with WebSearch and write a clean
Markdown report — title, summary, sections, and a Sources list — into a reports/
folder. Then update main.py so the SDK loads skills: set
setting_sources=["project"] and skills="all" in ClaudeAgentOptions. Tell me to
restart you when it's done.
```

**2. Give it a brand-new tool (YouTube transcripts).** This is the
[custom-tool](https://code.claude.com/docs/en/agent-sdk/custom-tools) pattern: a
Python function Claude can call.

```
Add a custom tool get_youtube_transcript(url) that returns a video's transcript
using the youtube-transcript-api package (add it to requirements.txt and install
it). Define it with the SDK's @tool decorator, bundle it with
create_sdk_mcp_server, register it under mcp_servers in ClaudeAgentOptions, and
pre-approve it by adding "mcp__<server>__get_youtube_transcript" to allowed_tools.
After I restart you, I'll paste a YouTube link and ask you to summarize it.
```

**3. Plug in an external MCP server (browser automation).** Reuse tools other
people built via [MCP](https://code.claude.com/docs/en/agent-sdk/mcp).

```
Give yourself browser automation by connecting the Playwright MCP server. In
ClaudeAgentOptions, add mcp_servers={"playwright": {"command": "npx", "args":
["@playwright/mcp@latest"]}} and pre-approve its tools with "mcp__playwright__*"
in allowed_tools. Then I can ask you to open a page, click around, and screenshot
it. (Needs Node/npx installed.)
```

**4. Give it memory between runs.** Mixes a custom tool with a custom
`system_prompt`.

```
Give yourself long-term memory. At startup, if memory.md exists, load its
contents into your system_prompt. Add a custom tool remember(fact) that appends a
bullet to memory.md, and pre-approve it. After I restart you, you should recall
anything I asked you to remember.
```

**5. Delegate to a [subagent](https://code.claude.com/docs/en/agent-sdk/subagents)
(deep research).**

```
Add a "researcher" subagent using the agents option (AgentDefinition) with its
own prompt and the Read, Glob, Grep, WebSearch, and WebFetch tools, and add
"Agent" to allowed_tools so you can call it. When I ask for deep research,
delegate to the researcher and summarize what it finds.
```

Mix and match — once it has the YouTube tool *and* the report Skill, "summarize
this video and write it up as a report" chains both. When something doesn't work,
just tell the agent the error and ask it to fix itself.

## Learn more

- [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Python SDK reference](https://code.claude.com/docs/en/agent-sdk/python)
- [Custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools) ·
  [Skills](https://code.claude.com/docs/en/agent-sdk/skills) ·
  [MCP](https://code.claude.com/docs/en/agent-sdk/mcp) ·
  [Subagents](https://code.claude.com/docs/en/agent-sdk/subagents)
