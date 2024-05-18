from madokami.internal.default_plugins.default_requester import DefaultRequester


def test_default_requester():
    requester = DefaultRequester()
    response = requester.request('https://google.com', 'GET')
    assert response.status_code == 200
    assert requester.status == (0, 'Finished')
