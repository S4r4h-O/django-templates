from django.db import models


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="hero/", blank=True, null=True)

    def __str__(self):
        return self.title


class Feature(models.Model):
    hero = models.ForeignKey(
        HeroSection, related_name="features", on_delete=models.CASCADE
    )
    icon = models.CharField(max_length=50)  # pode ser nome de ícone frontend
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class CallToAction(models.Model):
    label = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.label
