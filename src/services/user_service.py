from entities.user import User
from services.user_crypto_service import UserCryptoService
from repositories.user_repository import UserRepository

class UserService():
    """Luokka käyttäjien lisäämistä, poistamista ja muokkausta varten"""
    def __init__(self, user_repository : UserRepository, crypto_service : UserCryptoService) -> None:
        self._user_repository = user_repository
        self._crypto_service = crypto_service

    def create_new_user(self, username : str, password : str):
        # validate username
        # validate password
        if self._user_repository.is_username_taken(username):
            return
        new_user = User(self._crypto_service.create_user_uuid(), username, self._crypto_service.create_hash_from_password(password))
        success = self._user_repository.create_user_in_database(new_user)
        print(success, flush=True)

    def delete_user(self, user : User):
        self._user_repository.delete_user_from_database(user)

    def get_user_by_id(self, user_uuid : str):
        return self._user_repository.get_user_by_id_from_database(user_uuid)

    def set_new_user_password(self, user : User, password : str):
        # validate password
        new_hash = self._crypto_service.create_hash_from_password(password)
        user.set_password_hash(new_hash)
        self._user_repository.update_user_data(user)
    
    def debug_dump_users(self):
        return str(self._user_repository.debug_dump_db())
        