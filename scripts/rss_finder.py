import urllib.parse
import requests
import bs4  # BeautifulSoup
import xml.etree.ElementTree as ET
import re


def get_xml_namespace(tag):
    if "}" in tag:
        return tag.split("}")[1]
    return tag


def verify_feed_url(url, headers):
    try:
        resp = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        if resp.status_code == 200:
            content_type = resp.headers.get("Content-Type", "").lower()
            if "xml" in content_type or "rss" in content_type or "atom" in content_type:
                return url
    except Exception:
        pass
    return None


def check_sitemap_for_feed(sitemap_url, headers):
    try:
        resp = requests.get(sitemap_url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return None

        ct = resp.headers.get("Content-Type", "").lower()
        if "rss" in ct or "atom" in ct:
            return sitemap_url

        root = ET.fromstring(resp.content)

        def check_locs(elements):
            for el in elements:
                # BeautifulSoup-like finding in ElementTree is annoying,
                # so we use a simple namespace fallback
                loc = None
                for child in el:
                    if "loc" in child.tag.lower():
                        loc = child
                        break

                if loc is not None and loc.text:
                    candidate_url = loc.text.lower()
                    if (
                        "feed" in candidate_url
                        or "rss" in candidate_url
                        or "atom" in candidate_url
                        or candidate_url.endswith(".xml")
                        and "sitemap" not in candidate_url
                    ):
                        verified = verify_feed_url(loc.text, headers)
                        if verified:
                            return verified
            return None

        # Check standard URLs
        urls = root.findall(
            ".//{http://www.sitemaps.org/schemas/sitemap/0.9}url"
        ) + root.findall(".//url")
        if check_locs(urls):
            return check_locs(urls)

        # Check Sitemap Indexes
        sitemaps = root.findall(
            ".//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"
        ) + root.findall(".//sitemap")
        for sm in sitemaps:
            loc = sm.find(
                ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc"
            ) or sm.find(".//loc")
            if loc is not None and loc.text:
                child_result = check_sitemap_for_feed(loc.text, headers)
                if child_result:
                    return child_result

    except Exception:
        pass
    return None


def check_robots_and_sitemaps(base_url, headers):
    sitemap_urls = []
    robots_url = urllib.parse.urljoin(base_url, "/robots.txt")
    try:
        resp = requests.get(robots_url, headers=headers, timeout=5)
        if resp.status_code == 200:
            matches = re.findall(
                r"^Sitemap:\s*(.*)$", resp.text, re.IGNORECASE | re.MULTILINE
            )
            sitemap_urls.extend([m.strip() for m in matches])
    except Exception:
        pass

    standard_sitemap = urllib.parse.urljoin(base_url, "/sitemap.xml")
    if standard_sitemap not in sitemap_urls:
        sitemap_urls.append(standard_sitemap)

    for s_url in sitemap_urls:
        found = check_sitemap_for_feed(s_url, headers)
        if found:
            return found
    return None


def find_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Step 1: Check Headers
        try:
            resp_head = requests.head(
                url, headers=headers, timeout=5, allow_redirects=True
            )
            link_header = resp_head.headers.get("Link", "")
            if (
                "application/rss+xml" in link_header
                or "application/atom+xml" in link_header
            ):
                match = re.search(r"<(.*?)>", link_header)
                if match:
                    return match.group(1)
        except Exception:
            pass

        # Step 2: Parse HTML with BeautifulSoup (uses lxml by default if installed)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # "lxml" is much faster than the default "html.parser"
        soup = bs4.BeautifulSoup(response.text, "lxml")

        # Find the base URL for relative paths
        base_tag = soup.find("base")
        base_url = base_tag.get("href") if base_tag else url

        # Find all link tags
        # BeautifulSoup's syntax is much simpler than html5lib
        for link in soup.find_all("link", rel="alternate"):
            href = link.get("href")
            type_ = link.get("type", "").lower()

            if href and ("rss" in type_ or "atom" in type_):
                return urllib.parse.urljoin(base_url, href)

        # Step 3: Heuristics
        common_paths = ["/feed", "/rss", "/atom", "/rss.xml", "/atom.xml"]
        for path in common_paths:
            guess_url = urllib.parse.urljoin(base_url, path)
            verified = verify_feed_url(guess_url, headers)
            if verified:
                return verified

        # Step 4: Sitemap/Robots
        sitemap_feed = check_robots_and_sitemaps(base_url, headers)
        if sitemap_feed:
            return sitemap_feed

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python rss_finder.py [URL]")
        sys.exit(1)

    feed_url = find_feed(sys.argv[1])
    print(f"Feed URL found: {feed_url}" if feed_url else "No feed URL found.")
