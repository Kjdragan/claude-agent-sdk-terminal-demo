# Claude Terminal Agent — a minimal Agent SDK demo

A small (~150-line) Python program that gives you a Claude agent in your terminal. Ask it
a question, give it a task, and it keeps looping — ready for the next prompt —
until you quit. It's the smallest useful thing you can build with the
[Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), meant as
a first look for someone who has never used the SDK before.

```
You: what files are in this folder?
  [using Bash]
Claude: main.py, requirements.txt, README.md, SAMPLE_RUN.md, .env.example, and .gitignore.

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

## You could build this from a single prompt

You don't actually *need* this repo. Everything in it — the app, the `.env`
setup, the requirements file — was produced by one plain-English prompt to a
fresh [Claude Code](https://claude.com/claude-code) session (the **Code tab** in
the Claude desktop app, or the `claude` command in a terminal). If you'd rather
build your own from nothing than clone this, paste this and let Claude do it:

```
Build a tiny Python terminal app using the Claude Agent SDK (the
`claude-agent-sdk` pip package). It should loop: I type a question or a task,
Claude answers and can use its built-in tools (read/write files, run shell
commands, search the web) to actually do it, then it waits for my next message
until I type "exit". Authenticate with my Claude Pro/Max subscription using a
CLAUDE_CODE_OAUTH_TOKEN read from a .env file. Keep it dead simple: one
dependency, a requirements.txt, and a .env.example. Then create the virtual
environment, install it, tell me to run `claude setup-token` to get my token,
and show me how to start it.
```

Want it published like this one? Add a sentence: *"Then make it a git repo and
publish it as a new public GitHub repository."* Everything past this point
assumes you cloned the repo, which is the quickest way to get going.

## Requirements

- **Python 3.10+** — check with `python3 --version`.
- **A paid Claude plan — the free tier will not work.** You need at least
  **Claude Pro** (the entry paid plan, ~$20/month); **Max** works too. The login
  step below (`claude setup-token`) only succeeds on a paid subscription. The
  demo then runs entirely on that subscription — no separate API key, no
  per-token billing.
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

**Build the whole thing from scratch instead?** You don't need to clone anything
— see [You could build this from a single prompt](#you-could-build-this-from-a-single-prompt)
near the top for the one-prompt version.

## Is this safe to run?

Short version: yes, for a tool you run on your own machine — but understand what
you're handing it.

- **It acts as you, in the folder you start it from.** Because `Bash`, `Write`,
  and `Edit` are pre-approved, the agent can run shell commands and create or
  change files in that folder *without asking first*. That's exactly what lets it
  do real tasks. Start it in a project or scratch folder — not your home or a
  system directory — and only ask it to do things you'd be comfortable doing
  yourself. Want an answer-only assistant? Remove `Bash`, `Write`, and `Edit`
  from the `ALLOWED_TOOLS` list in [`main.py`](./main.py).
- **Your token is a password.** `claude setup-token` mints a token tied to your
  subscription. The demo saves it to `.env`, which is already in `.gitignore`, so
  it is never committed or pushed. Don't paste it anywhere public or share it.
- **Only paste prompts and links you trust.** An agent does what it's told —
  including instructions that might be hidden inside a web page or file you point
  it at. Treat it like your own hands on the keyboard.

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
