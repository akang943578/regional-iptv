import unittest

from build_playlist import build


class BuildPlaylistTest(unittest.TestCase):
    def test_filters_and_deduplicates(self):
        source = """#EXTM3U
#EXTINF:-1 tvg-id="keep.cn" tvg-country="CN",Keep
https://example.com/keep.m3u8
#EXTINF:-1 tvg-id="geo.jp" tvg-country="JP",Geo Ⓖ
https://example.com/geo.m3u8
#EXTINF:-1 tvg-id="shop.us" tvg-country="US",Shopping Channel
https://example.com/shop.m3u8
#EXTINF:-1 tvg-id="other.fr" tvg-country="FR",Other
https://example.com/other.m3u8
#EXTINF:-1 tvg-id="keep.cn" tvg-country="CN",Duplicate
https://example.com/duplicate.m3u8
"""
        playlist, count = build(source)

        self.assertEqual(count, 1)
        self.assertIn("Keep", playlist)
        self.assertNotIn("Geo", playlist)
        self.assertNotIn("Shopping", playlist)
        self.assertNotIn("Other", playlist)
        self.assertNotIn("Duplicate", playlist)


if __name__ == "__main__":
    unittest.main()
