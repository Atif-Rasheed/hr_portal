from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from core.models import User
import requests
from django.utils import timezone
from datetime import datetime

class Command(BaseCommand):
    help = 'Create a user with the applicant_admin role if it does not exist'
        
    def get_users(self,api_key):
        url = f"https://api.resumatorapi.com/v1/users?apikey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    


    def create_user(self,user_data):
        group_name = 'administrator'
        username = user_data['email']
        password = 'administrator@123'

        # Check if the group exists, create it if it doesn't
        group, created = Group.objects.get_or_create(name=group_name)
        # Check if the user exists, create it if it doesn't
        user, created = User.objects.get_or_create(username=username)

        # Assign the user to the group
        user.groups.add(group)
        user.user_id = user_data['id']
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.date_created = datetime.strptime(user_data['date_created'], '%Y-%m-%d')
        user.email = user_data['email']
        user.type = user_data['type']
        user.is_staff = True
        user.is_active = True

        # Set the user's password
        user.set_password(password)
        user.save()

        
    def handle(self, *args, **options):
        # group_name = 'hiring_manager'
        # username = 'HiringManager'
        # password = 'hiringmanager@123'

        # # Check if the group exists, create it if it doesn't
        # group, created = Group.objects.get_or_create(name=group_name)

        # # Check if the user exists, create it if it doesn't
        # user, created = User.objects.get_or_create(username=username)

        # # Assign the user to the group
        # user.groups.add(group)
        # user.is_staff = True
        # user.is_active = True

        # # Set the user's password
        # user.set_password(password)
        # user.save()

        # Replace 'your_api_key' with your actual API key
        api_key = 'MQFrqMaAJP0PH9Q93tyEDDoUWKSvY6xh'

        # Get the user data from the API route
        users = self.get_users(api_key)

        if users:
            for user in users:
                self.create_user(user)
                print(f"User {user['first_name']} {user['last_name']} created successfully.")
        else:
            print("Failed to retrieve user data from the API.")

