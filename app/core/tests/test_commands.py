from unittest.mock import patch  # helper for mocking data

from django.core.management import call_command  # helper for calling mc in test
from django.db.utils import OperationalError  # error that is raised if db is not operational
from django.test import TestCase


class CommandTests(TestCase):

    @patch('django.db.utils.ConnectionHandler.__getitem__', return_value=True)
    def test_wait_for_db_ready(self, gi):
        """ Test waiting for db when db is operational """

        call_command('wait_for_db')
        self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """ Test waiting for db 5 times, success on 6th time """

        # mocking time sleep with return value of True will avoid waiting in our test
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            #  setup side effect: first 5 calls will raise Operationalerror; 6th returns
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
