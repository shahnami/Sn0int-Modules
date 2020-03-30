-- Description: Importer
-- Version: 0.0.1
-- License: GPL-3.0

function run(arg)
	
	url = 'http://127.0.0.1:8000/jobs/targets.txt'
	
    session = http_mksession()
    req = http_request(session, 'GET', url, {})
    resp = http_send(req)
    
	if last_err() then return end
	
    if resp['status'] ~= 200 then return 'http error: ' .. resp['status'] end
	
	results = regex_find_all("[^\r\n]+", resp['text'])
	for i = 1, #results do
		info("Adding " .. results[i][1])
		domain_id = db_add('domain', {
			value=results[i][1],
		})
	end	  
end