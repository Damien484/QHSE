#!/usr/bin/env bash
# SessionStart hook for QHSE project
# Installs Python dependencies and injects superpowers context

set -euo pipefail

# Only run in remote Claude Code environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# Install Python dependencies
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

if [ -f "${PROJECT_DIR}/requirements.txt" ]; then
  pip install -r "${PROJECT_DIR}/requirements.txt" --quiet
fi

# Inject superpowers context
SKILLS_DIR="${PROJECT_DIR}/.claude/skills"
USING_SUPERPOWERS="${SKILLS_DIR}/using-superpowers/SKILL.md"

if [ ! -f "$USING_SUPERPOWERS" ]; then
  exit 0
fi

using_superpowers_content=$(cat "$USING_SUPERPOWERS" 2>/dev/null || echo "")

escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

using_superpowers_escaped=$(escape_for_json "$using_superpowers_content")
session_context="<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n**Below is the full content of your 'using-superpowers' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n${using_superpowers_escaped}\n</EXTREMELY_IMPORTANT>"

cat <<EOF
{
  "additional_context": "${session_context}",
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "${session_context}"
  }
}
EOF

exit 0
