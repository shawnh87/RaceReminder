from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .modules.view_construct import get_location, BikeRegCall, run_date


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)

        if u_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}. You may now login!')
            return redirect('br_email_profile')
    else:
        u_form = UserRegisterForm()

    context = {
            'u_form': u_form
        }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):

    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dist = {7: 'Weekly', 14: 'BiWeekly', 28: 'Monthly'}
            dstr_day = int(p_form.cleaned_data.get('dstr_day'))
            dstr_cad = int(p_form.cleaned_data.get('dstr_cad'))
            u_form.save()

            current_user = request.user
            
            event_call = BikeRegCall(form=p_form, user= current_user)
            params = event_call.get_q_string_dat()
            event_call.build_q_string(params)
            event_call.get_events()

            profile_update = p_form.save(commit=False)

            zip_cd = p_form.cleaned_data.get('zip')
            profile_update.location = get_location(zip_cd)
            profile_update.q_string = event_call.url 
            profile_update.run_date = run_date(dstr_day, dstr_cad)
            profile_update.save()
            p_form.save_m2m()

            messages.success(
               request,
               f'Your distribution settings have been updated. Distribution will be {dist[dstr_cad]} on {day[dstr_day]}s.')

            return redirect('br_email_events')
        else:
            messages.error(request,
                           "Please use at least one of the following options: distance from zip, state, or region.")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(
             instance=request.user.profile,
             initial=
                    {'event': [event for event in request.user.profile.event.all().values_list('id', flat=True)],
                     'states': [state for state in request.user.profile.states.all().values_list('id', flat=True)],
                     'region': [region for region in request.user.profile.region.all().values_list('id', flat=True)]
                    }
                              )
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
