"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities with correct structure.
        
        Arrange: Use reset_activities fixture to prepare test data
        Act: Make GET request to /activities endpoint
        Assert: Verify response status and structure
        """
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 3
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_activity_has_correct_structure(self, client, reset_activities):
        """Test that each activity has all required fields.
        
        Arrange: Use reset_activities fixture with known test data
        Act: Make GET request and extract an activity
        Assert: Verify all expected fields are present
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_activity_participants_are_listed(self, client, reset_activities):
        """Test that participants are correctly returned for an activity.
        
        Arrange: Use reset_activities with existing participants
        Act: Get activities and check a specific activity's participants
        Assert: Verify participants list matches fixture data
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert activities["Chess Club"]["participants"] == ["alice@mergington.edu"]
        assert activities["Programming Class"]["participants"] == []
        assert activities["Gym Class"]["participants"] == ["bob@mergington.edu", "charlie@mergington.edu"]

    def test_activity_max_participants_field(self, client, reset_activities):
        """Test that max_participants field is correctly returned.
        
        Arrange: Use reset_activities with known max_participants values
        Act: Get activities from endpoint
        Assert: Verify max_participants matches fixture data
        """
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert activities["Chess Club"]["max_participants"] == 3
        assert activities["Programming Class"]["max_participants"] == 2
        assert activities["Gym Class"]["max_participants"] == 5
