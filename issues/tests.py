from django.test import TestCase
from django.urls import reverse
from .models import Issue


class IssuesEncodingTests(TestCase):
    def test_text_response_charset_and_content(self):
        url = reverse("issues_text_sample")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content_type = response.headers.get("Content-Type", "")
        self.assertIn("charset=utf-8", content_type.lower())
        body = response.content.decode("utf-8")
        self.assertIn("Descripción", body)
        self.assertIn("á, é, í, ó, ú", body)
        self.assertIn("ñ", body)
        self.assertIn("¡Hola! ¿Qué tal?", body)

    def test_json_response_unicode(self):
        url = reverse("issues_json_sample")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content_type = response.headers.get("Content-Type", "")
        self.assertIn("application/json", content_type.lower())
        self.assertIn("charset=utf-8", content_type.lower())
        text = response.content.decode("utf-8")
        self.assertIn("Descripción", text)
        self.assertIn("tokenización", text)
        self.assertIn("número", text)
        self.assertIn("ñ", text)

    def test_database_storage_and_json_roundtrip(self):
        issue = Issue.objects.create(
            titulo="Factura y Pago – Confirmación",
            descripcion="Descripción con tildes á é í ó ú y eñe ñ",
        )
        url = reverse("issues_db_json", kwargs={"pk": issue.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content_type = response.headers.get("Content-Type", "")
        self.assertIn("application/json", content_type.lower())
        self.assertIn("charset=utf-8", content_type.lower())
        body = response.content.decode("utf-8")
        self.assertIn("Descripción", body)
        self.assertIn("Factura y Pago – Confirmación", body)
        self.assertIn("á é í ó ú", body)
        self.assertIn("ñ", body)
