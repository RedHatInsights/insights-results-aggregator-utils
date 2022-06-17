-- These queries let you duplicate the data in the aggregator database. This way you don't need to use the db-writer anymore for generating more and more data :)

-- Recommendation
INSERT INTO 
    recommendation (org_id, cluster_id, rule_fqdn, error_key, rule_id, created_at)
SELECT org_id, gen_random_uuid() AS cluster_id, rule_fqdn, error_key, rule_id, created_at
	FROM recommendation;

-- Rule_hit
INSERT INTO 
    rule_hit (org_id, cluster_id, rule_fqdn, error_key, template_data)
SELECT org_id, gen_random_uuid() AS cluster_id, rule_fqdn, error_key, template_data
	FROM rule_hit;

-- Report
INSERT INTO 
    report (org_id, cluster, report, reported_at, last_checked_at, kafka_offset, gathered_at)
SELECT org_id, gen_random_uuid() AS cluster, report, reported_at, last_checked_at, kafka_offset, gathered_at
	FROM report;