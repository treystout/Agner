local queue_name = KEYS[1]
local job = redis.call("RPOP", queue_name)
if job then
  local job_details = cjson.decode(job)
  job_details['blah'] = 25
  local updated_job = cjson.encode(job_details)
  redis.log(redis.LOG_NOTICE, "found job "..job_details['job_id'])
  redis.call("SET", "AGNER:RESERVED:"..job_details['job_id'], updated_job)
  redis.call("RPUSH", "AGNER:PROCESSING:"..queue_name, updated_job)
  return job
else
  return nil
end
