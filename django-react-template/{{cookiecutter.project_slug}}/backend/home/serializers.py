from rest_framework import serializers
from .models import HeroSection, Feature, CallToAction


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "icon", "text"]


class HeroSectionSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = HeroSection
        fields = ["id", "title", "subtitle", "background_image", "features"]


class CallToActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallToAction
        fields = ["id", "label", "url"]
