from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from django.http import JsonResponse

from .models import Government, GovernmentOfficial, Party, Politician, GovernmentParty, PoliticsParty


def parties_page(request):
    parties = (
        Party.objects.prefetch_related(
            Prefetch(
                'politicsparty_set',
                queryset=PoliticsParty.objects.select_related('politician').order_by(
                    'politician__surname',
                    'politician__name',
                    'start_of_membership',
                ),
            )
        )
        .all()
        .order_by('name')
    )
    context = {
        'page_title': 'Politické strany',
        'parties': parties,
    }
    return render(request, 'politicians/parties.html', context)


def politicians_page(request):
    politicians = Politician.objects.all().order_by('surname', 'name')
    context = {
        'page_title': 'Politici',
        'politicians': politicians,
    }
    return render(request, 'politicians/politicians.html', context)


def politician_detail_json(request, pk):
    try:
        p = Politician.objects.get(pk=pk)
    except Politician.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    # party memberships
    memberships = []
    for m in PoliticsParty.objects.select_related('party').filter(politician=p).order_by('start_of_membership'):
        party = m.party
        leader_name = (party.leader or '').strip()
        is_leader = leader_name == f"{p.name} {p.surname}" or leader_name == p.surname
        memberships.append({
            'party': party.name,
            'start_of_membership': m.start_of_membership.isoformat(),
            'end_of_membership': m.end_of_membership.isoformat() if m.end_of_membership else None,
            'is_leader': is_leader,
        })

    # government posts
    posts = []
    for g in GovernmentOfficial.objects.select_related('government', 'office', 'party').filter(politician=p).order_by('-start_of_term'):
        posts.append({
            'government_id': g.government.id,
            'government_in_function': g.government.in_function.isoformat(),
            'prime_minister': g.government.prime_minister,
            'office': g.office.name,
            'role': g.role,
            'start_of_term': g.start_of_term.isoformat(),
            'end_of_term': g.end_of_term.isoformat() if g.end_of_term else None,
            'party': g.party.name if g.party else None,
        })

    data = {
        'id': p.pk,
        'name': p.name,
        'surname': p.surname,
        'title': p.title,
        'age': p.age,
        'photo_url': p.photo_file.url if p.photo_file else None,
        'memberships': memberships,
        'government_posts': posts,
    }
    return JsonResponse(data)


def governments_page(request):
    governments = (
        Government.objects.prefetch_related(
            Prefetch(
                'governmentparty_set',
                queryset=GovernmentParty.objects.select_related('party').order_by('party__name'),
            )
        )
        .all()
        .order_by('-in_function')
    )
    context = {
        'page_title': 'Vlády',
        'governments': governments,
    }
    return render(request, 'politicians/governments.html', context)


def government_officials_page(request):
    officials = (
        GovernmentOfficial.objects.select_related('government', 'politician', 'party', 'office')
        .all()
        .order_by('-start_of_term')
    )
    context = {
        'page_title': 'Vládní funkcionáři',
        'officials': officials,
    }
    return render(request, 'politicians/government_officials.html', context)


class SiteLoginView(LoginView):
    template_name = 'politicians/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Přihlášení'
        context['next_url'] = self.request.GET.get('next') or self.request.POST.get('next') or ''
        return context

    def get_success_url(self):
        return self.get_redirect_url() or super().get_success_url()


def register_page(request):
    if request.user.is_authenticated:
        return redirect('politicians:parties')
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(next_url or 'politicians:parties')
    else:
        form = UserCreationForm()
    return render(request, 'politicians/register.html', {'page_title': 'Registrace', 'form': form, 'next_url': next_url})


class PartyUpdateView(PermissionRequiredMixin, UpdateView):
    model = Party
    fields = ['name', 'founding', 'leader', 'photo_file']
    template_name = 'politicians/edit_form.html'
    permission_required = 'politicians.change_party'
    success_url = reverse_lazy('politicians:parties')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Upravit stranu'
        return context


class PoliticianUpdateView(PermissionRequiredMixin, UpdateView):
    model = Politician
    fields = ['name', 'surname', 'title', 'age', 'photo_file']
    template_name = 'politicians/edit_form.html'
    permission_required = 'politicians.change_politician'
    success_url = reverse_lazy('politicians:politicians')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Upravit politika'
        return context


class GovernmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Government
    fields = ['in_function', 'prime_minister']
    template_name = 'politicians/edit_form.html'
    permission_required = 'politicians.change_government'
    success_url = reverse_lazy('politicians:governments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Upravit vládu'
        return context


class GovernmentOfficialUpdateView(PermissionRequiredMixin, UpdateView):
    model = GovernmentOfficial
    fields = ['government', 'politician', 'party', 'office', 'role', 'start_of_term', 'end_of_term']
    template_name = 'politicians/edit_form.html'
    permission_required = 'politicians.change_governmentofficial'
    success_url = reverse_lazy('politicians:government_officials')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Upravit vládního funkcionáře'
        return context
