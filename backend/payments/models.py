import uuid

from django.db import models


class Payment(models.Model):
    """
    Represents the 'Payment' step: order summary -> payment method -> confirm.
    On success, the linked Booking moves from 'pending' to 'confirmed'.
    No real payment gateway is integrated — this simulates success/failure,
    which is standard for a portfolio-scope project.
    """

    METHOD_CHOICES = (
        ("card", "Credit/Debit Card"),
        ("upi", "UPI"),
        ("wallet", "Wallet"),
    )
    STATUS_CHOICES = (
        ("success", "Success"),
        ("failed", "Failed"),
    )

    booking = models.OneToOneField("bookings.Booking", related_name="payment", on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=40, unique=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="success")
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
