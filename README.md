# mining-slackbot-alert
Python script to send mining alerts to a slackbot. Docker container included.

Currently works with Claymore-Dual-Ehterum-miner and sends GPU temperature alerts. Can monitor multiple miners and GPUs

## Future Updates
Work with additional miner programs
Alerts based off hash rate
Alerts based off rejected shares

## Config
Rename example.yaml to config.yaml and enter in your slack keys and miner hosts.

You can change the gpu_alert_temp to your liking, but it is defaulted to check for 80C
