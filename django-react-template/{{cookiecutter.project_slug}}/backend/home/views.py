from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HeroSection, CallToAction
from .serializers import HeroSectionSerializer, CallToActionSerializer


class HomepageView(APIView):
    def get(self, request):
        hero = HeroSection.objects.first()  # supõe 1 só
        hero_data = HeroSectionSerializer(hero).data if hero else None

        ctas = CallToAction.objects.all()
        ctas_data = CallToActionSerializer(ctas, many=True).data

        return Response({"hero": hero_data, "ctas": ctas_data})
