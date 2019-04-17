-- Description: Retrieve names of ssl protected (sub)domains from certificate transparancy logs using cert spotter (https://sslmate.com/certspotter).
-- Version: 0.1.1
-- Source: domains
-- License: GPL-3.0

function run(domain)
    session = http_mksession()

    request = http_request(session, 'GET', 'https://api.certspotter.com/v1/issuances', {
        query={
            include_subdomains='true',
            expand='dns_names',
            domain=domain['value'],
        }, 
        user_agent='sn0int cert spotter module',
    })
    response = http_send(request)
    if last_err() then return end
    if response['status'] ~= 200 then 
        return 'http status: ' .. response['status'] 
    end
    api_output = json_decode(response['text'])
    if #api_output > 0 
    then
        for cert_counter = 1, #api_output
        do
            for domain_counter = 1, #api_output[cert_counter]['dns_names']
            do
                new_domain = api_output[cert_counter]['dns_names'][domain_counter]
                new_psl_domain = psl_domain_from_dns_name(new_domain) 
                domain_id = db_add('domain', {
                    value=new_psl_domain,
                })    
                if domain_id ~= nil and new_domain ~= new_psl_domain then
                    db_add('subdomain', {
                        domain_id=domain_id,
                        value=new_domain,
                    })
                end
            end
        end 
    end
end
