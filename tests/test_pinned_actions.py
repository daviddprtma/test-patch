import os
def test_github_actions_pinned_to_sha():
    workflows_dir = ".github/workflows"
    if not os.path.exists(workflows_dir):
        raise AssertionError(f"Directory {workflows_dir} not found")

    found_yaml = False
    uses_count = 0
    for filename in os.listdir(workflows_dir):
        if not filename.endswith((".yml", ".yaml")):
            continue
        found_yaml = True
        filepath = os.path.join(workflows_dir, filename)
        with open(filepath, "r") as f:
            for line_no, line in enumerate(f, 1):
                if "uses:" not in line or line.strip().startswith("#"):
                    continue
                part = line.split("uses:", 1)[1].strip()
                if not part:
                    continue
                action_ref = part.split()[0]
                if "@" not in action_ref:
                    if action_ref.startswith("./") or action_ref.startswith(".\\"):
                        continue
                    raise AssertionError(f"File {filename}, line {line_no}: Action {action_ref} has no @ref")
                action, ref = action_ref.split("@", 1)
                uses_count += 1
                if len(ref) != 40 or not all(c in "0123456789abcdefABCDEF" for c in ref):
                    raise AssertionError(f"File {filename}, line {line_no}: Action {action} reference is not a 40-char SHA: {ref}")

    if not found_yaml:
        raise AssertionError("No workflows found inside .github/workflows")
    if uses_count == 0:
        raise AssertionError("No uses directives found in any workflows")
