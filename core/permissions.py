from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class IsSelfMixin(UserPassesTestMixin):
    def get_object_for_permission(self):
        if not hasattr(self, "_obj"):
            self._obj = self.get_object()
        return self._obj

    def test_func(self):
        obj = self.get_object_for_permission()
        return obj.pk == self.request.user.pk