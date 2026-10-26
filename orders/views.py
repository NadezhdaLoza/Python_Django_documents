from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .models import TransferOrder
from .forms import TransferOrderForm, TransferOrderItemFormSet


class OrderListView(ListView):
    model = TransferOrder
    template_name = 'orders/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return TransferOrder.objects.select_related('organization').order_by('-document_date')


class OrderCreateView(SuccessMessageMixin, CreateView):
    model = TransferOrder
    form_class = TransferOrderForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:list')
    success_message = "Приказ успешно создан"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TransferOrderItemFormSet(self.request.POST)
        else:
            context['formset'] = TransferOrderItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class OrderUpdateView(SuccessMessageMixin, UpdateView):
    model = TransferOrder
    form_class = TransferOrderForm
    template_name = 'orders/edit.html'
    success_url = reverse_lazy('orders:list')
    success_message = "Изменения сохранены"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TransferOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = TransferOrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))


class OrderDeleteView(DeleteView):
    model = TransferOrder
    success_url = reverse_lazy('orders:list')
    template_name = 'orders/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить: приказ используется.')
            return HttpResponseRedirect(self.success_url)


class OrderDetailView(DetailView):
    model = TransferOrder
    template_name = 'orders/views.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related(
            'employee', 'old_department', 'new_department', 'old_position', 'new_position'
        )
        context['current_date'] = timezone.localdate()
        return context