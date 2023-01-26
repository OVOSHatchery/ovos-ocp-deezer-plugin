from ovos_plugin_manager.templates.ocp import OCPStreamExtractor
from ovos_utils.log import LOG
import deezeridu
import os
from tempfile import gettempdir


class OCPDeezerExtractor(OCPStreamExtractor):

    def __init__(self, ocp_settings=None, deezer=None):
        super().__init__(ocp_settings)
        self.deezer = deezer or deezeridu.Deezer()
        self.settings = self.ocp_settings.get("deezer", {})

    @property
    def supported_seis(self):
        """
        skills may return results requesting a specific extractor to be used

        plugins should report a StreamExtractorIds (sei) that identifies it can handle certain kinds of requests

        any streams of the format "{sei}//{uri}" can be handled by this plugin
        """
        return ["deezer"]

    def validate_uri(self, uri):
        """ return True if uri can be handled by this extractor, False otherwise"""
        return any([uri.startswith(sei) for sei in self.supported_seis]) or \
               self.is_deezer(uri)

    def extract_stream(self, url, video=True):
        """ return the real uri that can be played by OCP """
        path = self.settings.get("path") or os.path.join(gettempdir(), "deezer")
        os.makedirs(path, exist_ok=True)
        try:
            t = self.deezer.download(url, output_dir=path, recursive_quality=True)
            track_info = t.track_info
            track_info["uri"] = "file://" + t.song_path
            track_info["image"] = "file://" + t.image_path
            return track_info
        except Exception as e:
            LOG.error(e)
            return {}

    @staticmethod
    def is_deezer(url):
        if not url:
            return False
        return "deezer." in url


