"""
TestFlight page scraper — checks if beta slots are available.
"""
import logging
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from config import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

FULL_INDICATORS = [
    "This beta is full",
    "This beta isn't accepting any new testers",
    "This beta isn't accepting",
]

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.5 Mobile/15E148 Safari/604.1"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


@dataclass
class CheckResult:
    status: str
    app_name: str
    error: str = ""


def _extract_app_name(soup: BeautifulSoup) -> str:
    title_tag = soup.find("title")
    if title_tag:
        t = title_tag.get_text(strip=True)
        if "Join the" in t and "beta" in t:
            name = t.split("Join the", 1)[1].split("beta", 1)[0].strip()
            if name:
                return name

    for sel in [".app-name", "h1"]:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)

    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"]

    return "Unknown App"


def check_testflight(url: str) -> CheckResult:
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if resp.status_code != 200:
            return CheckResult("error", "Unknown App", f"HTTP {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        app_name = _extract_app_name(soup)
        is_full = any(ind.lower() in resp.text.lower() for ind in FULL_INDICATORS)
        status = "full" if is_full else "available"

        logger.info("Checked %s — %s: %s", url, app_name, status)
        return CheckResult(status=status, app_name=app_name)

    except requests.Timeout:
        return CheckResult("error", "Unknown App", "Request timed out")
    except requests.ConnectionError:
        return CheckResult("error", "Unknown App", "Connection failed")
    except Exception as e:
        logger.exception("Error checking %s", url)
        return CheckResult("error", "Unknown App", str(e))
