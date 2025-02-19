import os
from typing import Optional

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.views.decorators.http import require_http_methods
from google import genai

from footprint.Schema import CarbonFootprintResponse
from footprint.forms import CarbonFootprintForm, RegisterForm
from footprint.models import UserCarbonFootprint

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def home(request):
    template = get_template("home.html")
    return HttpResponse(template.render(request=request))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    template = get_template("register.html")
    context = {'form': form}
    return HttpResponse(template.render(context=context, request=request))


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    context = {'form': form}
    template = get_template("login.html")
    return HttpResponse(template.render(context=context, request=request))


def user_logout(request):
    logout(request)
    template = get_template("logout.html")
    return HttpResponse(template.render(request=request))


def extract_carbon_footprint(prompt: str) -> CarbonFootprintResponse:
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': CarbonFootprintResponse,
        },
    )

    # noinspection PyTypeChecker
    return response.parsed


@login_required
def index(request):
    result: Optional[CarbonFootprintResponse] = None

    if request.method == "POST":
        form = CarbonFootprintForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            result = extract_carbon_footprint(prompt)
            m = UserCarbonFootprint.objects.create(user=request.user, json_data=result.model_dump())
            m.save()
    else:
        form = CarbonFootprintForm()

    template = get_template("footprint/index.html")
    context = {
        'form': form,
        'result': result
    }
    return HttpResponse(template.render(context, request))


@login_required
def dashboard(request):
    user_reports = UserCarbonFootprint.objects.filter(user=request.user)

    # Parse JSON data
    reports = []
    for report in user_reports:
        json_data = CarbonFootprintResponse.model_validate(obj=report.json_data, strict=True)
        formatted_date = report.created_at.strftime("%Y-%m-%d %H:%M")

        if json_data.valid_data_provided:
            reports.append({
                "pk": report.pk,
                "created_at": formatted_date,
                "total_emissions": json_data.total_emissions.value if json_data.total_emissions else None,
                "transportation": json_data.transportation.value if json_data.transportation else None,
                "energy": json_data.energy.value if json_data.energy else None,
                "diet": json_data.diet.value if json_data.diet else None,
                "other": json_data.other.value if json_data.other else None,
                "reasons": {
                    "total": json_data.total_emissions.reason if json_data.total_emissions else None,
                    "transportation": json_data.transportation.reason if json_data.transportation else None,
                    "energy": json_data.energy.reason if json_data.energy else None,
                    "diet": json_data.diet.reason if json_data.diet else None,
                    "other": json_data.other.reason if json_data.other else None,
                },
                "recommendations": json_data.recommendations or None,
            })

    template = get_template("dashboard.html")
    context = {"reports": reports}
    return HttpResponse(template.render(context, request))


@login_required
@require_http_methods(["DELETE"])
def delete_footprint_json(request, pk):
    u = get_object_or_404(UserCarbonFootprint, pk=pk)

    if u.user != request.user:
        raise PermissionDenied("You do not have permission to delete this.")

    u.delete()
    return JsonResponse({}, status=204)
