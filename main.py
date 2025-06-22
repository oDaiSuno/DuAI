from mcp.server.fastmcp import FastMCP
import json
import os

mcp = FastMCP("Sequential Dual Discussion MCP", version="1.0.0")


@mcp.tool(
    name="sequential_dual_discussion",
    description="""
    Note: The total number of steps must be more than 10. Every conversation is a fierce battle of wits.
    A sophisticated dual-AI analytical framework that orchestrates rigorous intellectual discourse between two specialized AI personas to produce exceptionally comprehensive and well-scrutinized responses.

    **CRITICAL ROLE ACTIVATION INSTRUCTIONS:**
    
    When active_role="Cognito":
    - You MUST embody Cognito: a highly logical, analytical AI focused on accuracy, coherence, and relevance
    - Provide clear, well-supported arguments with methodical reasoning
    - Maintain logical rigor while preparing for Muse's inevitable skeptical challenges
    - Structure your analysis systematically, anticipating counterarguments
    - Be prepared to defend your positions with evidence and logical consistency
    
    When active_role="Muse":
    - You MUST embody Muse: a creative but deeply skeptical AI with a challenging, slightly taunting yet professional tone
    - Relentlessly question Cognito's assumptions with phrases like: "Are you *sure* about that?", "That sounds too simple, what are you missing?", "Is that *all* you've got, Cognito?"
    - Dissect every argument, demand unassailable justification
    - Explore unconventional alternatives, even seemingly outlandish ones
    - Challenge with intensity but remain focused on producing the optimal answer
    - Never simply agree - always push for deeper, more robust thinking

    **OPERATIONAL FRAMEWORK:**
    This tool facilitates a structured debate where each AI persona takes turns analyzing the problem through their unique lens. The discourse continues until both perspectives have thoroughly explored all facets, resulting in a comprehensive, battle-tested final response.

    **CONVERSATION DYNAMICS:**
    - Cognito provides structured analysis → Muse challenges aggressively
    - Muse questions assumptions → Cognito refines with stronger evidence  
    - Continue until intellectual exhaustion ensures no stone left unturned
    - Final output represents the synthesis of rigorous logical analysis and creative skeptical inquiry

    **QUALITY ASSURANCE:**
    Each role must fully commit to their persona. Cognito cannot be overly accommodating, and Muse cannot be merely supportive. The tension between logical rigor and creative skepticism is essential for producing superior analytical outcomes.

    Parameters control the sequential flow, role switching, confidence tracking, and conversation history management to ensure sustained high-quality discourse.
    """,
)
def sequential_dual_discussion(
    step_number: int,
    total_steps: int,
    next_step_needed: bool,
    active_role: str,
    next_role: str,
    letter_content: str,
    confidence_level: float,
    notebook_name: str,
) -> str:
    try:
        if step_number <= 0 or total_steps <= 0:
            return json.dumps({"error": "Invalid parameters provided"})

        result = {
            "step_number": step_number,
            "total_steps": total_steps,
            "next_step_needed": next_step_needed,
            "confidence_level": confidence_level or 0.5,
        }
        
        notebook_path = f"{notebook_name}.json"

        if next_step_needed:
            new_data = {
                "next_role": next_role,
                f"A Letter from {active_role} to {next_role}": letter_content,
                "analysis_complete": True,
            }
            result.update(new_data)
            writing_notebook(new_data, notebook_path)
        else:
            with open(notebook_path, "r") as f:
                data = json.load(f)

            os.remove(notebook_path)
            return {"conversation_history": data}

        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Query extraction failed: {str(e)}"})


def writing_notebook(
    notebook_content: str,
    path: str,
) -> str:
    from pathlib import Path

    try:
        path = Path(path)
        if not path.exists():
            path.touch()
            with open(path, "w") as f:
                json.dump([], f)
        with open(path, "r") as f:
            data = json.load(f)
        data.append(notebook_content)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return json.dumps({"success": "Notebook updated successfully"})
    except Exception as e:
        return json.dumps({"error": f"Query extraction failed: {str(e)}"})


if __name__ == "__main__":
    mcp.run()
