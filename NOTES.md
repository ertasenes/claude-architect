# Claude Architect — Learning Notes

Learning journal for building an agentic AI system with the Anthropic API,
on the path to the Anthropic Certified Architect certification.
Starting point: zero Python experience.

## Project Goal
Build a working multi-tool AI agent from scratch while learning Python and
agentic architecture in parallel. Every step is written by hand (not copied)
to build durable understanding. Progress is tracked via commits in this repo.

## How the Agent Loop Works
- `messages` is a list that acts as the agent's memory. Claude has no memory
  of its own — we re-send the full conversation history on every turn.
- Claude decides which tool to use based on each tool's `description`.
- When Claude responds, `stop_reason` tells us why it stopped:
  - `"end_turn"` → Claude is done and gave its final answer.
  - `"tool_use"` → Claude is waiting for us to run a tool.
- When `stop_reason == "tool_use"`, we:
  1. Add Claude's tool request to `messages`.
  2. Run the requested tool ourselves.
  3. Add the result back to `messages` as a `tool_result`.
  4. Call Claude again with the updated `messages`.
- The whole thing runs inside a `while True` loop that only breaks when
  `stop_reason == "end_turn"`.

## File Structure (Separation of Concerns)
- `tools.py` → all tool functions (`calculate`, `get_current_time`,
  `get_weather`) and their tool schemas. Functions and their schemas live
  together because they change together.
- `agent.py` → the agent loop, the Claude API calls, and the tool dispatch.
- Reason for splitting: tools and the loop change for different reasons.
  Keeping them separate means editing one doesn't disturb the other.

## Import Rules
- `import tools` in `agent.py` gives access via the `tools.` prefix
  (e.g. `tools.get_weather`). Chosen for readability while learning.
- Each file is responsible for its own imports. An import in one file does
  not "leak" into another. `tools.py` needs its own
  `from datetime import datetime`.
- Circular import: if `agent.py` imports `tools` and `tools.py` imports
  `agent`, they call each other endlessly and Python breaks. Always import
  from the original source, not from another file that happens to have it.

## Tool Registry Pattern
Instead of a long `if/elif` chain to pick which tool to run, use a dictionary
that maps tool names (strings) to functions:

    tool_functions = {
        "calculate": tools.calculate,
        "get_current_time": tools.get_current_time,
        "get_weather": tools.get_weather
    }

Then dispatch in a single line:

    result = tool_functions[tool_name](**block.input)

- Functions are stored WITHOUT parentheses — the function itself, not its
  result. In Python, functions are values (first-class functions).
- `**block.input` unpacks the argument dictionary Claude sends into the
  function's arguments. Works for any tool, including ones with no arguments
  (empty dict → no arguments).
- Adding a new tool no longer touches the loop — just add the function and
  one registry entry. This is data-driven design.

## Errors I Solved
- `ModuleNotFoundError: No module named 'dotenv'` → virtual environment was
  not activated. Fixed with `source venv/bin/activate`.
- `name 'tool_functions' is not defined` → the registry dictionary must be
  defined before the loop, not inside it. Python reads top to bottom.
- `name 'tool_name' is not defined` → the tool name comes from `block.name`.
  Assigned it with `tool_name = block.name` before using it.

## Key Principles Learned
- Separation of concerns: each file has one job.
- DRY (Don't Repeat Yourself): define once, use everywhere.
- Read the error message — most errors name exactly what's missing.
- Code is written to be read, not just to run.