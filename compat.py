"""Workaround for a known CrewAI bug with Groq.

CrewAI adds a `cache_breakpoint` flag to messages (meant for Anthropic prompt
caching). Groq rejects it with:
    property 'cache_breakpoint' is unsupported
This file switches the flag off and strips it from messages as a safety net.
Remove this file (and the apply_patches() call) once CrewAI ships a fix.
"""
import sys

_APPLIED = False


def _strip(messages):
    if not isinstance(messages, list):
        return messages
    cleaned = []
    for m in messages:
        if isinstance(m, dict):
            m = {k: v for k, v in m.items() if k != "cache_breakpoint"}
            content = m.get("content")
            if isinstance(content, list):
                m["content"] = [
                    {k: v for k, v in part.items() if k != "cache_breakpoint"}
                    if isinstance(part, dict)
                    else part
                    for part in content
                ]
        cleaned.append(m)
    return cleaned


def apply_patches():
    global _APPLIED
    if _APPLIED:
        return
    _APPLIED = True

    # 1) Turn off CrewAI's cache-breakpoint marking everywhere it is used.
    try:
        import crewai.llms.cache as cache_module

        def _noop(message, *args, **kwargs):
            return message

        cache_module.mark_cache_breakpoint = _noop
        for name, module in list(sys.modules.items()):
            if name.startswith("crewai") and hasattr(module, "mark_cache_breakpoint"):
                module.mark_cache_breakpoint = _noop
    except Exception:
        pass

    # 2) Safety net: strip the flag right before the request goes to litellm.
    try:
        import litellm

        original_completion = litellm.completion

        def patched_completion(*args, **kwargs):
            if "messages" in kwargs:
                kwargs["messages"] = _strip(kwargs["messages"])
            return original_completion(*args, **kwargs)

        litellm.completion = patched_completion
        for name, module in list(sys.modules.items()):
            if name.startswith("crewai") and getattr(module, "completion", None) is original_completion:
                module.completion = patched_completion

        original_acompletion = litellm.acompletion

        async def patched_acompletion(*args, **kwargs):
            if "messages" in kwargs:
                kwargs["messages"] = _strip(kwargs["messages"])
            return await original_acompletion(*args, **kwargs)

        litellm.acompletion = patched_acompletion
        for name, module in list(sys.modules.items()):
            if name.startswith("crewai") and getattr(module, "acompletion", None) is original_acompletion:
                module.acompletion = patched_acompletion
    except Exception:
        pass
