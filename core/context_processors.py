from django.db.models import Sum
from progress.models import PointsEvent

def user_points(request):
    if request.user.is_authenticated:
        total = PointsEvent.objects.filter(user=request.user).aggregate(s=Sum("points"))["s"] or 0
        return {"USER_POINTS": total}
    return {"USER_POINTS": 0}
