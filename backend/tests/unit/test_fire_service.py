"""
Unit tests for fire service.
Tests XML parsing logic in isolation — no network calls made.
"""
import pytest
from unittest.mock import patch, MagicMock

from app.services.fire import parse_fire_xml, fetch_fire_data

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


def test_north_central_has_tfb():
    result = parse_fire_xml(SAMPLE_XML)
    assert result["North Central"]["total_fire_ban"] is True


def test_central_has_no_tfb():
    result = parse_fire_xml(SAMPLE_XML)
    assert result["Central"]["total_fire_ban"] is False


def test_fire_danger_has_4_days():
    result = parse_fire_xml(SAMPLE_XML)
    assert len(result["North Central"]["fire_danger"]) == 4


def test_day_letters_derived_from_title():
    result = parse_fire_xml(SAMPLE_XML)
    days = [d.day for d in result["North Central"]["fire_danger"]]
    assert days == ["T", "F", "S", "S"]


def test_ratings_are_title_cased():
    result = parse_fire_xml(SAMPLE_XML)
    fdr = result["North Central"]["fire_danger"]
    assert fdr[0].rating == "Extreme"
    assert fdr[1].rating == "High"
    assert fdr[2].rating == "Very High"
    assert fdr[3].rating == "Moderate"


def test_low_moderate_hyphen_preserved():
    result = parse_fire_xml(SAMPLE_XML)
    fdr = result["Central"]["fire_danger"]
    assert fdr[3].rating == "Low-Moderate"


def test_index_is_none():
    result = parse_fire_xml(SAMPLE_XML)
    for day in result["North Central"]["fire_danger"]:
        assert day.index is None


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
