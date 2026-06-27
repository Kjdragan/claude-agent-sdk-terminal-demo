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
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
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


# Tools Claude is pre-approved to use. Because they are listed here, Claude runs
# them without pausing to ask permission -- otherwise a terminal demo would hang
# waiting for an approval it can't show. Bash means Claude can run any shell
# command in this folder, so keep this list to what you're comfortable with.
ALLOWED_TOOLS = [
    "Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebSearch", "WebFetch",
]

OPTIONS = ClaudeAgentOptions(
    system_prompt=(
        "You are a helpful assistant running in a terminal. Answer questions "
        "directly and concisely. When asked to do a task, use your tools to "
        "actually do it, then briefly say what you did."
    ),
    allowed_tools=ALLOWED_TOOLS,
    # acceptEdits auto-confirms file edits. Combined with the allow-list above,
    # the agent runs end to end without interactive prompts.
    permission_mode="acceptEdits",
)


async def main() -> None:
    load_env()
    if not os.environ.get("CLAUDE_CODE_OAUTH_TOKEN") and not os.environ.get("ANTHROPIC_API_KEY"):
        print("No credentials found. Copy .env.example to .env and add your")
        print("CLAUDE_CODE_OAUTH_TOKEN (run `claude setup-token` to get one).")
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
