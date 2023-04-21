package main

// configuration
const (
	minRuleHits = 1
	maxRuleHits = 10
)

type RuleHit struct {
	RuleFQDN  string
	ErrorKey  string
	TotalRisk uint
}

var ruleHits = []RuleHit{
	RuleHit{
		"nodes_requirements_check",
		"NODES_MINIMUM_REQUIREMENTS_NOT_MET",
		2,
	},
	RuleHit{
		"bug_1234567",
		"BUGZILLA_BUG_1234567",
		1,
	},
	RuleHit{
		"bug_5678900",
		"BUGZILLA_BUG_5678900",
		2,
	},
	RuleHit{
		"bug_9999999",
		"BUGZILLA_BUG_9999999",
		2,
	},
	RuleHit{
		"nodes_kubelet_version_check",
		"NODE_KUBELET_VERSION",
		3,
	},
	RuleHit{
		"samples_op_failed_image_import_check",
		"SAMPLES_FAILED_IMAGE_IMPORT_ERR",
		0},
	RuleHit{
		"cluster_wide_proxy_auth_check",
		"AUTH_OPERATOR_PROXY_ERROR",
		3,
	},
	RuleHit{
		"image_registry_pv_not_bound",
		"MISSING_REQUIREMENTS",
		5,
	},
}

func main() {
}
