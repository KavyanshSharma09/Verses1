"""
Self-pinging keep-alive for Render free tier.

Starts a background daemon thread that sends a GET request to the app's own
health-check endpoint every 5 minutes, preventing Render from spinning down
the instance due to inactivity.

The thread is a daemon, so it dies automatically when gunicorn shuts down.
"""

import logging
import os
import threading
import time
import urllib.request
import urllib.error

logger = logging.getLogger("keep_alive")

RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "")
PING_INTERVAL = 5 * 60  # 5 minutes in seconds
REQUEST_TIMEOUT = 25     # seconds

_started = False
_lock = threading.Lock()


def _ping_loop(url: str) -> None:
    """Runs forever in a daemon thread, pinging the health endpoint."""
    health_url = f"{url.rstrip('/')}/health/"
    logger.info("Keep-alive thread started → pinging %s every %ds", health_url, PING_INTERVAL)

    while True:
        try:
            req = urllib.request.Request(health_url, method="GET")
            req.add_header("User-Agent", "Verses1-KeepAlive/1.0")
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                logger.info("Keep-alive ping → %s (status %d)", health_url, resp.status)
        except urllib.error.HTTPError as exc:
            # Server responded (it's awake), even if with an error code.
            logger.warning("Keep-alive ping → %s (HTTP %d)", health_url, exc.code)
        except Exception as exc:
            logger.warning("Keep-alive ping failed → %s: %s", health_url, exc)

        time.sleep(PING_INTERVAL)


def start() -> None:
    """Start the keep-alive thread (idempotent, production-only)."""
    global _started

    # Only run on Render (RENDER_EXTERNAL_URL is set automatically by Render)
    if not RENDER_EXTERNAL_URL:
        logger.debug("RENDER_EXTERNAL_URL not set — skipping keep-alive (dev mode).")
        return

    with _lock:
        if _started:
            return
        _started = True

    thread = threading.Thread(target=_ping_loop, args=(RENDER_EXTERNAL_URL,), daemon=True)
    thread.start()
    logger.info("Keep-alive background thread launched.")
