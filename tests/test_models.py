import unittest
from models import User, SessionLocal, engine, Base

class TestModels(unittest.TestCase):

    def setUp(self):
        # Create a new database schema for each test
        Base.metadata.create_all(bind=engine)
        self.db = SessionLocal()

    def tearDown(self):
        # Drop the schema after each test
        Base.metadata.drop_all(bind=engine)
        self.db.close()

    def test_user_creation(self):
        user = User(username="testuser", hashed_password="hashedpassword")
        self.db.add(user)
        self.db.commit()

        # Query the user back
        retrieved_user = self.db.query(User).filter(User.username == "testuser").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.hashed_password, "hashedpassword")

if __name__ == '__main__':
    unittest.main()