def user_role_flags(request):
    user = request.user
    if not user.is_authenticated:
        return {
            'is_teacher_user': False,
            'is_student_user': False,
        }

    def has_relation(obj, relation_name):
        try:
            getattr(obj, relation_name)
            return True
        except Exception:
            return False

    return {
        'is_teacher_user': has_relation(user, 'teacher'),
        'is_student_user': has_relation(user, 'student'),
    }
