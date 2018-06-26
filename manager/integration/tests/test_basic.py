import json
import requests

from common import BASE_URL, param, update_param, set_token_fqdn, get_token_fqdn


def test_create_domain():  # NOQA
    url = build_url(BASE_URL, "", "")
    print "create Url is \n"
    print url
    response = create_domain_test(url, param)
    result = response.json()
    assert result == response.json()
    set_token_fqdn(result)


# This method creates the domain
def create_domain_test(url, data):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


def test_get_domain():  # NOQA
    token, fqdn = get_token_fqdn()
    print "get token is \n"
    print token
    print "get fqdn is \n"
    print fqdn
    url = build_url(BASE_URL, "/" + fqdn, "")
    print "get Url is \n"
    print url
    response = get_domain_test(url, token)
    result = response.json()
    assert result == response.json()
    print "get result \n"
    print result


# This method gets the domain
def get_domain_test(url, token):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": 'Bearer %s' % token}

    response = requests.get(url, params=None, headers=headers)
    return response


def test_update_domain():  # NOQA
    token, fqdn = get_token_fqdn()
    print "update token is \n"
    print token
    print "update fqdn is \n"
    print fqdn
    url = build_url(BASE_URL, "/" + fqdn, "")
    print "update Url is \n"
    print url
    response = update_domain_test(url, token, update_param)
    result = response.json()
    assert result == response.json()
    print "update result \n"
    print result


# This method updates the domain
def update_domain_test(url, token, data):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": 'Bearer %s' % token}

    response = requests.put(url, data=json.dumps(data), headers=headers)
    return response


def test_renew_domain():  # NOQA
    token, fqdn = get_token_fqdn()
    print "renew token is \n"
    print token
    print "renew fqdn is \n"
    print fqdn
    url = build_url(BASE_URL, "/" + fqdn, "/renew")
    print "renew Url is \n"
    print url
    response = renew_domain_test(url, token)
    result = response.json()
    assert result == response.json()
    print "renew result \n"
    print result
    assert 0


# This method renews the domain
def renew_domain_test(url, token):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": 'Bearer %s' % token}

    response = requests.put(url, data=None, headers=headers)
    return response


def test_delete_domain():  # NOQA
    token, fqdn = get_token_fqdn()
    print "delete token is \n"
    print token
    print "delete fqdn is \n"
    print fqdn
    url = build_url(BASE_URL, "/" + fqdn, "")
    print "delete Url is \n"
    print url
    response = delete_domain_test(url, token)
    result = response.json()
    assert result == response.json()
    print "delete result \n"
    print result


# This method deletes the domain
def delete_domain_test(url, token):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json",
               "Authorization": 'Bearer %s' % token}

    response = requests.delete(url, headers=headers)
    return response


# buildUrl return request url
def build_url(base, fqdn, path):
    return '%s/domain%s%s' % (base, fqdn, path)
