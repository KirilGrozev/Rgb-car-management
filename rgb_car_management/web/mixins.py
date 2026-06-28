from django.contrib.auth.mixins import AccessMixin
from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy

from rgb_car_management.web.forms import AcceptedCarForm, IssuedCarForm, CarIssueForm
from rgb_car_management.web.models import AcceptedCar, CarIssue, CarIssueCategory, IssuedCar


class SearchMixin:
    search_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')

        if search_query and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': search_query})
            queryset = queryset.filter(q_objects)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
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

    def build_formset(self):
        extra = 0 if getattr(self, 'object', None) else 1
        FormSet = modelformset_factory(CarIssue, form=CarIssueForm, extra=extra, can_delete=True)
        data = self.request.POST if self.request.method == 'POST' else None
        fs =  FormSet(data, queryset=self.issue_queryset(), prefix=self.formset_prefix)
        return fs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('formset', self.build_formset())
        context['other_category_ids'] = list(
            CarIssueCategory.objects.filter(is_other=True).values_list('id', flat=True))
        return context

    def form_valid(self, form):
        formset = self.build_formset()
        if not (form.is_valid() and formset.is_valid()):
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        with transaction.atomic():
            self.object = form.save()
            formset.save()
            kept = [f.instance for f in formset.forms if f.instance.pk and f not in formset.deleted_forms]
            getattr(self.object, self.m2m_field).set(kept)
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
