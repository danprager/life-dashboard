"""
Unit tests for fire service.
Tests XML parsing logic in isolation — no network calls made.
"""
import pytest
from unittest.mock import patch, MagicMock

from app.services.fire import parse_bom_xml, parse_cfa_tfb, fetch_fire_data

# Minimal sample RSS XML matching the real CFA feed structure.
# Day 1 (Thursday): North Central has TFB=YES, rating=EXTREME; Central has TFB=NO, rating=MODERATE
# Day 2 (Friday): no TFBs, North Central=HIGH, Central=HIGH
# Day 3 (Saturday): no TFBs, North Central=VERY HIGH, Central=MODERATE
# Day 4 (Sunday): no TFBs, North Central=MODERATE, Central=LOW-MODERATE
SAMPLE_XML = b"""<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0"><channel>
<title>CFA Fire Danger Ratings</title>
<item>
  <title>Thursday, 19 February 2026</title>
  <description>&lt;p&gt;Today is a day of Total Fire Ban.&lt;/p&gt;&lt;p&gt;North Central: YES&lt;br&gt;Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;&lt;/p&gt;&lt;p&gt;Fire Danger Ratings&lt;br/&gt;&lt;/p&gt;&lt;p&gt;North Central: EXTREME&lt;br&gt;Central: MODERATE&lt;br&gt;&lt;/p&gt;</description>
</item>
<item>
  <title>Friday, 20 February 2026</title>
  <description>&lt;p&gt;Tomorrow is not currently a day of Total Fire Ban.&lt;/p&gt;&lt;p&gt;North Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;&lt;/p&gt;&lt;p&gt;Fire Danger Ratings&lt;br/&gt;&lt;/p&gt;&lt;p&gt;North Central: HIGH&lt;br&gt;Central: HIGH&lt;br&gt;&lt;/p&gt;</description>
</item>
<item>
  <title>Saturday, 21 February 2026</title>
  <description>&lt;p&gt;Not a day of Total Fire Ban.&lt;/p&gt;&lt;p&gt;North Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;&lt;/p&gt;&lt;p&gt;Fire Danger Ratings&lt;br/&gt;&lt;/p&gt;&lt;p&gt;North Central: VERY HIGH&lt;br&gt;Central: MODERATE&lt;br&gt;&lt;/p&gt;</description>
</item>
<item>
  <title>Sunday, 22 February 2026</title>
  <description>&lt;p&gt;Not a day of Total Fire Ban.&lt;/p&gt;&lt;p&gt;North Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;&lt;/p&gt;&lt;p&gt;Fire Danger Ratings&lt;br/&gt;&lt;/p&gt;&lt;p&gt;North Central: MODERATE&lt;br&gt;Central: LOW-MODERATE&lt;br&gt;&lt;/p&gt;</description>
</item>
<item>
  <title>Monday, 23 February 2026</title>
  <description>&lt;p&gt;Not a day of Total Fire Ban.&lt;/p&gt;&lt;p&gt;North Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;Central: NO - RESTRICTIONS MAY APPLY&lt;br&gt;&lt;/p&gt;&lt;p&gt;Fire Danger Ratings&lt;br/&gt;&lt;/p&gt;&lt;p&gt;North Central: MODERATE&lt;br&gt;Central: MODERATE&lt;br&gt;&lt;/p&gt;</description>
</item>
</channel></rss>"""


# Minimal BOM XML feed sample.
# Central: F=High(34), S=Moderate(23), S=High(42), M=Moderate(20)
# North Central: F=High(36), S=High(35), S=High(33), M=Moderate(16)
BOM_SAMPLE_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<product>
  <forecast>
    <area aac="VIC_FW007" description="Central" type="fire-district">
      <forecast-period index="0" start-time-local="2026-02-20T05:25:00+11:00">
        <element type="fire_behaviour_index">34</element>
        <text type="fire_danger">High</text>
      </forecast-period>
      <forecast-period index="1" start-time-local="2026-02-21T00:00:00+11:00">
        <element type="fire_behaviour_index">23</element>
        <text type="fire_danger">Moderate</text>
      </forecast-period>
      <forecast-period index="2" start-time-local="2026-02-22T00:00:00+11:00">
        <element type="fire_behaviour_index">42</element>
        <text type="fire_danger">High</text>
      </forecast-period>
      <forecast-period index="3" start-time-local="2026-02-23T00:00:00+11:00">
        <element type="fire_behaviour_index">20</element>
        <text type="fire_danger">Moderate</text>
      </forecast-period>
    </area>
    <area aac="VIC_FW008" description="North Central" type="fire-district">
      <forecast-period index="0" start-time-local="2026-02-20T05:25:00+11:00">
        <element type="fire_behaviour_index">36</element>
        <text type="fire_danger">High</text>
      </forecast-period>
      <forecast-period index="1" start-time-local="2026-02-21T00:00:00+11:00">
        <element type="fire_behaviour_index">35</element>
        <text type="fire_danger">High</text>
      </forecast-period>
      <forecast-period index="2" start-time-local="2026-02-22T00:00:00+11:00">
        <element type="fire_behaviour_index">33</element>
        <text type="fire_danger">High</text>
      </forecast-period>
      <forecast-period index="3" start-time-local="2026-02-23T00:00:00+11:00">
        <element type="fire_behaviour_index">16</element>
        <text type="fire_danger">Moderate</text>
      </forecast-period>
    </area>
  </forecast>
