from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {'name': 'Superman', 'email': 'superman@dc.com', 'team': 'DC'},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': 'DC'},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Captain America', 'email': 'cap@marvel.com', 'team': 'Marvel'},
            {'name': 'Black Widow', 'email': 'widow@marvel.com', 'team': 'Marvel'},
        ]
        teams = [
            {'name': 'Marvel', 'members': ['Iron Man', 'Captain America', 'Black Widow']},
            {'name': 'DC', 'members': ['Superman', 'Batman', 'Wonder Woman']},
        ]
        activities = [
            {'user': 'Superman', 'activity': 'Flying', 'duration': 60},
            {'user': 'Iron Man', 'activity': 'Flight Training', 'duration': 45},
        ]
        leaderboard = [
            {'team': 'Marvel', 'points': 300},
            {'team': 'DC', 'points': 250},
        ]
        workouts = [
            {'name': 'Strength', 'description': 'Heavy lifting'},
            {'name': 'Cardio', 'description': 'Running and cycling'},
        ]
        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
