from helpers import registers_helpers
import json


class TestRegisters:
    def test_ddat_family(self):
        families = registers_helpers.ddat_job_families()
        assert families['Product and Delivery'] == '101'

    def test_get_jobs_in_job_family(self):
        expected_return = {
            'User researcher': '1038',
            'Service designer': '1037'
        }
        assert registers_helpers.get_unique_jobs_in_job_family('106') == expected_return