</product>"""


# --- parse_bom_xml tests ---

def test_bom_returns_known_districts():
    result = parse_bom_xml(BOM_SAMPLE_XML)
    assert "Central" in result
    assert "North Central" in result


def test_bom_fire_danger_has_4_days():
    result = parse_bom_xml(BOM_SAMPLE_XML)
    assert len(result["Central"]) == 4


def test_bom_fbi_index_is_integer():
    result = parse_bom_xml(BOM_SAMPLE_XML)
    assert result["Central"][0].index == 34
    assert result["North Central"][0].index == 36


def test_bom_rating_extracted():
    result = parse_bom_xml(BOM_SAMPLE_XML)
    assert result["Central"][0].rating == "High"
    assert result["Central"][1].rating == "Moderate"


def test_bom_day_letters_from_dates():
    result = parse_bom_xml(BOM_SAMPLE_XML)
    days = [d.day for d in result["Central"]]
    assert days == ["F", "S", "S", "M"]


def test_bom_returns_empty_on_malformed_xml():
    assert parse_bom_xml(b"not xml <<<") == {}


# --- parse_cfa_tfb tests ---

def test_cfa_tfb_north_central_has_ban():
    result = parse_cfa_tfb(SAMPLE_XML)
    assert result["North Central"] is True


def test_cfa_tfb_central_has_no_ban():
    result = parse_cfa_tfb(SAMPLE_XML)
    assert result["Central"] is False


def test_cfa_tfb_returns_empty_on_malformed_xml():
    assert parse_cfa_tfb(b"not xml <<<") == {}



def test_fetch_fire_data_merges_bom_and_cfa():
    with patch("app.services.fire._fetch_url") as mock_fetch:
        def side_effect(url, timeout=10):
            if "bom.gov.au" in url:
                return BOM_SAMPLE_XML
            return SAMPLE_XML
        mock_fetch.side_effect = side_effect
        result = fetch_fire_data()
    assert result["Central"]["total_fire_ban"] is False
    assert result["North Central"]["total_fire_ban"] is True
    assert result["Central"]["fire_danger"][0].index == 34
    assert result["North Central"]["fire_danger"][0].index == 36


def test_fetch_fire_data_bom_failure_nulls_fire_danger():
    with patch("app.services.fire._fetch_url") as mock_fetch:
        def side_effect(url, timeout=10):
            if "bom.gov.au" in url:
                raise Exception("BOM down")
            return SAMPLE_XML
        mock_fetch.side_effect = side_effect
        result = fetch_fire_data()
    assert result.get("North Central", {}).get("fire_danger") is None
    assert result.get("North Central", {}).get("total_fire_ban") is True


def test_fetch_fire_data_cfa_failure_defaults_tfb_false():
    with patch("app.services.fire._fetch_url") as mock_fetch:
        def side_effect(url, timeout=10):
            if "cfa.vic.gov.au" in url:
                raise Exception("CFA down")
            return BOM_SAMPLE_XML
        mock_fetch.side_effect = side_effect
        result = fetch_fire_data()
    assert result["Central"]["total_fire_ban"] is False
    assert result["Central"]["fire_danger"][0].index == 34


def test_fetch_fire_data_returns_empty_on_network_error():
    with patch("app.services.fire.urllib.request.urlopen", side_effect=Exception("Network error")):
        result = fetch_fire_data()
    assert result == {}


def test_fetch_fire_data_returns_empty_on_malformed_xml():
    mock_response = MagicMock()
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)
    mock_response.read = MagicMock(return_value=b"not xml at all <<<")
    with patch("app.services.fire.urllib.request.urlopen", return_value=mock_response):
        result = fetch_fire_data()
    assert result == {}
