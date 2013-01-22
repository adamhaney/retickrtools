import unittest


class TestNetworkFunctions(unittest.TestCase):

    def setUp(self):
        self.url = "http://www.google.com"

        # The following url will give you simpler output. If you are debugging
        # these tests you may want to uncomment the following line to get more
        # readable print outs of responses
        #self.url = "http://simile.mit.edu/crowbar/test.html"

        self.user_agents = [
            ("Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) "
             "AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 "
             "Mobile/10A5376e Safari/8536.25"),

            ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) "
             "AppleWebKit/537.17 (KHTML, like Gecko) "
             "Chrome/24.0.1309.0 Safari/537.17"),
        ]

    def test_multi_ua_get(self):
        url = self.url
        user_agents = self.user_agents

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, user_agents)

        # Make sure we have 2 responses
        self.assertEqual(len(responses), 2)

        # Make sure the full user agent string is associated with each response
        self.assertEqual(responses[0][0], user_agents[0])
        self.assertEqual(responses[1][0], user_agents[1])

        # Make sure the responses are not empty
        self.assertTrue(len(responses[0][1]))
        self.assertTrue(len(responses[1][1]))

    def test_multi_ua_get_bad_url(self):
        """
        Verify that we gracefully handle a bad url.
        """
        url = "frob.noz"
        user_agents = self.user_agents

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, self.user_agents)

        # Make sure we have 2 responses
        self.assertEqual(len(responses), 2)

        # Make sure the full user agent string is associated with each response
        self.assertEqual(responses[0][0], user_agents[0])
        self.assertEqual(responses[1][0], user_agents[1])

        # Responses will be empty
        self.assertTrue(len(responses[0][1]) is 0)
        self.assertTrue(len(responses[1][1]) is 0)

    def test_multi_ua_get_bad_ua(self):
        """
        Verify that we handle a bogus ua gracefully
        """
        url = self.url
        user_agents = self.user_agents
        user_agents[0] = "kwatz!"

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, user_agents)

        # Make sure we have 2 responses
        self.assertEqual(len(responses), 2)

        # Make sure the full user agent string is associated with each response
        self.assertEqual(responses[0][0], user_agents[0])
        self.assertEqual(responses[1][0], user_agents[1])

        # Make sure the responses are not empty
        self.assertTrue(len(responses[0][1]))
        self.assertTrue(len(responses[1][1]))

    def test_multi_ua_get_empty_url(self):
        """
        Verify that we gracefully handle an empty url
        """
        url = ""
        user_agents = self.user_agents

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, user_agents)

        # We supplied no url, so we do no requests. In this case the list of ua
        # responses is empty.
        self.assertEqual(len(responses), 0)

    def test_multi_ua_get_empty_ua(self):
        """
        Verify that we gracefully handle an empty user agent
        """
        url = self.url
        user_agents = self.user_agents
        user_agents[0] = ""

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, user_agents)

        # Make sure we have 2 responses
        self.assertEqual(len(responses), 2)

        # Make sure the full user agent string is associated with each response
        self.assertEqual(responses[0][0], user_agents[0])
        self.assertEqual(responses[1][0], user_agents[1])

        # Make sure the responses are not empty
        self.assertTrue(len(responses[0][1]))
        self.assertTrue(len(responses[1][1]))

    def test_multi_ua_get_empty_ua_list(self):
        """
        Verify that we gracefully handle an empty user agent list
        """
        url = self.url
        user_agents = []

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, user_agents)

        # We supplied no user agent strings. We handle this as if the user
        # supplied only a single empty user agent string
        self.assertEqual(len(responses), 1)

        # The request was done with an empty user agent
        self.assertEqual(responses[0][0], '')

        # We should still have a response
        self.assertTrue(len(responses[0][1]))

    def test_multi_ua_get_timeout(self):
        """
        Verify that we gracefully handle a timeout
        """
        url = self.url
        user_agents = self.user_agents

        from retickrtools.network import multi_ua_get
        responses = multi_ua_get(url, user_agents, timeout=0)

        # Make sure we have 2 responses
        self.assertEqual(len(responses), 2)

        # Make sure the full user agent string is associated with each response
        self.assertEqual(responses[0][0], user_agents[0])
        self.assertEqual(responses[1][0], user_agents[1])

        self.assertTrue(len(responses[0][1]) is 0)
        self.assertTrue(len(responses[1][1]) is 0)

if '__main__' == __name__:
    unittest.main()
