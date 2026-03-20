from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from documents.models import Document
import json
import os


class Command(BaseCommand):
    help = 'Initialize the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database...')
        
        # Create sample user if not exists
        if not User.objects.filter(email='demo@example.com').exists():
            user = User.objects.create_user(
                username='demo',
                email='demo@example.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )
            self.stdout.write(f'Created demo user: {user.email}')
        else:
            user = User.objects.get(email='demo@example.com')
            self.stdout.write(f'Demo user already exists: {user.email}')
        
        # Create sample document if not exists
        if not Document.objects.filter(title='Sample Legal Contract').exists():
            # Create a sample document record (without actual file)
            document = Document.objects.create(
                user=user,
                title='Sample Legal Contract',
                file_type='pdf',
                extracted_text='This is a sample legal contract for demonstration purposes. It contains various legal terms and clauses that would be analyzed by the AI system.',
                summary='This document is a sample legal contract containing standard legal terms and clauses for demonstration of the AI legal analysis system.',
                keywords=['contract', 'legal', 'terms', 'clauses', 'agreement', 'liability'],
                constitutional_references=[
                    {
                        'article': 'Article 19',
                        'text': 'All citizens shall have the right to freedom of speech and expression, assembly, association, movement, residence and settlement, and to practice any profession or occupation.',
                        'score': 0.85
                    }
                ],
                ipc_sections=[
                    {
                        'section': '420',
                        'description': 'Cheating and dishonestly inducing delivery of property',
                        'punishment': 'Imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.',
                        'score': 0.72
                    }
                ],
                legal_analysis='This sample contract demonstrates the AI legal analysis capabilities. The system has identified relevant constitutional provisions and IPC sections that may be applicable to contract disputes and enforcement.',
                is_processed=True
            )
            self.stdout.write(f'Created sample document: {document.title}')
        
        self.stdout.write(
            self.style.SUCCESS('Database initialization completed successfully!')
        )




