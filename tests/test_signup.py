"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""

    def test_signup_successful(self, client, reset_activities):
        """Test that a student can successfully sign up for an activity.
        
        Arrange: Use reset_activities with an activity that has available spots
        Act: Make POST request to signup endpoint
        Assert: Verify response status and message, and student is added to participants
        """
        # Arrange
        activity_name = "Programming Class"
        email = "david@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client, reset_activities):
        """Test that signup fails with 404 for non-existent activity.
        
        Arrange: Use reset_activities (doesn't include 'Nonexistent Activity')
        Act: Try to sign up for a non-existent activity
        Assert: Verify 404 status and error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_duplicate_student(self, client, reset_activities):
        """Test that a student cannot sign up twice for the same activity.
        
        Arrange: Use reset_activities (Chess Club has alice@mergington.edu already)
        Act: Try to sign up the same student again
        Assert: Verify 400 status and duplicate error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"  # Already signed up in fixture
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up"

    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """Test that multiple different students can sign up for the same activity.
        
        Arrange: Use reset_activities
        Act: Sign up two different students for Programming Class
        Assert: Verify both students are in the participants list
        """
        # Arrange
        activity_name = "Programming Class"
        email1 = "eve@mergington.edu"
        email2 = "frank@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]

    def test_signup_special_characters_in_email(self, client, reset_activities):
        """Test that signup handles emails with special characters.
        
        Arrange: Use reset_activities with a special character email
        Act: Try to sign up with an email containing a plus sign
        Assert: Verify signup succeeds and email is stored correctly
        """
        # Arrange
        activity_name = "Programming Class"
        email = "test+alias@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
