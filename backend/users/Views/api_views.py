from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from ..Models.modelsSENA import Person, User, Subject, DigitalDictionary, TestResult
from ..serializers import (
    PersonSerializer, UserSerializer, UserDetailSerializer,
    SubjectSerializer, DigitalDictionarySerializer, TestResultSerializer,
    LoginSerializer, RegisterSerializer
)


# ─── Mapeo de roles Backend -> Frontend ──────────────────────────────────────
ROLE_MAP = {
    'ADMIN': 'admin',
    'INSTRUCTOR': 'teacher',
    'MONITOR': 'teacher',
    'APRENDIZ': 'student',
}

ROLE_MAP_REVERSE = {
    'admin': 'ADMIN',
    'teacher': 'INSTRUCTOR',
    'student': 'APRENDIZ',
}

STATUS_MAP = {
    'ACTIVO': 'active',
    'INACTIVO': 'inactive',
    'PENDIENTE': 'inactive',
    'EN_FORMACION': 'active',
    'CANCELADO': 'inactive',
    'TRASLADADO': 'inactive',
    'RETIRO': 'inactive',
    'APLAZADO': 'inactive',
}

# ─── Permisos por rol ────────────────────────────────────────────────────────
def get_permissions_by_role(role):
    """Devuelve los permisos segun el rol del usuario"""
    role_permissions = {
        'admin': {
            'canManageUsers': True,
            'canManageDocuments': True,
            'canViewStatistics': True,
            'canGiveFeedback': True,
            'canTakeQuiz': False,
            'canViewResults': True,
            'canManageSubjects': True,
            'canConfigureLevels': True,
        },
        'teacher': {
            'canManageUsers': False,
            'canManageDocuments': True,
            'canViewStatistics': True,
            'canGiveFeedback': True,
            'canTakeQuiz': False,
            'canViewResults': True,
            'canManageSubjects': False,
            'canConfigureLevels': False,
        },
        'student': {
            'canManageUsers': False,
            'canManageDocuments': False,
            'canViewStatistics': False,
            'canGiveFeedback': False,
            'canTakeQuiz': True,
            'canViewResults': True,
            'canManageSubjects': False,
            'canConfigureLevels': False,
        }
    }
    return role_permissions.get(role, role_permissions['student'])


# ─── Auth Views ──────────────────────────────────────────────────────────────

class LoginAPIView(APIView):
    """Vista para autenticacion de usuarios"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            person = Person.objects.get(email=email)
        except Person.DoesNotExist:
            return Response(
                {'error': 'Credenciales incorrectas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verificar password
        if not check_password(password, person.password):
            return Response(
                {'error': 'Credenciales incorrectas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Verificar estado
        if person.status != 'ACTIVO':
            return Response(
                {'error': 'Cuenta inactiva. Contacte al administrador.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Obtener usuario asociado
        try:
            user = User.objects.get(person=person)
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no tiene cuenta asociada'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        # Mapear rol al formato del frontend
        frontend_role = ROLE_MAP.get(user.role_id, 'student')
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.user_id),
                'name': f"{person.first_name} {person.last_name}",
                'email': person.email,
                'role': frontend_role,
                'status': STATUS_MAP.get(person.status, 'inactive'),
                'permissions': get_permissions_by_role(frontend_role),
                'docType': person.doc_type,
                'docNum': person.doc_num,
                'phoneNum': person.phone_num,
                'firstName': person.first_name,
                'lastName': person.last_name,
            }
        })


class RegisterAPIView(APIView):
    """Vista para registro de nuevos usuarios"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        person = user.person
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        # El rol por defecto es APRENDIZ = student
        frontend_role = 'student'
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.user_id),
                'name': f"{person.first_name} {person.last_name}",
                'email': person.email,
                'role': frontend_role,
                'status': 'active',
                'permissions': get_permissions_by_role(frontend_role),
                'docType': person.doc_type,
                'docNum': person.doc_num,
                'phoneNum': person.phone_num,
                'firstName': person.first_name,
                'lastName': person.last_name,
            }
        }, status=status.HTTP_201_CREATED)


