import pytest
import httpx
import asyncio
from unittest.mock import AsyncMock, MagicMock
from friday.tools.web import fetch_and_parse_feed

@pytest.fixture
def mock_client():
    client = MagicMock()
    client.get = AsyncMock()
    return client

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_success(mock_client):
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <rss>
        <channel>
            <item>
                <title>Test Title 1</title>
                <description>&lt;p&gt;Test description 1&lt;/p&gt;</description>
                <link>http://example.com/1</link>
            </item>
            <item>
                <title>Test Title 2</title>
                <description>Test description 2 without tags</description>
                <link>http://example.com/2</link>
            </item>
            <item>
                <title>Test Title 3</title>
                <description></description>
                <link>http://example.com/3</link>
            </item>
            <item>
                <title>Test Title 4</title>
                <link>http://example.com/4</link>
            </item>
            <item>
                <title>Test Title 5</title>
                <description>A very long description that should hopefully be truncated but I actually need it to be more than two hundred characters. Let's keep going to ensure it reaches the limit properly. Wait, it needs to be longer. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.</description>
                <link>http://example.com/5</link>
            </item>
            <item>
                <title>Test Title 6</title>
                <description>Should not be included</description>
                <link>http://example.com/6</link>
            </item>
        </channel>
    </rss>
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = xml_content.encode('utf-8')
    mock_client.get.return_value = mock_response

    url = 'https://www.bbc.co.uk/news'
    result = await fetch_and_parse_feed(mock_client, url)

    assert len(result) == 5

    assert result[0]["source"] == "BBC"
    assert result[0]["title"] == "Test Title 1"
    assert result[0]["summary"] == "Test description 1..."
    assert result[0]["link"] == "http://example.com/1"

    assert result[1]["summary"] == "Test description 2 without tags..."

    assert result[2]["summary"] == ""

    assert result[3]["summary"] == ""

    assert len(result[4]["summary"]) == 203 # 200 chars + "..."
    assert result[4]["summary"].endswith("...")

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_non_200(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client.get.return_value = mock_response

    url = 'https://www.bbc.co.uk/news'
    result = await fetch_and_parse_feed(mock_client, url)

    assert result == []

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_exception(mock_client):
    mock_client.get.side_effect = Exception("Network error")

    url = 'https://www.bbc.co.uk/news'
    result = await fetch_and_parse_feed(mock_client, url)

    assert result == []

@pytest.mark.asyncio
async def test_fetch_and_parse_feed_invalid_xml(mock_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Not XML"
    mock_client.get.return_value = mock_response

    url = 'https://www.bbc.co.uk/news'
    result = await fetch_and_parse_feed(mock_client, url)

    assert result == []
