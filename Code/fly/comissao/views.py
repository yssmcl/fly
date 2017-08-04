from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.utils import timezone

from .models import Comissao, Comissao_Docente
from docente.models import Docente
from .forms import ComissaoForm, Comissao_DocenteFormSet
from base.utils import parse_locale_date

class NovaComissao(LoginRequiredMixin, View):
    def get(self, request):
        main_form = ComissaoForm(prefix='main')
        membros_formset = Comissao_DocenteFormSet(prefix='membros')

        membros_formset.can_delete = False

        return render(request, 'comissao/comissao_form.html', {'main_form': main_form, 'membros_formset': membros_formset})

    def post(self, request):
        main_form = ComissaoForm(request.POST, prefix='main')

        comissao = main_form.instance

        membros_formset = Comissao_DocenteFormSet(request.POST, instance=comissao, prefix='membros')

        if (main_form.is_valid()
                and membros_formset.is_valid()):

            with transaction.atomic():
                main_form.save()
                membros_formset.save()

            return redirect('comissao:consulta')

        else:
            membros_formset.can_delete = False

            return render(request, 'comissao/comissao_form.html', {'main_form': main_form, 'membros_formset': membros_formset})


class ConsultaComissao(LoginRequiredMixin, generic.ListView):
    model = Comissao

    def get_queryset(self):
        d = {}

        if 'periodo' in self.request.GET:
            if self.request.GET['periodo']:
                periodo = parse_locale_date(self.request.GET['periodo'])
                d['inicio__lte'] = periodo
                d['fim__gt'] = periodo
        else:
            d['inicio__lte'] = timezone.now()
            d['fim__gt'] = timezone.now()

        return Comissao.objects.filter(**d)


class DetalheComissao(LoginRequiredMixin, View):
    def get(self, request, pk):
        comissao = get_object_or_404(Comissao, pk=pk)

        main_form = ComissaoForm(instance=comissao, prefix='main')
        membros_formset = Comissao_DocenteFormSet(instance=comissao, prefix='membros')

        return render(request, 'comissao/comissao_form.html', {'main_form': main_form, 'membros_formset': membros_formset})

    def post(self, request, pk):
        comissao = get_object_or_404(Comissao, pk=pk)

        main_form = ComissaoForm(request.POST, instance=comissao, prefix='main')
        membros_formset = Comissao_DocenteFormSet(request.POST, instance=comissao, prefix='membros')

        if (main_form.is_valid()
                and membros_formset.is_valid()):

            with transaction.atomic():
                main_form.save()
                membros_formset.save()

            return redirect('comissao:consulta')

        else:
            return render(request, 'comissao/comissao_form.html', {'main_form': main_form, 'membros_formset': membros_formset})