class MeAPIView(APIView):
    """Vista para obtener datos del usuario autenticado"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        person = user.person
        frontend_role = ROLE_MAP.get(user.role_id, 'student')
        
        return Response({
            'id': str(user.user_id),
            'name': f"{person.first_name} {person.last_name}",
            'email': person.email,
            'role': frontend_role,
            'status': STATUS_MAP.get(person.status, 'inactive'),
            'permissions': get_permissions_by_role(frontend_role),
            'docType': person.doc_type,
            'docNum': person.doc_num,
            'phoneNum': person.phone_num,
            'firstName': person.first_name,
            'lastName': person.last_name,
        })


# ─── ViewSets ────────────────────────────────────────────────────────────────

class PersonViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de personas"""
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de usuarios"""
    queryset = User.objects.select_related('person').all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        role = self.request.query_params.get('role', None)
        if role:
            # Convertir rol de frontend a backend
            backend_role = ROLE_MAP_REVERSE.get(role, role.upper())
            queryset = queryset.filter(role_id=backend_role)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        users = []
        
        for user in queryset:
            person = user.person
            frontend_role = ROLE_MAP.get(user.role_id, 'student')
            users.append({
                'id': str(user.user_id),
                'name': f"{person.first_name} {person.last_name}",
                'email': person.email,
                'role': frontend_role,
                'status': STATUS_MAP.get(person.status, 'inactive'),
                'permissions': get_permissions_by_role(frontend_role),
                'docType': person.doc_type,
                'docNum': person.doc_num,
                'phoneNum': person.phone_num,
                'firstName': person.first_name,
                'lastName': person.last_name,
                'createdAt': user.created_at.isoformat() if user.created_at else None,
            })
        
        return Response(users)
    
    @action(detail=True, methods=['patch'])
    def toggle_status(self, request, pk=None):
        """Activar/desactivar usuario"""
        user = self.get_object()
        person = user.person
        person.status = 'INACTIVO' if person.status == 'ACTIVO' else 'ACTIVO'
        person.save()
        return Response({'status': STATUS_MAP.get(person.status, 'inactive')})
    
    @action(detail=True, methods=['patch'])
    def change_role(self, request, pk=None):
        """Cambiar rol del usuario"""
        user = self.get_object()
        new_role = request.data.get('role')
        if new_role:
            backend_role = ROLE_MAP_REVERSE.get(new_role, 'APRENDIZ')
            user.role_id = backend_role
            user.save()
            return Response({'role': new_role})
        return Response({'error': 'Role not provided'}, status=status.HTTP_400_BAD_REQUEST)


class SubjectViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de asignaturas"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        subjects = []
        
        colors = ['#39A900', '#1F4E78', '#D89E00', '#E21B3C', '#9B59B6', '#3498DB']
        
        for i, subject in enumerate(queryset):
            subjects.append({
                'id': subject.subject_id,
                'name': subject.subject_id,
                'description': subject.description,
                'color': colors[i % len(colors)],
                'createdAt': None,
            })
        
        return Response(subjects)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        subject = Subject.objects.create(
            subject_id=data.get('name', data.get('subject_id')),
            description=data.get('description', '')
        )
        return Response({
            'id': subject.subject_id,
            'name': subject.subject_id,
            'description': subject.description,
            'color': '#39A900',
            'createdAt': None,
        }, status=status.HTTP_201_CREATED)


class DigitalDictionaryViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD del diccionario digital"""
    queryset = DigitalDictionary.objects.select_related('subject').all()
    serializer_class = DigitalDictionarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        documents = []
        
        for doc in queryset:
            documents.append({
                'id': str(doc.id),
                'name': doc.word_id,
                'subjectId': doc.subject.subject_id if doc.subject else None,
                'subjectName': doc.subject.description if doc.subject else 'Sin asignar',
                'program': 'Todos los programas',
                'uploadedAt': None,
                'fileType': 'DICT',
                'size': '-',
                'uploadedBy': 'Sistema',
                'wordId': doc.word_id,
                'definition': doc.definition,
                'synonyms': doc.synonyms,
                'audioUrl': doc.audio,
                'videoUrl': doc.video,
                'imageUrl': doc.image,
            })
        
        return Response(documents)


class TestResultViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de resultados de pruebas"""
    queryset = TestResult.objects.select_related('user__person').all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        results = []
        
        for result in queryset:
            person = result.user.person
            results.append({
                'id': str(result.id),
                'userId': str(result.user.user_id),
                'userName': f"{person.first_name} {person.last_name}",
                'score': result.score,
                'level': result.level,
                'correctAnswers': result.correct_answers,
                'totalQuestions': result.total_questions,
                'feedback': result.feedback,
                'duration': result.duration,
                'completedAt': result.created_at.isoformat() if result.created_at else None,
                'answers': [],
            })
        
        return Response(results)
    
    @action(detail=True, methods=['patch'])
    def add_feedback(self, request, pk=None):
        """Agregar feedback a un resultado"""
        result = self.get_object()
        feedback = request.data.get('feedback')
        if feedback:
            result.feedback = feedback
            result.save()
            return Response({'feedback': feedback})
        return Response({'error': 'Feedback not provided'}, status=status.HTTP_400_BAD_REQUEST)
