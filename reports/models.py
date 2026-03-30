from django.db import models

# Test report model (entity)
class Report(models.Model):
    #Status "enum"
    STATUS_CHOICES = [
        ('c', "Current"),
        ('a', "Archived"),
    ]

    report_date = models.DateField()
    filepath = models.CharField(max_length=500, unique=True)
    filename = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="c")
    discovered_at = models.DateTimeField(auto_now_add=True)#Auto sets on initial save
    updated_at = models.DateTimeField(auto_now=True)#Auto sets on all saves

    class Meta:
        ordering = ['-report_date', 'filename']

    def __str__(self):
        return f"{self.report_date} - {self.filename} [{self.get_status_display()}]"