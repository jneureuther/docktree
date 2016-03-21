#!/usr/bin/env python

import sys
import unittest

tests = unittest.TestLoader().loadTestsFromNames(
    [
        'test_cli_argparse',
        'test_image_layer'
    ]
)

result = unittest.TextTestRunner(verbosity=1).run(tests)
sys.exit(0 if result.wasSuccessful() else 1)
