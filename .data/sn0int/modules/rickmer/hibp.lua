-- Description: check email addresses for known password leaks
-- Version: 0.1.0
-- Source: emails
-- License: GPL-3.0

function run(emailaddress)
    session = http_mksession()

    request = http_request(session, 'GET', 'https://haveibeenpwned.com/api/v2/breachedaccount/' .. emailaddress['value'], {
         user_agent='sn0int hibp module' 
    })
    
    response = http_send(request)
    if last_err() then return end
    if response['status'] == 404 then
        info('0 breaches found')    
        return 
    elseif response['status'] ~= 200 then 
        return 'http error: ' .. response['status'] 
    end
    api_output = json_decode(response['text'])
    if #api_output > 0 
    then
        for counter = 1, #api_output
        do
            breach = db_add('breach', {value=api_output[counter]['Description'],})
            db_add('breach-email', {breach_id=breach, email_id=emailaddress['id'],})
        end 
        info(#api_output .. ' breaches found')
    end
    sleep(1.5)
end
