import pytest
from unittest.mock import patch
from movie_song_downloader.providers.wikidata_provider import WikidataProvider
from movie_song_downloader.core.database import db


@pytest.mark.asyncio
async def test_wikidata_get_posters_batch():
    await db.run_migrations()
    provider = WikidataProvider()

    # Mock response from Wikidata wbgetentities API
    mock_response = {
        "entities": {
            "Q102147287": {
                "sitelinks": {"enwiki": {"title": "Vikram (2022 film)"}},
                "claims": {
                    "P18": [{"mainsnak": {"datavalue": {"value": "Vikram_poster.jpg"}}}]
                },
            }
        }
    }

    with patch.object(
        provider, "_wikidata_request", return_value=mock_response
    ) as mock_req:
        results = await provider.get_posters_batch(["Vikram (2022 film)"], lang="en")
        assert len(results) == 1
        assert "Vikram (2022 film)" in results
        assert (
            results["Vikram (2022 film)"]
            == "https://commons.wikimedia.org/wiki/Special:FilePath/Vikram_poster.jpg"
        )
        mock_req.assert_called_once()
