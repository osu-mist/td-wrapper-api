import logging
import sys
import unittest

import utils


class IntegrationTest(unittest.TestCase):
    # helper funtion: test response time
    def assert_response_time(self, res, max_elapsed_seconds):
        elapsed_seconds = res.elapsed.total_seconds()
        logging.debug(f"Request took {elapsed_seconds} second(s)")

        self.assertLess(elapsed_seconds, max_elapsed_seconds)

    def attributes_checker(self, attributes):
        for redundant_key in ['iD', 'uri']:
            self.assertNotIn(redundant_key, attributes)

        for key in attributes:
            if key.lower().startswith('los'):
                self.assertTrue(key.startswith('los'))
            elif key.lower() == 'sla':
                self.assertTrue(key == 'sla')
            else:
                self.assertTrue(key[0].islower())

    def test_get_services(self):
        res = utils.get_services()

        self.assertIn('data', res.json())
        self.assertIsInstance(res.json()['data'], list)
        self.assert_response_time(res, 3)
        self.assertEqual(res.status_code, 200)
        for data in res.json()['data']:
            self.attributes_checker(data['attributes'])

    def test_get_service_by_valid_id(self):
        valid_id = service_id
        res = utils.get_service_by_id(valid_id)

        self.assertIn('data', res.json())
        self.assertIsInstance(res.json()['data'], dict)
        self.assert_response_time(res, 3)
        self.assertEqual(res.status_code, 200)
        self.attributes_checker(res.json()['data']['attributes'])

    def test_get_service_by_invalid_id(self):
        invalid_id = 'invalid_id'
        res = utils.get_service_by_id(invalid_id)

        self.assert_response_time(res, 2)
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    args, argv = utils.parse_args()
    config_data = utils.load_config(args.config)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)

    service_id = config_data['service_id']

    sys.argv[:] = argv
    unittest.main()
