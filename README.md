# Commute Delay Alerting

This scripts monitors your commute set in config.yaml and sends alerts when there is a delay or reroute found on your
route. Alerts are send once at start of delay or when reroute is detected. Final alert is send when delay or reroute is 
cleared. The Telegram API is used to send the alerts. Waze API is used to calculate delays or reroutes on the specified 
routes. I use this script to leave early when first delay alert is received or leave when all alerts are cleared to avoid 
traffic jams on my route. This keeps me from checking Waze or Google Maps for traffic jams manually.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/)

```bash
pip install -r requirements.txt
```

## Requirements

- .env file with telegram API token and chat_id 
  - copy env_example to .env
  - [generate-telegram-token-for-bot-api](https://medium.com/geekculture/generate-telegram-token-for-bot-api-d26faf9bf064)
- coordinates (lat,lon) of origin and destination
  - Open google maps
  - Right-click on place or area on map
  - Left-click coordinates from pop-up window
- config.yaml
  - copy and rename config_example.yaml
  - read comments in config_example.yaml for details
  
## Usage

Run main.py to start monitoring for delays or reroutes for your commute. 