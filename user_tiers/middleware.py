# TODO: Implement middleware enforcing User Tiers
class TiersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     # process_view() is called just before Django calls the view.
    #     pass
    #
    # def process_exception(self, request, exception):
    #     # Django calls process_exception() when a view raises an exception
    #     pass
    #
    # def process_template_response(self, request, response):
    #     # process_template_response() is called just after the view has finished executing
    #     pass
