from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class LoginAndAdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an admin."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        elif not request.user.is_admin:
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)