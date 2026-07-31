import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock
from friday.tools.web import fetch_and_parse_feed, get_world_news

@pytest.fixture
def sample_xml():
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Sample News</title>
    <item>
      <title>Article 1</title>
      <description>Description 1 &lt;b&gt;bold&lt;/b&gt;</description>
      <link>http://example.com/1</link>
    </item>
    <item>
      <title>Article 2</title>
      <description>Description 2</description>
      <link>http://example.com/2</link>
    </item>
  </channel>
</rss>
"""

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_success(sample_xml):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = sample_xml.encode('utf-8')

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    url = "https://www.bbc.co.uk/news/world/rss.xml"

    results = await fetch_and_parse_feed(mock_client, url)

    assert len(results) == 2
    assert results[0]["source"] == "BBC"
    assert results[0]["title"] == "Article 1"
    assert results[0]["summary"] == "Description 1 bold..."
    assert results[0]["link"] == "http://example.com/1"

    assert results[1]["title"] == "Article 2"
    assert results[1]["summary"] == "Description 2..."

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_error_status():
    mock_response = MagicMock()
    mock_response.status_code = 404

    mock_client = AsyncMock()
    mock_client.get.return_value = mock_response

    results = await fetch_and_parse_feed(mock_client, "https://example.com/rss.xml")
    assert results == []

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_exception():
    mock_client = AsyncMock()
    mock_client.get.side_effect = Exception("Network error")

    results = await fetch_and_parse_feed(mock_client, "https://example.com/rss.xml")
    assert results == []

@pytest.mark.asyncio
@patch("friday.tools.web.fetch_and_parse_feed")
async def test_get_world_news_success(mock_fetch):
    async def mock_fetch_call(client, url):
        return [
            {
                "source": "SRC",
                "title": f"Article from {url}",
                "summary": "Summary...",
                "link": "http://example.com"
            }
        ]
    mock_fetch.side_effect = mock_fetch_call

    result = await get_world_news()

    assert "### GLOBAL NEWS BRIEFING (LIVE)" in result
    assert "Article from" in result

@pytest.mark.asyncio
@patch("friday.tools.web.fetch_and_parse_feed")
async def test_get_world_news_limits_to_12(mock_fetch):
    async def mock_fetch_call(client, url):
        return [
            {
                "source": "SRC",
                "title": f"Article {i}",
                "summary": "Summary...",
                "link": "http://example.com"
            } for i in range(5)
        ]
    mock_fetch.side_effect = mock_fetch_call

    result = await get_world_news()

    assert "### GLOBAL NEWS BRIEFING (LIVE)" in result
    assert result.count("**[") == 12

@pytest.mark.asyncio
@patch("friday.tools.web.fetch_and_parse_feed")
async def test_get_world_news_empty(mock_fetch):
    mock_fetch.return_value = []

    result = await get_world_news()

    assert result == "The global news grid is unresponsive, sir. I'm unable to pull headlines."
