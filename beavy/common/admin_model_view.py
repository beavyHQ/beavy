from flask import abort, redirect, url_for
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import func
from flask_security import current_user


# Customized model view class
class AdminModelView(ModelView):

    def is_accessible(self):
        if not current_user.is_active() or not current_user.is_authenticated():
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated():
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))



    def get_count_query(self):
        """
            Return a the count query for the model type

            A ``query(self.model).count()`` approach produces an excessive
            subquery, so ``query(func.count('*'))`` should be used instead.

            See commit ``#45a2723`` for details.
        """
        if 'polymorphic_identity' in self.model.__mapper_args__:
            return self.session.query(func.count('*')).select_from(self.model.query.selectable)

        return self.session.query(func.count('*')).select_from(self.model)
