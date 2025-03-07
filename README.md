# Cloudflare Tunnel Status Monitor

This Python script is designed to monitor the health of a specific Cloudflare Tunnel and update a status page when the tunnel's status changes. It utilizes the Cloudflare API to check the tunnel's status and sends alerts to an Instatus webhook.

---

## Features

- Monitors the status of a Cloudflare Tunnel using the Cloudflare API.
- Sends status updates (UP/DOWN) to an Instatus webhook.
- Provides real-time logging for tunnel statuses and errors.
- Includes automatic error handling and retry logic.

---

## Prerequisites

Before using the script, ensure you have the following:

1. **Cloudflare Account**: Obtain your Cloudflare **Token**, **Email**, **Account ID**, and the **Tunnel ID** you want to monitor.
2. **Instatus Webhook**: Set up an Instatus status page and create a webhook integration. Replace `<YOUR WEBHOOK CODE>` in the script with your actual webhook code.
3. **Python Libraries**: Install the required Python libraries:
   ```bash
   pip install requests
