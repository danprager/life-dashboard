"""
Fire danger service.
Fetches fire danger data from two sources:
- BOM XML feed: fire danger ratings and FBI index per district
- CFA RSS feed: Total Fire Ban status per district
No external dependencies — uses Python stdlib only.
"""
import html
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from xml.etree import ElementTree as ET

from app.models.weather import FireDangerDay

BOM_FEED_URL = "https://www.bom.gov.au/fwo/IDV18555.xml"
CFA_FEED_URL = "https://www.cfa.vic.gov.au/cfa/rssfeed/tfbfdrforecast_rss.xml"


def parse_bom_xml(xml_data) -> dict:
    """
    Parse BOM fire danger XML feed.
    Returns dict mapping district name to list of FireDangerDay (4 days).
    Returns {} on parse error.
    """
    try:
        if isinstance(xml_data, bytes):
            xml_data = xml_data.decode('utf-8')
        root = ET.fromstring(xml_data)
        result = {}
        for area in root.findall('./forecast/area[@type="fire-district"]'):
            district = area.get('description')
            if not district:
                continue
            days = []
            for period in sorted(area.findall('forecast-period'),
                                 key=lambda p: int(p.get('index', 99)))[:4]:
                start = period.get('start-time-local', '')
                try:
                    day_letter = datetime.strptime(start[:10], '%Y-%m-%d').strftime('%A')[0]
                except ValueError:
                    day_letter = '?'
                fbi_el = period.find('element[@type="fire_behaviour_index"]')
                fdr_el = period.find('text[@type="fire_danger"]')
                index = int(fbi_el.text) if fbi_el is not None and fbi_el.text else None
                rating = fdr_el.text.strip() if fdr_el is not None and fdr_el.text else 'Unknown'
                days.append(FireDangerDay(day=day_letter, rating=rating, index=index))
            if days:
                result[district] = days
        return result
    except ET.ParseError:
        return {}


def parse_cfa_tfb(xml_data) -> dict:
    """
    Parse CFA RSS feed for Total Fire Ban status only.
    Returns dict mapping district name to bool.
    Returns {} on parse error.
    """
    try:
        if isinstance(xml_data, str):
            xml_data = xml_data.encode('utf-8')
        xml_data = xml_data.lstrip(b'\xef\xbb\xbf')
        root = ET.fromstring(xml_data)
        items = root.findall('./channel/item')
        if not items:
            return {}
        # TFB is only for today — first item
        description = items[0].findtext('description', '')
        decoded = html.unescape(description)
        paragraphs = re.split(r'</p>', decoded)
        fdr_idx = next(
            (i for i, p in enumerate(paragraphs) if 'Fire Danger Ratings' in p),
            None
        )
        if fdr_idx is None or fdr_idx == 0:
            return {}
        result = {}
        for district, value in _parse_district_lines(paragraphs[fdr_idx - 1]).items():
            result[district] = 'YES' in value and 'NO' not in value
        return result
    except ET.ParseError:
        return {}


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


def _fetch_url(url: str, timeout: int = 10) -> bytes:
    """Fetch a URL and return the response bytes."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def fetch_fire_data() -> dict:
    """
    Fetch BOM and CFA feeds concurrently.
    BOM feed provides fire danger ratings and FBI index per district.
    CFA feed provides Total Fire Ban status per district.
    Returns dict: { district: { total_fire_ban: bool, fire_danger: list|None } }
    Each feed degrades independently on error.
    """
    bom_xml = None
    cfa_xml = None

    def fetch_bom():
        return _fetch_url(BOM_FEED_URL)

    def fetch_cfa():
        return _fetch_url(CFA_FEED_URL)

    with ThreadPoolExecutor(max_workers=2) as executor:
        bom_future = executor.submit(fetch_bom)
        cfa_future = executor.submit(fetch_cfa)
        try:
            bom_xml = bom_future.result()
        except Exception:
            pass
        try:
            cfa_xml = cfa_future.result()
        except Exception:
            pass

    bom_data = parse_bom_xml(bom_xml) if bom_xml else {}
    cfa_data = parse_cfa_tfb(cfa_xml) if cfa_xml else {}

    all_districts = set(bom_data.keys()) | set(cfa_data.keys())
    result = {}
    for district in all_districts:
        result[district] = {
            "total_fire_ban": cfa_data.get(district, False),
            "fire_danger": bom_data.get(district),
        }
    return result
