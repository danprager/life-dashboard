"""
Fire danger service.
Fetches and parses the CFA RSS feed for Total Fire Ban status
and Fire Danger Ratings by Victorian district.
No external dependencies — uses Python stdlib only.
"""
import html
import re
import urllib.request
from datetime import datetime
from xml.etree import ElementTree as ET

from app.models.weather import FireDangerDay

CFA_FEED_URL = "https://www.cfa.vic.gov.au/cfa/rssfeed/tfbfdrforecast_rss.xml"


def _parse_district_lines(paragraph: str) -> dict[str, str]:
    """Extract 'District: Value' pairs from an HTML paragraph string."""
    clean = re.sub(r'<[^>]+>', '\n', paragraph)
    result = {}
    for line in clean.splitlines():
        line = line.strip()
        if ':' in line:
            district, _, value = line.partition(':')
            district = district.strip()
            value = value.strip()
            if district and value:
                result[district] = value
    return result


def _title_case_rating(rating: str) -> str:
    """Convert 'VERY HIGH' -> 'Very High', 'LOW-MODERATE' -> 'Low-Moderate'."""
    return '-'.join(part.title() for part in rating.split('-'))


def parse_fire_xml(xml_data) -> dict:
    """
    Parse CFA RSS XML bytes/string.
    Returns dict mapping district name to:
      - "total_fire_ban": bool  (today = first item only)
      - "fire_danger": list[FireDangerDay]  (today + next 3 days)
    Returns {} on parse error.
    """
    try:
        if isinstance(xml_data, str):
            xml_data = xml_data.encode('utf-8')
        # Strip UTF-8 BOM if present
        xml_data = xml_data.lstrip(b'\xef\xbb\xbf')

        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')[:4]  # today + 3 days

        if not items:
            return {}

        # Parse each item into (day_letter, tfb_by_district, rating_by_district)
        parsed_days = []
        for item in items:
            title = item.findtext('title', '').strip()
            description = item.findtext('description', '')

            # Derive single-letter weekday from title e.g. "Thursday, 19 February 2026"
            try:
                date = datetime.strptime(title, '%A, %d %B %Y')
                day_letter = date.strftime('%A')[0]
            except ValueError:
                day_letter = '?'

            decoded = html.unescape(description)
            paragraphs = re.split(r'</p>', decoded)

            # Find the "Fire Danger Ratings" header paragraph
            fdr_idx = next(
                (i for i, p in enumerate(paragraphs) if 'Fire Danger Ratings' in p),
                None
            )

            tfb_by_district: dict[str, bool] = {}
            rating_by_district: dict[str, str] = {}

            if fdr_idx is not None:
                # TFB section is the paragraph immediately before the FDR header
                if fdr_idx > 0:
                    for district, value in _parse_district_lines(paragraphs[fdr_idx - 1]).items():
                        tfb_by_district[district] = 'YES' in value and 'NO' not in value

                # FDR ratings are in the paragraph immediately after the FDR header
                if fdr_idx + 1 < len(paragraphs):
                    for district, value in _parse_district_lines(paragraphs[fdr_idx + 1]).items():
                        rating_by_district[district] = _title_case_rating(value)

            parsed_days.append((day_letter, tfb_by_district, rating_by_district))

        # Collect all district names seen across all days
        all_districts: set[str] = set()
        for _, tfb_map, rating_map in parsed_days:
            all_districts.update(tfb_map.keys())
            all_districts.update(rating_map.keys())

        # Build result per district
        result = {}
        _, today_tfb, _ = parsed_days[0]
        for district in all_districts:
            fire_danger = []
            for day_letter, _, rating_map in parsed_days:
                fire_danger.append(FireDangerDay(
                    day=day_letter,
                    rating=rating_map.get(district, 'Unknown'),
                    index=None,
                ))
            result[district] = {
                "total_fire_ban": today_tfb.get(district, False),
                "fire_danger": fire_danger,
            }

        return result

    except ET.ParseError:
        return {}


def fetch_fire_data() -> dict:
    """
    Fetch the live CFA RSS feed and parse it.
    Returns {} on any network or parse error so callers degrade gracefully.
    """
    try:
        with urllib.request.urlopen(CFA_FEED_URL, timeout=10) as response:
            xml_bytes = response.read()
        return parse_fire_xml(xml_bytes)
    except Exception:
        return {}
