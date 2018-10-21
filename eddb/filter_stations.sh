jq -c '.[] | del(.selling_modules)' stations.json | jq -cs '.'
