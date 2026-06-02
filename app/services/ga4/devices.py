async def get_devices_service(days=30):

    return {
        "success": True,
        "data": [
            {
                "device": "mobile",
                "users": 2400
            },
            {
                "device": "desktop",
                "users": 1200
            },
            {
                "device": "tablet",
                "users": 300
            }
        ]
    }