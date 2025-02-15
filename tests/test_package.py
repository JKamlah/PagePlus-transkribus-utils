import os
import shutil
import unittest
from pathlib import Path
import pytest

from transkribus_utils import PagePlusTranskribusUtils
from transkribus_utils.mets import get_title_from_mets, replace_img_urls_in_mets
from transkribus_utils.iiif import get_title_from_iiif


file_path = Path(__file__).absolute().parent
CLIENT = ACDHTranskribusUtils()
COL_NAME = "acdh-transkribus-utils"
COL_ID = 190357
METS_URL = "https://viewer.acdh.oeaw.ac.at/viewer/sourcefile?id=AC16292422"
DOC_NAME = "Hesketh Crescent"
SAMPLE_METS = os.path.join(file_path, "sample_mets2.xml")


class TestTestTest(unittest.TestCase):
    """Tests for `acdh_cidoc_pyutils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_smoke(self):
        self.assertEqual(1, 1)

    def test_002_init(self):
        client = CLIENT
        self.assertTrue("http" in client.base_url)

    def test_003_get_or_create_col(self):
        client = CLIENT
        col = client.get_or_create_collection(COL_NAME)
        self.assertEqual(col, COL_ID)

    def test_004_title_from_mets(self):
        title = get_title_from_mets(METS_URL)
        self.assertEqual(title, DOC_NAME)

    def test_005_doc_from_mets(self):
        client = CLIENT
        upload_status = client.upload_mets_file_from_url(METS_URL, COL_ID)
        self.assertFalse(upload_status)

    def test_006_search_document(self):
        client = CLIENT
        result = client.search_for_document(title=DOC_NAME, col_id=COL_ID)
        self.assertTrue(len(result) > 0)

    def test_008_iiif_title(self):
        iiif_url = "https://iiif.onb.ac.at/presentation/ANNO/wrz17500103/manifest/"
        label = get_title_from_iiif(iiif_url)
        self.assertEqual(label, "Wiener Zeitung 1750-01-03")
        iiif_url = "https://iiif.onb.ac.at/presentation/ANNO/wrz17500103/manifestasdf/"
        label = get_title_from_iiif(iiif_url)
        self.assertEqual(label, iiif_url)

    def test_009_filter_cols_by_name(self):
        client = CLIENT
        cols = client.filter_collections_by_name("acdh-transkribus-utils")
        self.assertEqual(len(cols), 1)

    def test_010_create_report(self):
        client = CLIENT
        status = client.create_status_report(
            filter_string="acdh-transkribus-utils", transcription_threshold=1
        )
        self.assertEqual(len(status), 5)

    def test_011_user_id(self):
        client = CLIENT
        user_id = client.get_user_id(client.user)
        self.assertTrue(user_id)

    def test_012_add_user(self):
        client = CLIENT
        status = client.add_user_to_collection(
            client.user, col_id=COL_ID, send_mail=False
        )
        self.assertTrue(f"{190357}" in status)
        self.assertTrue(f"{client.user}" in status)

    def test_013_wrong_credentials(self):
        with pytest.raises(Exception):
            ACDHTranskribusUtils(user="whatever@gmail.com", password="this-wont work")

    def test_014_doc_md(self):
        client = CLIENT
        doc_id = 1351422
        doc_md = client.get_doc_md(doc_id, COL_ID)
        self.assertTrue(doc_md["docId"], doc_id)

    def test_014_get_fulldoc_md(self):
        client = CLIENT
        doc_id = 1351422
        doc_md = client.get_fulldoc_md(doc_id, COL_ID)
        self.assertTrue(doc_md["extra_info"]["nrOfPages"], 10)

    def test_015_save_mets_to_file(self):
        client = CLIENT
        doc_id = 1351422
        f_name = f"{doc_id}_mets.xml"
        try:
            os.remove(f_name)
        except OSError:
            pass
        client.save_mets_to_file(doc_id, COL_ID)
        my_file = Path(f_name)
        self.assertTrue(my_file.is_file())
        os.remove(f_name)

    def test_016_list_documents(self):
        client = CLIENT
        result = client.list_documents(COL_ID)
        self.assertTrue(len(result), 5)

    def test_017_dl_collection(self):
        shutil.rmtree(f"{COL_ID}", ignore_errors=True)
        result = CLIENT.collection_to_mets(COL_ID)
        doc_id = 1351422
        self.assertTrue(doc_id in result)
        my_file = Path(os.path.join(f"{COL_ID}", f"{doc_id}_mets.xml"))
        self.assertTrue(my_file.is_file())
        shutil.rmtree(f"{COL_ID}", ignore_errors=True)
