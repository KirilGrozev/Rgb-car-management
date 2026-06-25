from django.contrib.auth.mixins import AccessMixin
from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from flask import redirect

from rgb_car_management.web.forms import AcceptedCarForm, IssuedCarForm, CarIssueForm
from rgb_car_management.web.models import AcceptedCar, CarIssue, CarIssueCategory, IssuedCar


class SearchMixin:
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')

        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': search_query})
            queryset = queryset.filter(q_objects)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['clear_url'] = self.request.path
        return context


class StaffOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Exception('Нямаш достъп до тази страница!')
        return super().dispatch(request, *args, **kwargs)


class CarIssueFormSetMixin:
    m2m_field = None
    formset_prefix = None

    def issue_queryset(self):
        if getattr(self, 'object', None):
            return getattr(self.object, self.m2m_field).all()
        return CarIssue.objects.none()

    def build_fromset(self, data=None):
        FormSet = modelformset_factory(CarIssue, form=CarIssueForm, extra=1, can_delete=True)
        data = self.request.POST if self.request.method == 'POST' else None
        return FormSet(data, queryset=self.issue_queryset(), prefix=self.formset_prefix)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('issues', self.build_fromset())
        context['other_category_ids'] = list(
            CarIssueCategory.objects.filter(is_other=True).values_list('id', flat=True))
        return context

    def form_valid(self, form):
        formset = self.build_fromset()
        if not (form.is_valid() and formset.is_valid()):
            return self.render_to_response(self.get_context_data(form=form, issues=formset))
        with transaction.atomic():
            self.object = form.save()
            formset.save()
            kept = [f.instance for f in formset.forms if f.instance.pk and f not in formset.deleted_forms]
            self.object.issues.set(kept)
        return redirect(self.get_success_url())


class AcceptedCarFormMixin(CarIssueFormSetMixin):
    model = AcceptedCar
    form_class = AcceptedCarForm
    template_name = 'accepted_car_actions.html'
    success_url = reverse_lazy('accepted cars')
    m2m_field = 'issues'
    formset_prefix = 'issues'


class IssuedCarFormMixin(CarIssueFormSetMixin):
    model = IssuedCar
    form_class = IssuedCarForm
    template_name = 'issued_car_actions.html'
    success_url = reverse_lazy('issued cars')
    m2m_field = 'repairs'
    formset_prefix = 'repairs'
