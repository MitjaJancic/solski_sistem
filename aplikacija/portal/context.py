from .models import Obvestilo


def obvestila(request):
    """Izpostavi število neprebranih obvestil za prikaz značke v navigaciji."""
    if request.user.is_authenticated:
        return {
            "neprebrana_obvestila": Obvestilo.objects.filter(
                prejemnik=request.user, prebrano=False
            ).count()
        }
    return {"neprebrana_obvestila": 0}
