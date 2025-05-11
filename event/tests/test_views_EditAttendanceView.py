from django.test import TestCase, Client
from django.urls import reverse
from event.models import Table, Attendee, DateTimeEntry, CustomUser,DateAvailability   # Import CustomUser

class EditAttendanceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testusername' ,email='testuser@example.com', password='testpassword')  # Use CustomUser
        self.table = Table.objects.create(
            user=self.user,
            event='Test Event',
            password='testpassword',
            address='Test Address',
            freetext='Test Free Text'
        )
        self.attendee = Attendee.objects.create(table=self.table, name='Test Attendee')
        self.date_entry = DateTimeEntry.objects.create(
            date='2024-01-01',
            start_time='12:00',
            end_time='14:00'
        )

    def test_attendee_editing(self):
        date_availability = DateAvailability.objects.create(
            attendee=self.attendee,
            date=self.date_entry,
            availability='maybe'
        )
        data = {'name': 'Updated Attendee', 'availability': 'maybe', 'comment': 'Updated Comment'}
        response = self.client.post(reverse('event:edit_attendance', kwargs={'pk': self.table.pk, 'attendee_id': self.attendee.pk}), data)
        self.assertEqual(response.status_code, 302)  # Redirect status

        updated_attendee = Attendee.objects.get(pk=self.attendee.pk)

        # 現在の日付に関連するDateAvailabilityインスタンスを使用して可用性を確認
        updated_date_availability = updated_attendee.date_availabilities.get(date=self.date_entry)
        self.assertEqual(updated_date_availability.availability, 'maybe')
        self.assertEqual(updated_attendee.name, 'Updated Attendee')
        self.assertEqual(updated_attendee.comment, 'Updated Comment')

    def test_event_edit_page_navigation(self):
        response = self.client.get(reverse('event:edit_attendance', kwargs={'pk': self.table.pk, 'attendee_id': self.attendee.pk}))
        self.assertEqual(response.status_code, 200)  # Normal response

        # Assuming there's a form on the edit page, you might want to check for its presence.
        self.assertContains(response, '<form')

        # You can check for other elements on the edit page as needed.
