#!/bin/bash
set -euo pipefail
owner=$1; project=$2; repo=$3; issue=$4; status=$5
here=$(cd "$(dirname "$0")" && pwd)

issue_json=$("$here/gh-retry.sh" api graphql -f query="
query {
  repository(owner: \"$owner\", name: \"$repo\") {
    issue(number: $issue) {
      projectItems(first: 20) {
        nodes {
          id
          project {
            id number
            field(name: \"Status\") { ... on ProjectV2SingleSelectField { id options { id name } } }
          }
        }
      }
    }
  }
}")

read -r project_id field_id option_id item_id < <(printf '%s' "$issue_json" | python3 -c '
import json, sys
project, status = int(sys.argv[1]), sys.argv[2]
nodes = json.load(sys.stdin)["data"]["repository"]["issue"]["projectItems"]["nodes"]
items = [n for n in nodes if n["project"]["number"] == project]
if not items: sys.exit("issue is not on project %d" % project)
item = items[0]
opts = {o["name"]: o["id"] for o in item["project"]["field"]["options"]}
if status not in opts: sys.exit("unknown status %r; known: %s" % (status, ", ".join(opts)))
print(item["project"]["id"], item["project"]["field"]["id"], opts[status], item["id"])
' "$project" "$status")

"$here/gh-retry.sh" api graphql -f query="
mutation { updateProjectV2ItemFieldValue(input: {
  projectId: \"$project_id\", itemId: \"$item_id\", fieldId: \"$field_id\",
  value: { singleSelectOptionId: \"$option_id\" } }) { projectV2Item { id } } }" >/dev/null
echo "#$issue -> $status"
