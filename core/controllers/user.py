from flask_restful import abort
from core.models.user import User as UserModel


class User:
    @staticmethod
    def get(user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(
                404,
                message="User with id: " + str(user_id) + " doesn't exist."
            )

        return {
            'id': user.id,
            'username': user.username,
        }

    @staticmethod
    def post(username, password):
        if username is None or password is None:
            abort(
                400,
                message="Missing arguments."
            )
        has_user = UserModel \
            .query \
            .filter(UserModel.username == username) \
            .first()
        if has_user is not None:
            abort(
                400,
                message="User with username: "
                        + str(username) + " already exist."
            )
        user = UserModel(username=username)
        user.hash_password(password)
        user.save()

        return ({'id': user.id, 'username': user.username}, 201)
