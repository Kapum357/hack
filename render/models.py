from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FloodThreat(models.Model):
    """Model for storing flood threat areas"""
    
    THREAT_LEVEL_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    threat_level = models.CharField(
        max_length=50, 
        choices=THREAT_LEVEL_CHOICES,
        default='MEDIUM'
    )
    geometry = models.MultiPolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Flood Threat"
        verbose_name_plural = "Flood Threats"

    def __str__(self):
        return f"{self.name} ({self.threat_level})"


class SocialVulnerability(models.Model):
    """Model for storing social vulnerability areas"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    vulnerability_index = models.FloatField(
        help_text="Vulnerability index from 0 to 1",
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ]
    )
    affected_population = models.IntegerField(
        default=0,
        help_text="Estimated affected population",
        validators=[MinValueValidator(0)]
    )
    linked_families = models.IntegerField(
        default=0,
        help_text="Number of families linked to Red Cross programs",
        validators=[MinValueValidator(0)]
    )
    geometry = models.MultiPolygonField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Vulnerability"
        verbose_name_plural = "Social Vulnerabilities"

    def __str__(self):
        return f"{self.name} (Index: {self.vulnerability_index})"
