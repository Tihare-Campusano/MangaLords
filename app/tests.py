from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Contacto

class UserRolesTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a client user (non-staff)
        self.client_user = User.objects.create_user(
            username='client@example.com',
            password='password123',
            email='client@example.com'
        )
        # Create an admin user (staff)
        self.admin_user = User.objects.create_user(
            username='admin@example.com',
            password='password123',
            email='admin@example.com',
            is_staff=True
        )

    def test_client_can_access_cart(self):
        """A normal client user can access the cart page."""
        self.client.login(username='client@example.com', password='password123')
        response = self.client.get(reverse('carrito'))
        self.assertEqual(response.status_code, 200)

    def test_admin_cannot_access_cart(self):
        """An administrator is redirected when trying to access the cart page."""
        self.client.login(username='admin@example.com', password='password123')
        response = self.client.get(reverse('carrito'))
        # Should redirect to admin dashboard
        self.assertRedirects(response, reverse('admin'))
        
        # Check that warning message exists
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Los administradores no tienen acceso al carrito de compras.", messages)

    def test_admin_cannot_access_checkout(self):
        """An administrator is redirected when trying to access the checkout page."""
        self.client.login(username='admin@example.com', password='password123')
        response = self.client.get(reverse('pagar'))
        self.assertRedirects(response, reverse('admin'))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Los administradores no pueden realizar compras.", messages)

    def test_admin_cannot_add_to_cart(self):
        """An administrator is redirected when trying to add an item to the cart."""
        self.client.login(username='admin@example.com', password='password123')
        # Using a dummy ID or 1 for pk
        response = self.client.get(reverse('agregar_al_carrito', kwargs={'pk': '1'}))
        self.assertRedirects(response, reverse('admin'))
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Los administradores no pueden añadir productos al carrito.", messages)

    def test_admin_redirected_from_home_and_directory(self):
        """An administrator is redirected from the home and directory pages to their dashboard."""
        self.client.login(username='admin@example.com', password='password123')
        
        # Test home redirect
        response_home = self.client.get(reverse('MangaLords'))
        self.assertRedirects(response_home, reverse('admin'))
        
        # Test directory redirect
        response_dir = self.client.get(reverse('directorio'))
        self.assertRedirects(response_dir, reverse('admin'))

    def test_compras_realizadas_visibility(self):
        """Compras realizadas view behaves correctly for client (own purchases) and admin (all purchases)."""
        # Client check
        self.client.login(username='client@example.com', password='password123')
        response = self.client.get(reverse('compras_realizadas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/compras_realizadas.html')
        
        # Admin check
        self.client.login(username='admin@example.com', password='password123')
        response_admin = self.client.get(reverse('compras_realizadas'))
        self.assertEqual(response_admin.status_code, 200)
        self.assertTemplateUsed(response_admin, 'app/compras_realizadas.html')

    def test_contacto_view_segregation(self):
        """Contacto view serves the contact form to clients and the messages inbox to admins."""
        # Client check
        self.client.login(username='client@example.com', password='password123')
        response = self.client.get(reverse('contacto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/contacto.html')
        
        # Admin check
        self.client.login(username='admin@example.com', password='password123')
        response_admin = self.client.get(reverse('contacto'))
        self.assertEqual(response_admin.status_code, 200)
        self.assertTemplateUsed(response_admin, 'app/contacto_admin.html')

    def test_admin_can_toggle_other_user_role(self):
        """An administrator can toggle other user's staff status (role)."""
        self.client.login(username='admin@example.com', password='password123')
        self.assertFalse(self.client_user.is_staff)
        
        response = self.client.get(reverse('toggle_user_role', kwargs={'username': self.client_user.username}))
        self.assertRedirects(response, reverse('listar_productos'))
        
        # Refresh from db
        self.client_user.refresh_from_db()
        self.assertTrue(self.client_user.is_staff)

    def test_admin_cannot_toggle_own_role(self):
        """An administrator cannot toggle their own role (prevent lock out)."""
        self.client.login(username='admin@example.com', password='password123')
        self.assertTrue(self.admin_user.is_staff)
        
        response = self.client.get(reverse('toggle_user_role', kwargs={'username': self.admin_user.username}))
        self.assertRedirects(response, reverse('listar_productos'))
        
        # Refresh from db
        self.admin_user.refresh_from_db()
        self.assertTrue(self.admin_user.is_staff)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("No puedes cambiar tu propio rol para no perder el acceso a la administración.", messages)

    def test_client_cannot_toggle_roles(self):
        """A normal client cannot toggle roles."""
        self.client.login(username='client@example.com', password='password123')
        response = self.client.get(reverse('toggle_user_role', kwargs={'username': self.admin_user.username}))
        self.assertRedirects(response, reverse('MangaLords'))

    def test_contact_submission_and_admin_reply(self):
        """A client submits a message, which is saved with their reference, and the admin replies to it."""
        # 1. Client submits contact message
        self.client.login(username='client@example.com', password='password123')
        # We simulate a POST to the contact form
        response = self.client.post(reverse('contacto'), {
            'nombre': 'Client User',
            'email': 'client@example.com',
            'telefono': '987654321',
            'tipo_consulta': 2, # Consultas
            'mensaje': 'Hello, I have a question.'
        })
        self.assertEqual(response.status_code, 200)
        
        # Verify it was saved and associated with the client user
        contacto_msg = Contacto.objects.filter(user=self.client_user).first()
        self.assertIsNotNone(contacto_msg)
        self.assertEqual(contacto_msg.mensaje, 'Hello, I have a question.')
        self.assertFalse(contacto_msg.respondido)
        
        # 2. Admin replies to the contact message
        self.client.login(username='admin@example.com', password='password123')
        response_reply = self.client.post(reverse('responder_contacto', kwargs={'pk': contacto_msg.pk}), {
            'respuesta': 'Here is your answer.'
        })
        self.assertRedirects(response_reply, reverse('contacto'))
        
        # Verify the reply is saved
        contacto_msg.refresh_from_db()
        self.assertTrue(contacto_msg.respondido)
        self.assertEqual(contacto_msg.respuesta, 'Here is your answer.')
        self.assertIsNotNone(contacto_msg.fecha_respuesta)

    def test_client_cannot_reply_to_contact_messages(self):
        """A normal client cannot submit a reply via responder_contacto."""
        contacto_msg = Contacto.objects.create(
            user=self.client_user,
            nombre='Client User',
            email='client@example.com',
            telefono=987654321,
            tipo_consulta=2,
            mensaje='Test message'
        )
        self.client.login(username='client@example.com', password='password123')
        response = self.client.post(reverse('responder_contacto', kwargs={'pk': contacto_msg.pk}), {
            'respuesta': 'Hacked reply'
        })
        self.assertRedirects(response, reverse('MangaLords'))
        contacto_msg.refresh_from_db()
        self.assertFalse(contacto_msg.respondido)
        self.assertIsNone(contacto_msg.respuesta)


from .models import Notificacion, Manga

class NotificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client_user = User.objects.create_user(
            username='client@example.com',
            password='password123',
            email='client@example.com'
        )
        self.admin_user = User.objects.create_user(
            username='admin@example.com',
            password='password123',
            email='admin@example.com',
            is_staff=True
        )

    def test_user_registration_notifies_admins(self):
        # Trigger user registration view (POST request)
        response = self.client.post(reverse('RegistroUsuario'), {
            'nombres': 'Pepito',
            'apellidos': 'Perez',
            'email': 'pepito@example.com',
            'telefono': '987654321',
            'password1': 'Contra987',
            'password2': 'Contra987'
        })
        # Check that a notification is created for the admin user
        admin_notifs = Notificacion.objects.filter(user=self.admin_user)
        self.assertTrue(admin_notifs.exists())
        self.assertIn("Nuevo usuario registrado", admin_notifs.first().mensaje)

    def test_contact_submission_notifies_admins(self):
        self.client.login(username='client@example.com', password='password123')
        self.client.post(reverse('contacto'), {
            'nombre': 'Client User',
            'email': 'client@example.com',
            'telefono': '987654321',
            'tipo_consulta': 2,
            'mensaje': 'Testing notifications'
        })
        admin_notifs = Notificacion.objects.filter(user=self.admin_user)
        self.assertTrue(admin_notifs.exists())
        self.assertIn("Nuevo mensaje pendiente de respuesta", admin_notifs.first().mensaje)

    def test_admin_reply_notifies_client(self):
        contacto_msg = Contacto.objects.create(
            user=self.client_user,
            nombre='Client User',
            email='client@example.com',
            telefono=987654321,
            tipo_consulta=2,
            mensaje='Test query'
        )
        self.client.login(username='admin@example.com', password='password123')
        self.client.post(reverse('responder_contacto', kwargs={'pk': contacto_msg.pk}), {
            'respuesta': 'Official reply'
        })
        client_notifs = Notificacion.objects.filter(user=self.client_user)
        self.assertTrue(client_notifs.exists())
        self.assertIn("Tu mensaje fue respondido", client_notifs.first().mensaje)

    def test_api_endpoints(self):
        n1 = Notificacion.objects.create(user=self.client_user, mensaje="Test 1")
        n2 = Notificacion.objects.create(user=self.client_user, mensaje="Test 2")
        
        self.client.login(username='client@example.com', password='password123')
        
        # Get notifications list
        response = self.client.get(reverse('get_notifications'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['unread_count'], 2)
        self.assertEqual(len(data['notifications']), 2)

        # Mark single read
        response_read = self.client.post(reverse('mark_notification_read', kwargs={'pk': n1.pk}))
        self.assertEqual(response_read.status_code, 200)
        n1.refresh_from_db()
        self.assertTrue(n1.leido)
        self.assertEqual(response_read.json()['unread_count'], 1)

        # Mark all read
        response_all = self.client.post(reverse('mark_all_notifications_read'))
        self.assertEqual(response_all.status_code, 200)
        n2.refresh_from_db()
        self.assertTrue(n2.leido)
        self.assertEqual(response_all.json()['unread_count'], 0)
