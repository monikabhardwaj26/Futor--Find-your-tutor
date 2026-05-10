"""
Management Command: seed_data
Run: python manage.py seed_data

Creates dummy teachers, students, courses, and bookings
so the project has data to display right away.
"""

from django.core.management.base import BaseCommand
from accounts.models import CustomUser, TeacherProfile, StudentProfile
from courses.models import Course
from bookings.models import Booking
from reviews.models import Review
from datetime import date, time


class Command(BaseCommand):
    help = 'Seed the database with dummy data for Futor demo'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding database...'))

        # ── SUPERUSER ──────────────────────────────────────────
        if not CustomUser.objects.filter(email='admin@futor.in').exists():
            admin = CustomUser.objects.create_superuser(
                email='admin@futor.in',
                password='admin123',
                full_name='Futor Admin',
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin@futor.in / admin123'))

        # ── TEACHERS ───────────────────────────────────────────
        teachers_data = [
            {
                'full_name': 'Anita Sharma',
                'email': 'anita@futor.in',
                'phone': '9876543210',
                'qual': 'M.Sc Mathematics, B.Ed',
                'exp': 8,
                'subjects': 'Mathematics, Physics',
                'fees': 3000,
                'city': 'Delhi',
                'mode': 'both',
                'bio': 'Experienced Maths tutor with 8 years of teaching Class 9–12 students. Specialised in JEE preparation.',
                'verified': True,
            },
            {
                'full_name': 'Rajesh Kumar',
                'email': 'rajesh@futor.in',
                'phone': '9876543211',
                'qual': 'M.Sc Physics, Ph.D (pursuing)',
                'exp': 5,
                'subjects': 'Physics, Chemistry',
                'fees': 2500,
                'city': 'Mumbai',
                'mode': 'online',
                'bio': 'Physics graduate passionate about making concepts clear. Online classes for Class 11 & 12.',
                'verified': True,
            },
            {
                'full_name': 'Priya Patel',
                'email': 'priya@futor.in',
                'phone': '9876543212',
                'qual': 'B.Sc Chemistry, M.Ed',
                'exp': 6,
                'subjects': 'Chemistry, Biology, Science',
                'fees': 2000,
                'city': 'Ahmedabad',
                'mode': 'offline',
                'bio': 'Dedicated chemistry teacher with a patient and systematic approach. Home tuition specialist.',
                'verified': True,
            },
            {
                'full_name': 'Mohammed Iqbal',
                'email': 'iqbal@futor.in',
                'phone': '9876543213',
                'qual': 'M.A. English Literature',
                'exp': 10,
                'subjects': 'English, Hindi',
                'fees': 1500,
                'city': 'Lucknow',
                'mode': 'both',
                'bio': 'Expert English teacher helping students build strong grammar, writing and communication skills.',
                'verified': False,
            },
            {
                'full_name': 'Sunita Verma',
                'email': 'sunita@futor.in',
                'phone': '9876543214',
                'qual': 'B.Tech Computer Science',
                'exp': 4,
                'subjects': 'Computer Science, Mathematics',
                'fees': 2800,
                'city': 'Bangalore',
                'mode': 'online',
                'bio': 'Software engineer turned educator. Teaching Python, C++, and school computer science curriculum.',
                'verified': True,
            },
            {
                'full_name': 'Vikram Singh',
                'email': 'vikram@futor.in',
                'phone': '9876543215',
                'qual': 'M.Sc Mathematics',
                'exp': 12,
                'subjects': 'Mathematics, Science, Social Science',
                'fees': 1800,
                'city': 'Jaipur',
                'mode': 'offline',
                'bio': 'Veteran mathematics teacher with 12 years experience. Specialises in primary and middle school students.',
                'verified': True,
            },
        ]

        teacher_users = []
        for td in teachers_data:
            user, created = CustomUser.objects.get_or_create(
                email=td['email'],
                defaults={
                    'full_name': td['full_name'],
                    'phone_number': td['phone'],
                    'role': 'teacher',
                }
            )
            if created:
                user.set_password('teacher123')
                user.save()

            profile, _ = TeacherProfile.objects.get_or_create(user=user)
            profile.qualification   = td['qual']
            profile.experience_years = td['exp']
            profile.subjects        = td['subjects']
            profile.fees_per_month  = td['fees']
            profile.city            = td['city']
            profile.teaching_mode   = td['mode']
            profile.bio             = td['bio']
            profile.is_verified     = td['verified']
            profile.is_available    = True
            profile.save()

            teacher_users.append(user)
            if created:
                self.stdout.write(f'  Created teacher: {user.full_name}')

        # ── STUDENTS ───────────────────────────────────────────
        students_data = [
            {'full_name': 'Rahul Sharma',   'email': 'rahul@futor.in',   'class_name': '12', 'subjects': 'Mathematics, Physics',   'city': 'Delhi'},
            {'full_name': 'Sneha Gupta',    'email': 'sneha@futor.in',   'class_name': '11', 'subjects': 'Chemistry, Biology',     'city': 'Mumbai'},
            {'full_name': 'Arjun Mehta',    'email': 'arjun@futor.in',   'class_name': '10', 'subjects': 'Science, English',       'city': 'Ahmedabad'},
            {'full_name': 'Kavya Reddy',    'email': 'kavya@futor.in',   'class_name': '9',  'subjects': 'Mathematics, Hindi',     'city': 'Hyderabad'},
        ]

        student_users = []
        for sd in students_data:
            user, created = CustomUser.objects.get_or_create(
                email=sd['email'],
                defaults={
                    'full_name': sd['full_name'],
                    'role': 'student',
                }
            )
            if created:
                user.set_password('student123')
                user.save()

            sprofile, _ = StudentProfile.objects.get_or_create(user=user)
            sprofile.class_name         = sd['class_name']
            sprofile.interested_subjects = sd['subjects']
            sprofile.city               = sd['city']
            sprofile.save()

            student_users.append(user)
            if created:
                self.stdout.write(f'  Created student: {user.full_name}')

        # ── COURSES ────────────────────────────────────────────
        courses_to_create = [
            ('12', 'Mathematics'), ('12', 'Physics'), ('12', 'Chemistry'),
            ('11', 'Mathematics'), ('11', 'Physics'), ('11', 'Chemistry'),
            ('10', 'Mathematics'), ('10', 'Science'), ('10', 'English'),
            ('9',  'Mathematics'), ('9',  'Science'), ('9',  'Hindi'),
            ('8',  'Mathematics'), ('8',  'Science'), ('8',  'English'),
        ]
        for cls, subj in courses_to_create:
            Course.objects.get_or_create(class_name=cls, subject_name=subj)
        self.stdout.write(f'  Created {len(courses_to_create)} courses')

        # ── BOOKINGS ───────────────────────────────────────────
        if student_users and teacher_users:
            booking_combos = [
                (student_users[0], teacher_users[0], 'Mathematics', 'confirmed'),
                (student_users[0], teacher_users[1], 'Physics',     'pending'),
                (student_users[1], teacher_users[2], 'Chemistry',   'completed'),
                (student_users[2], teacher_users[3], 'English',     'confirmed'),
                (student_users[3], teacher_users[4], 'Computer Science', 'pending'),
            ]
            for stu, tea, subj, status in booking_combos:
                b, created = Booking.objects.get_or_create(
                    student=stu, teacher=tea, subject=subj,
                    defaults={
                        'preferred_date': date(2025, 6, 15),
                        'preferred_time': time(17, 0),
                        'status': status,
                        'message': 'Looking forward to the demo class!',
                    }
                )
                if created:
                    b.status = status
                    b.save()
            self.stdout.write(f'  Created {len(booking_combos)} bookings')

        # ── REVIEWS ────────────────────────────────────────────
        if student_users and teacher_users:
            reviews_data = [
                (student_users[1], teacher_users[2], 5, 'Excellent Chemistry teacher! Very clear explanations.'),
                (student_users[2], teacher_users[3], 4, 'Great English classes. Improved my writing a lot.'),
            ]
            for stu, tea, rating, text in reviews_data:
                Review.objects.get_or_create(
                    student=stu, teacher=tea,
                    defaults={'rating': rating, 'review_text': text}
                )
            self.stdout.write(f'  Created {len(reviews_data)} reviews')

        # ── FAVORITES ──────────────────────────────────────────
        if student_users and teacher_users:
            try:
                sp = student_users[0].student_profile
                sp.favorite_tutors.add(teacher_users[0], teacher_users[1])
            except Exception:
                pass

        self.stdout.write(self.style.SUCCESS('\nDatabase seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin:    admin@futor.in   / admin123')
        self.stdout.write('  Teacher:  anita@futor.in   / teacher123')
        self.stdout.write('  Student:  rahul@futor.in   / student123')
