"""A tiny terminal agent built on the Claude Agent SDK.

It loops forever: you type a question or a task, Claude answers (and can read
files, write files, run shell commands, and search the web to get it done),
then it waits for your next prompt. Type "exit" or press Ctrl-D to quit.

This is the smallest useful thing you can build with the Agent SDK, meant as a
first look for someone who has never used it before. Two ideas to take away:

  1. ClaudeSDKClient keeps one conversation alive, so Claude remembers earlier
     turns (ask a follow-up like "now do the same for the other file").
  2. allowed_tools is an allow-list of built-in tools Claude may use without
     stopping to ask you. That is what turns a chatbot into an agent that
     actually does things on your machine.
"""

import asyncio
import os
import shutil
import subprocess
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    PermissionResultAllow,
    PermissionResultDeny,
    TextBlock,
    ToolUseBlock,
)


def load_env(path: str = ".env") -> None:
    """Load KEY=value lines from a .env file into os.environ.

    The SDK reads its auth token from the environment, but nothing loads .env
    for you. This is the whole loader -- no python-dotenv dependency needed.
    """
    env_file = Path(path)
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def save_token(token: str, path: str = ".env") -> None:
    """Write the token into .env, replacing any existing token line."""
    env_file = Path(path)
    lines = env_file.read_text().splitlines() if env_file.exists() else []
    out, replaced = [], False
    for line in lines:
        if line.strip().startswith("CLAUDE_CODE_OAUTH_TOKEN="):
            out.append(f"CLAUDE_CODE_OAUTH_TOKEN={token}")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"CLAUDE_CODE_OAUTH_TOKEN={token}")
    env_file.write_text("\n".join(out) + "\n")


def onboard() -> bool:
    """First-run flow: authorize the user's Claude subscription and save a token.

    Runs automatically the first time the demo starts (when no token is set).
    Returns True if a token was saved and the demo can continue.
    """
    print("Welcome! This demo runs on your Claude Pro/Max subscription.")
    print("First we'll authorize it — this happens once, then it's saved to .env.\n")

    if shutil.which("claude") is None:
        print("You need the Claude Code CLI to authorize. Install it with:")
        print("  curl -fsSL https://claude.ai/install.sh | bash")
        print("  (or: npm install -g @anthropic-ai/claude-code)")
        print("Then run this demo again.")
        return False

    input("Press Enter to open the login flow in your browser... ")
    # Hand the terminal to the CLI so you can complete the browser login. When
    # it finishes it prints a token (starts with sk-ant-oat...).
    subprocess.run(["claude", "setup-token"])

    token = input("\nPaste the token it printed here: ").strip()
    if not token:
        print("No token entered — run the demo again when you're ready.")
        return False

    save_token(token)
    os.environ["CLAUDE_CODE_OAUTH_TOKEN"] = token
    print("\nSaved to .env. You're authorized — starting the agent.\n")
    return True


# The agent's writes are fenced to this project directory. It can create and
# edit any file in here -- including this main.py, which is how it can build and
# fix its own code -- but it is refused writes anywhere outside the project, so
# it can't scatter files across your home or system folders. Reads, web search,
# and shell stay unrestricted so it can still do real work.
PROJECT_DIR = Path(__file__).resolve().parent

# Pre-approved tools run without a permission check. The file-writing tools are
# deliberately left off this list so every write is routed through can_use_tool()
# below for the project-directory check.
ALLOWED_TOOLS = ["Read", "Glob", "Grep", "Bash", "WebSearch", "WebFetch"]
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}


async def can_use_tool(tool_name, tool_input, context):
    """Permission hook: allow everything, except writes outside the project dir."""
    if tool_name in WRITE_TOOLS:
        path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        target = Path(path)
        target = target.resolve() if target.is_absolute() else (PROJECT_DIR / target).resolve()
        if target != PROJECT_DIR and PROJECT_DIR not in target.parents:
            return PermissionResultDeny(
                message=(
                    "Writing outside the project directory is blocked. Write inside "
                    f"{PROJECT_DIR} instead (a relative path stays in the project)."
                )
            )
    return PermissionResultAllow()


OPTIONS = ClaudeAgentOptions(
    system_prompt=(
        "You are a helpful assistant running in a terminal. Answer questions "
        "directly and concisely. When asked to do a task, use your tools to "
        "actually do it, then briefly say what you did. Save any files you create "
        "inside the current project directory."
    ),
    allowed_tools=ALLOWED_TOOLS,
    can_use_tool=can_use_tool,
    cwd=str(PROJECT_DIR),
    # "default" routes any tool that isn't pre-approved (Write/Edit) through
    # can_use_tool above instead of auto-accepting it -- no interactive hang,
    # because the callback decides instantly.
    permission_mode="default",
)


async def main() -> None:
    load_env()
    if not os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") and not os.environ.get("ANTHROPIC_API_KEY"):
        if not onboard():
            return

    print("Claude terminal agent. Ask a question or give it a task.")
    print('Type "exit" or press Ctrl-D to quit.\n')

    async with ClaudeSDKClient(options=OPTIONS) as client:
        while True:
            try:
                prompt = input("You: ").strip()
            except EOFError:        # Ctrl-D
                print()
                break
            if not prompt:
                continue
            if prompt.lower() in ("exit", "quit"):
                break

            await client.query(prompt)
            # Iterate to completion -- don't `break` out of this loop early, it
            # confuses asyncio cleanup (documented SDK gotcha).
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Claude: {block.text}")
                        elif isinstance(block, ToolUseBlock):
                            print(f"  [using {block.name}]")
            print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:        # Ctrl-C
        print("\nBye.")
