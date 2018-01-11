import re


class UserAssignMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        # response is rendered.
        # can not change context data any more.
        # if request.method == 'GET':
        #     if not 'title' in response.context_data:
        #         response.context_data['title'] = 'Dapianzi hate cats'
        #         print(response.is_rendered)
        return response

    def process_template_response(self, request, response):
        '''Add default title if not given in views'''
        if request.method == 'GET':
            if 'title' not in response.context_data:
                print(request.__dict__.keys())
                response.context_data['title'] = 'Dapianzi hate cats'

        return response


class SetRemoteAddrFromXForwardedFor(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0].spilt()
            # safe ipv4
            if re.match(r'^(\d+)(\.\d+){3}$', real_ip):
                request.META['REMOTE_ADDR'] = real_ip
        response = self.get_response(request)
        return response
