import os
import unittest
from unittest.mock import MagicMock, patch

import deepseek_client


class DeepSeekClientTests(unittest.TestCase):
    def test_search_deepseek_success(self):
        previous = os.environ.get('DEEPSEEK_API_KEY')
        self.addCleanup(self._restore_key, previous)
        os.environ['DEEPSEEK_API_KEY'] = 'testkey'

        mock_response = MagicMock()
        mock_response.json.return_value = {'results': [1]}
        mock_response.raise_for_status.return_value = None
        mock_session = MagicMock()
        mock_session.__enter__.return_value = mock_session
        mock_session.post.return_value = mock_response

        with patch('deepseek_client.requests.Session', return_value=mock_session):
            result = deepseek_client.search_deepseek('some query')

        self.assertEqual(result, {'results': [1]})
        mock_session.post.assert_called_once()

    def test_missing_key_raises(self):
        previous = os.environ.get('DEEPSEEK_API_KEY')
        self.addCleanup(self._restore_key, previous)
        os.environ.pop('DEEPSEEK_API_KEY', None)
        with self.assertRaises(RuntimeError):
            deepseek_client._get_api_key(None)

    @staticmethod
    def _restore_key(previous):
        if previous is None:
            os.environ.pop('DEEPSEEK_API_KEY', None)
        else:
            os.environ['DEEPSEEK_API_KEY'] = previous


if __name__ == '__main__':
    unittest.main()
