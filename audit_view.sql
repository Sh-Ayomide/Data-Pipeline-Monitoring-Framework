CREATE OR REPLACE VIEW `database-502011.monitoring.pipeline_performance_audit` AS
SELECT
  job_id,
  project_id,
  user_email AS executed_by,
  job_type,
  statement_type, 
  creation_time AS start_time,
  end_time,
  TIMESTAMP_DIFF(end_time, creation_time, SECOND) AS duration_seconds,
  total_slot_ms / 1000 AS slot_seconds_used,
  total_bytes_billed,
  ROUND(total_bytes_billed / POW(1024, 3), 2) AS gigabytes_billed,
  ROUND((total_bytes_billed / POW(1024, 4)) * 6.25, 4) AS estimated_cost_usd, 
  error_result.reason AS error_reason,
  error_result.message AS error_message,
  IF(error_result.reason IS NULL, 'SUCCESS', 'FAILED') AS job_status
FROM
  `database-502011.region-africa-south1`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY);
