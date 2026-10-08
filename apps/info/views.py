from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Tblinfo


# PAGE
@login_required(login_url='login')
def info_list_page(request):
    query = request.GET.get('q', '').strip()

    infos = Tblinfo.objects.all().order_by('-created_at')

    if query:
        infos = infos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(status__icontains=query)
        )

    paginator = Paginator(infos, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'info/list.html', {
        'infos': page_obj,
        'query': query,
    })


# GET SINGLE (AJAX)
@login_required(login_url='login')
def info_get_ajax(request, pk):
    info = get_object_or_404(Tblinfo, pk=pk)
    return JsonResponse({
        "id":          info.id,
        "title":       info.title,
        "description": info.description,
        "status":      info.status,
    })


# CREATE / UPDATE (AJAX)
@login_required(login_url='login')
@require_POST
def info_save_ajax(request):
    info_id = request.POST.get("id")

    if info_id:
        info = get_object_or_404(Tblinfo, pk=info_id)
    else:
        info = Tblinfo()

    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    status = request.POST.get("status", "active")

    if not title:
        return JsonResponse({"error": "Title is required."}, status=400)
    if len(title) > 150:
        return JsonResponse({"error": "Title must not exceed 150 characters."}, status=400)
    if status not in ('active', 'inactive'):
        return JsonResponse({"error": "Invalid status."}, status=400)

    info.title = title
    info.description = description
    info.status = status
    info.save()

    return JsonResponse({
        "status":      "success",
        "id":          info.id,
        "title":       info.title,
        "description": info.description,
        "status":      info.status,
    })


# DELETE (AJAX)
@login_required(login_url='login')
@require_POST
def info_delete_ajax(request, pk):
    info = get_object_or_404(Tblinfo, pk=pk)
    info.delete()
    return JsonResponse({"status": "deleted"})
