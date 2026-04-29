#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba.
Ejecutar desde el directorio backend:
    cd backend
    python manage.py shell < ../scripts/seed_data.py
O directamente con Django:
    cd backend
    python -c "exec(open('../scripts/seed_data.py').read())"
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.Models.modelsSENA import Person, User, Subject, DigitalDictionary, TestResult

def create_seed_data():
    print("Iniciando creacion de datos de prueba...")
    
    # ── Crear Personas y Usuarios ────────────────────────────────────────────
    users_data = [
        {
            'person': {
                'email': 'admin@gmail.com',
                'password': make_password('123'),
                'doc_type': 'CC',
                'doc_num': '1000000001',
                'first_name': 'Administrador',
                'last_name': 'SENA',
                'phone_num': 3001234567,
                'status': 'ACTIVO',
            },
            'user': {
                'role_id': 'ADMIN',
                'status': 'EN_FORMACION',
                'mfa': '',
            }
        },
        {
            'person': {
                'email': 'docente@gmail.com',
                'password': make_password('123'),
                'doc_type': 'CC',
                'doc_num': '1000000002',
                'first_name': 'Carlos',
                'last_name': 'Martinez',
                'phone_num': 3001234568,
                'status': 'ACTIVO',
            },
            'user': {
                'role_id': 'INSTRUCTOR',
                'status': 'EN_FORMACION',
                'mfa': '',
            }
        },
        {
            'person': {
                'email': 'juan@gmail.com',
                'password': make_password('123'),
                'doc_type': 'CC',
                'doc_num': '1000000003',
                'first_name': 'Juan David',
                'last_name': 'Perez',
                'phone_num': 3001234569,
                'status': 'ACTIVO',
            },
            'user': {
                'role_id': 'APRENDIZ',
                'status': 'EN_FORMACION',
                'mfa': '',
            }
        },
        {
            'person': {
                'email': 'maria@gmail.com',
                'password': make_password('123'),
                'doc_type': 'CC',
                'doc_num': '1000000004',
                'first_name': 'Maria',
                'last_name': 'Garcia Lopez',
                'phone_num': 3001234570,
                'status': 'ACTIVO',
            },
            'user': {
                'role_id': 'APRENDIZ',
                'status': 'EN_FORMACION',
                'mfa': '',
            }
        },
        {
            'person': {
                'email': 'carlos@gmail.com',
                'password': make_password('123'),
                'doc_type': 'CC',
                'doc_num': '1000000005',
                'first_name': 'Carlos Andres',
                'last_name': 'Lopez',
                'phone_num': 3001234571,
                'status': 'INACTIVO',
            },
            'user': {
                'role_id': 'APRENDIZ',
                'status': 'CANCELADO',
                'mfa': '',
            }
        },
        {
            'person': {
                'email': 'ana@gmail.com',
                'password': make_password('123'),
                'doc_type': 'CC',
                'doc_num': '1000000006',
                'first_name': 'Ana Sofia',
                'last_name': 'Rodriguez',
                'phone_num': 3001234572,
                'status': 'ACTIVO',
            },
            'user': {
                'role_id': 'INSTRUCTOR',
                'status': 'EN_FORMACION',
                'mfa': '',
            }
        },
    ]
    
    created_users = []
    for user_data in users_data:
        person_data = user_data['person']
        user_info = user_data['user']
        
        # Verificar si ya existe
        person, created = Person.objects.get_or_create(
            email=person_data['email'],
            defaults=person_data
        )
        
        if created:
            print(f"  + Creada persona: {person.first_name} {person.last_name}")
        else:
            print(f"  = Persona existente: {person.first_name} {person.last_name}")
        
        user, created = User.objects.get_or_create(
            person=person,
            defaults=user_info
        )
        
        if created:
            print(f"    + Creado usuario con rol: {user.role_id}")
        else:
            print(f"    = Usuario existente con rol: {user.role_id}")
        
        created_users.append(user)
    
    # ── Crear Subjects ───────────────────────────────────────────────────────
    subjects_data = [
        {'subject_id': 'Ingles Tecnico', 'description': 'Vocabulario y expresiones tecnicas en ingles'},
        {'subject_id': 'Gramatica Basica', 'description': 'Fundamentos gramaticales del idioma ingles'},
        {'subject_id': 'Comprension Lectora', 'description': 'Desarrollo de habilidades de lectura en ingles'},
        {'subject_id': 'Conversacion', 'description': 'Practica de expresion oral en ingles'},
    ]
    
    created_subjects = []
    for subject_data in subjects_data:
        subject, created = Subject.objects.get_or_create(
            subject_id=subject_data['subject_id'],
            defaults={'description': subject_data['description']}
        )
        
        if created:
            print(f"  + Creada asignatura: {subject.subject_id}")
        else:
            print(f"  = Asignatura existente: {subject.subject_id}")
        
        created_subjects.append(subject)
    
    # ── Crear entradas de diccionario ────────────────────────────────────────
    dictionary_data = [
        {
            'word_id': 'algorithm',
            'subject': created_subjects[0],  # Ingles Tecnico
            'definition': 'A step-by-step procedure for solving a problem',
            'synonyms': 'procedure, method, process',
            'audio': '',
            'video': '',
            'image': '',
        },
        {
            'word_id': 'database',
            'subject': created_subjects[0],
            'definition': 'An organized collection of data stored electronically',
            'synonyms': 'data store, repository',
            'audio': '',
            'video': '',
            'image': '',
        },
        {
            'word_id': 'present simple',
            'subject': created_subjects[1],  # Gramatica Basica
            'definition': 'Tense used for habits, facts, and general truths',
            'synonyms': 'simple present tense',
            'audio': '',
            'video': '',
            'image': '',
        },
    ]
    
    for dict_data in dictionary_data:
        entry, created = DigitalDictionary.objects.get_or_create(
            word_id=dict_data['word_id'],
            subject=dict_data['subject'],
            defaults={
                'definition': dict_data['definition'],
                'synonyms': dict_data['synonyms'],
                'audio': dict_data['audio'],
                'video': dict_data['video'],
                'image': dict_data['image'],
            }
        )
        
        if created:
            print(f"  + Creada entrada de diccionario: {entry.word_id}")
        else:
            print(f"  = Entrada existente: {entry.word_id}")
    
    # ── Crear resultados de pruebas ──────────────────────────────────────────
    # Obtener usuarios estudiantes
    student_users = [u for u in created_users if u.role_id == 'APRENDIZ']
    
    results_data = [
        {
            'user': student_users[0] if len(student_users) > 0 else created_users[2],
            'score': 85,
            'level': 'B2',
            'correct_answers': 17,
            'total_questions': 20,
            'feedback': '',
            'duration': '8:45',
        },
        {
            'user': student_users[0] if len(student_users) > 0 else created_users[2],
            'score': 70,
            'level': 'B1',
            'correct_answers': 14,
            'total_questions': 20,
            'feedback': 'Buen progreso. Te recomiendo practicar mas los tiempos verbales condicionales.',
            'duration': '9:12',
        },
        {
            'user': student_users[1] if len(student_users) > 1 else created_users[3],
            'score': 92,
            'level': 'C1',
            'correct_answers': 18,
            'total_questions': 20,
            'feedback': '',
            'duration': '7:30',
        },
    ]
    
    for result_data in results_data:
        result = TestResult.objects.create(**result_data)
        print(f"  + Creado resultado de prueba: {result.user.person.first_name} - {result.level} ({result.score}%)")
    
    print("\nDatos de prueba creados exitosamente!")
    print(f"  - {Person.objects.count()} personas")
    print(f"  - {User.objects.count()} usuarios")
    print(f"  - {Subject.objects.count()} asignaturas")
    print(f"  - {DigitalDictionary.objects.count()} entradas de diccionario")
    print(f"  - {TestResult.objects.count()} resultados de pruebas")

if __name__ == '__main__':
    create_seed_data()
