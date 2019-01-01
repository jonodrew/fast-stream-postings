import requests


def ddat_job_families():
    endpoint = "https://ddat-profession-capability-framework-job-family.register.gov.uk/records.json?page-size=5000"
    with requests.get(endpoint) as url:
        data = url.json()
        return {data[key]['item'][0]['name']: key for key in data.keys()}


def _get_record_from_key(host, key):
    return requests.get("https://{host}.register.gov.uk/records/{key}.json".format(host=host, key=key)).json()


def get_unique_jobs_in_job_family(job_family_key):
    """
    This function returns a dictionary of role titles and their unique keys
    :param job_family_key: a string key that represents a job family
    :return: Dict
    """
    key = "profession-capability-framework-job-family/ddat-profession-capability-framework-job-family:{}".format(job_family_key)
    all_jobs = _get_record_from_key("ddat-profession-capability-framework", key=key)
    role_keys = {
        _attribute_from_response(all_jobs, key, 'profession-capability-framework-role').split(':')[1] for key in all_jobs.keys()
                 }
    return {
        _attribute_from_response(
            _get_record_from_key("ddat-profession-capability-framework-role", key), key, 'name'): key
        for key in role_keys
    }


def _attribute_from_response(json_response, key, attribute_name):
    return json_response.get(key)['item'][0][attribute_name]
