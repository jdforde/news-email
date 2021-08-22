import unittest
from src.util import functions as f
import src.util.constants as c

class TestSendRequest(unittest.TestCase):
    
    def testSuccess(self):
        req = f.send_request("https://www.npr.org/", 'NPR')
        self.assertEqual(200, req.status_code)

    def testUnknown(self):
        req = f.send_request("htt://abc.com/", 'ABC')
        self.assertEqual(None, req)
    
    def testHttpError(self):
        req = f.send_request("https://hg92jz78*/", 'junk')
        self.assertEqual(None, req)

class TestComponents(unittest.TestCase):

    def testSuccess(self):
        story_dict = {
        c.STORY_URL: 'url',
        c.STORY_TEXT: 'txt',
        c.STORY_TITLE: 'title',
        c.STORY_CAPTION: 'caption',
        c.STORY_SOURCE: 'src',
        }

        self.assertTrue(f.has_all_components(story_dict))
    
    def testFailure(self):
        story_dict = {
        c.STORY_URL: 'url',
        c.STORY_TITLE: 'title',
        c.STORY_CAPTION: 'caption',
        c.STORY_TEXT: 'txt'
        }
        self.assertFalse(f.has_all_components(story_dict))
    
    def testFailureNotDict(self):
        story_dict = [c.STORY_URL, c.STORY_TITLE, c.STORY_CAPTION, c.STORY_TEXT, c.STORY_SOURCE]
        self.assertFalse(f.has_all_components(story_dict))

class TestReadCache(unittest.TestCase):

    def testFailure(self):
        self.assertEqual(f.read_cache("fakefile.txt"), [])

if __name__ == '__main__':
    unittest.main()
