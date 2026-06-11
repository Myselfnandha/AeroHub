import os
import json

log_path = r"C:\Users\NANDHA A\.gemini\antigravity-ide\brain\1237cb3f-efd0-4a57-b440-f74287d1898a\.system_generated\logs\transcript.jsonl"
output_dir = r"c:\Users\NANDHA A\Desktop\UTILITIES\scratch\extracted"
os.makedirs(output_dir, exist_ok=True)

with open(log_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        data = json.loads(line)
        step_idx = data.get("step_index")
        tool_calls = data.get("tool_calls", [])
        if not tool_calls:
            continue
            
        for tc_idx, tc in enumerate(tool_calls):
            args = tc.get("args", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    pass
            
            # Check if this tool call modifies health_app.py
            target_file = args.get("TargetFile", "")
            if "health_app.py" in target_file or any("health_app.py" in str(v) for v in args.values()):
                print(f"Step {step_idx} matches. Tool: {tc.get('name')}")
                # Save the arguments to a file
                out_path = os.path.join(output_dir, f"step_{step_idx}_tc_{tc_idx}.json")
                with open(out_path, "w", encoding="utf-8") as out:
                    json.dump(args, out, indent=2)
                
                # If there's replacement content, save it separately
                repl = args.get("ReplacementContent")
                if repl:
                    repl_path = os.path.join(output_dir, f"step_{step_idx}_replacement.py")
                    with open(repl_path, "w", encoding="utf-8") as out:
                        out.write(repl)
