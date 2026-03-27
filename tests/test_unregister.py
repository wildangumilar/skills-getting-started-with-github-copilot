"""Tests for the DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities."""

    def test_unregister_successful(self, client, reset_activities):
        """Test that a student can successfully unregister from an activity.
        
        Arrange: Use reset_activities with a student signed up in Chess Club
        Act: Make DELETE request to unregister endpoint
        Assert: Verify response status and student is removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"  # Already signed up in fixture
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_activity_not_found(self, client, reset_activities):
        """Test that unregister fails with 404 for non-existent activity.
        
        Arrange: Use reset_activities (doesn't include 'Nonexistent Activity')
        Act: Try to unregister from a non-existent activity
        Assert: Verify 404 status and error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_student_not_registered(self, client, reset_activities):
        """Test that unregister fails with 400 for student not in activity.
        
        Arrange: Use reset_activities (Programming Class is empty)
        Act: Try to unregister a student who was never signed up
        Assert: Verify 400 status and error message
        """
        # Arrange
        activity_name = "Programming Class"
        email = "nonexistent@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student not registered for this activity"

    def test_unregister_from_activity_with_multiple_participants(self, client, reset_activities):
        """Test that unregister removes only the specified student.
        
        Arrange: Use reset_activities (Gym Class has 2 participants)
        Act: Unregister one student from Gym Class
        Assert: Verify only that student is removed, other stays
        """
        # Arrange
        activity_name = "Gym Class"
        email_to_remove = "bob@mergington.edu"
        email_to_keep = "charlie@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert email_to_keep in activities[activity_name]["participants"]

    def test_unregister_then_signup_again(self, client, reset_activities):
        """Test that a student can sign up after unregistering.
        
        Arrange: Use reset_activities with a student in Chess Club
        Act: Unregister student, then sign them up again
        Assert: Verify student is successfully added back
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]

    def test_unregister_case_sensitive_email(self, client, reset_activities):
        """Test that unregister matches email case-sensitively.
        
        Arrange: Use reset_activities with alice@mergington.edu
        Act: Try to unregister ALICE@mergington.edu (different case)
        Assert: Verify unregister fails because case doesn't match
        """
        # Arrange
        activity_name = "Chess Club"
        original_email = "alice@mergington.edu"
        different_case_email = "ALICE@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": different_case_email}
        )
        
        # Assert
        assert response.status_code == 400
        
        # Verify original email is still there
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert original_email in activities[activity_name]["participants"]
