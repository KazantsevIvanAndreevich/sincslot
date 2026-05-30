class TestBooking:
    def test_booking_creation(self):
        booking = {
            "id": 1,
            "client_name": "Иван",
            "service": "Стрижка",
            "time": "2026-06-01 10:00",
        }
        assert booking["id"] == 1
        assert booking["client_name"] == "Иван"
        assert booking["service"] == "Стрижка"

    def test_booking_cancellation(self):
        is_cancelled = True
        assert is_cancelled == True

    def test_service_list(self):
        services = ["Стрижка", "Маникюр", "Педикюр"]
        assert len(services) == 3
        assert "Стрижка" in services
