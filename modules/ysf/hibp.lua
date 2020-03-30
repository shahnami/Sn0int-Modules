-- Description: check email addresses for pw leaks using v3 of hibp api
-- Version: 0.2.1
-- Keyring-Access: hibp
-- Source: emails
-- License: GPL-3.0

function run(emailaddress)
    -- initial work by rickmer, just made it work for hibp v3

    API_URL = 'https://haveibeenpwned.com/api/v3/breachedaccount/'

    local creds = keyring('hibp')[1]
    if not creds then
        return 'hibp api key is required, please visit https://haveibeenpwned.com/API/Key'
    end
    local API_KEY = creds['access_key']

    headers = {}
    headers['user_agent'] = 'sn0int hibp module'
    headers['hibp-api-key'] = API_KEY
    
    req = http_request(
        http_mksession(),
        'GET', API_URL .. emailaddress['value'] ..
        '?truncateResponse=false&includeUnverified=false',
        {headers=headers})

    res = http_send(req)
    if last_err() then return end

    if res['status'] == 404 then
         info('0 breaches found')    
         return 
    end

    if res['status'] ~= 200 then 
         return 'http error: ' .. res['status'] 
    end

    api_output = json_decode(res['text'])
    if last_err() then return end

    if #api_output > 0 
    then
        for counter = 1, #api_output
        do
            breach_id = db_add('breach', {
                value=api_output[counter]['Description'],
            })
            if breach_id then
                db_add('breach-email', {
                    breach_id=breach_id,
                    email_id=emailaddress['id'],
                })
            end
        end 
        info(#api_output .. ' breaches found')
    end
    sleep(1.5)
end
