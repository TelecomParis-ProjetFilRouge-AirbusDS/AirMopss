#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import time

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        time.sleep(1)

    def containsThatContains(self, l, s):
        for a in l:
            if s.lower() in a.lower():
                return True
        return False

class MyTests(MyTestCase):
    def testfct(self):
        article = "hello buzz"
        output = "test"
        # output = webapp_getpage.fct(article)
        self.assertEqual(output, [1])

if __name__ == "__main__":
    # https://stackoverflow.com/a/2713010/414272
    log_file = 'test_output.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTests)
    ret = runner.run(suite)
    total = ret.testsRun
    bad = len(ret.failures) + len(ret.errors)
    print("Comment :=>> %d tests failed out of %d total tests" % (bad, total))
    print("Grade :=>> %d" % int(20.*(total-bad)/total))
    f.close()

