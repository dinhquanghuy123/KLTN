from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from slugify import slugify


class Tour(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(
        unique=True,
        blank=True
    )
    destination = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)
    duration = models.PositiveIntegerField(help_text="Số ngày")
    slots = models.PositiveIntegerField(default=10)
    description = models.TextField()
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Tour.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.destination})"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tour')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.tour.name} ({self.rating})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tour')
