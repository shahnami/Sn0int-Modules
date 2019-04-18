-- Description: Exporter
-- Version: 0.0.1
-- License: GPL-3.0

function run(arg)
	
	command = getopt('command')
	
	if not command then
        error("Command is not set, e.g. \"set command json\"")
		return
    end

    -- create connection
	sock = sock_connect("host.docker.internal", 9008)
    if last_err() then return end

    -- send command
	info("Sending Command: `" .. command .. "`")
	
	sock_send(sock, command)
	
    if last_err() then return end
	
end