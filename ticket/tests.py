from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Ticket

# Create your tests here.


class TicketAPITests(APITestCase):
    def test_create_ticket(self):
        payload = {"title": "Login broken", "priority": "high"}
        response = self.client.post(reverse("ticket-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "open")
        self.assertEqual(Ticket.objects.count(), 1)

    def test_stats_counts_by_status(self):
        Ticket.objects.create(title="a", status="open")
        Ticket.objects.create(title="b", status="open")
        Ticket.objects.create(title="c", status="closed")

        response = self.client.get(reverse("ticket-stats"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["open"], 2)
        self.assertEqual(response.data["closed"], 1)
        self.assertEqual(response.data["in_progress"], 0)

    def test_list_filters_by_status_and_paginates(self):
        for i in range(3):
            Ticket.objects.create(title=f"open {i}", status="open")
        Ticket.objects.create(title="done", status="closed")

        response = self.client.get(reverse("ticket-list"), {"status": "open", "page_size": 2})

        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 2)

    def test_patch_updates_status(self):
        ticket = Ticket.objects.create(title="a")

        response = self.client.patch(
            reverse("ticket-detail", args=[ticket.id]), {"status": "closed"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, "closed")