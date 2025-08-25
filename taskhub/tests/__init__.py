import os
os.environ['TESTING'] = 'True'

import sys
from unittest.mock import MagicMock

sys.modules['rest_framework.views'] = MagicMock()
sys.modules['rest_framework.response'] = MagicMock()
sys.modules['rest_framework.exceptions'] = MagicMock()

sys.modules['rest_framework_simplejwt'] = MagicMock()
sys.modules['rest_framework_simplejwt.authentication'] = MagicMock()