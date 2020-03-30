-- Description: Exporter
-- Version: 0.0.1
-- License: GPL-3.0

function run(arg)
	
	host = getopt('host')
	command = getopt('command')
	port = getopt('port')
	
	if not host then
		info("Host was not set, using default `set host localhost`")
		-- host = 'host.docker.internal'
		host = 'localhost'
    end
	
	if not command then
		info("Command was not set, using default `set command json`")
		-- command = 'csv'
		command = 'json'
    end
	
	if not port then
		info("Port was not set, using default `set port 9008`")
		port = 9008
    end

    -- create connection
	sock = sock_connect(host, port)
    if last_err() then return end

    -- send command
	info("Sending Command: `" .. command .. "`")
	
	sock_send(sock, command)
	
    if last_err() then return end
	
end