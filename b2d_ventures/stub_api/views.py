from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import uuid
from datetime import datetime


@api_view(["GET"])
def list_stub_endpoints(request):
    endpoints = {
        "endpoints": [
            {"method": "POST", "url": "/api/stub/auths/"},
            {"method": "PUT", "url": "/api/stub/auths/update/"},
            {"method": "GET", "url": "/api/stub/startup/<str:pk>/profile/"},
            {"method": "GET", "url": "/api/stub/startup/<str:pk>/deals/"},
            {"method": "POST", "url": "/api/stub/startup/<str:pk>/deals/"},
            {"method": "GET", "url": "/api/stub/investor/<str:pk>/profile/"},
            {"method": "GET", "url": "/api/stub/investor/<str:pk>/investments/"},
            {"method": "GET", "url": "/api/stub/admin/users/"},
            {"method": "GET", "url": "/api/stub/admin/deals/"},
        ]
    }
    return Response(endpoints)


@api_view(["POST"])
def auth_create(request):
    mock_response = {
        "data": {
            "attributes": {
                "id": str(uuid.uuid4()),
                "username": "John Doe",
                "email": "johndoe@example.com",
                "role": "investor",
                "is_active": True,
                "date_joined": datetime.now().isoformat(),
            }
        },
        "is_new_user": True,
    }
    return Response(mock_response, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
def auth_update(request):
    mock_response = {
        "data": {
            "attributes": {
                "id": str(uuid.uuid4()),
                "username": "John Doe",
                "email": "johndoe@example.com",
                "role": "startup",
                "is_active": True,
                "date_joined": datetime.now().isoformat(),
            }
        }
    }
    return Response(mock_response)


@api_view(["GET", "PUT"])
def startup_profile(request, pk):
    mock_response = {
        "data": {
            "attributes": {
                "id": pk,
                "name": "Startup Inc.",
                "description": "A promising startup",
                "fundraising_goal": 1000000.00,
                "total_raised": 500000.00,
            }
        }
    }
    return Response(mock_response)


@api_view(["GET", "POST"])
def startup_deals(request, pk):
    mock_response = {
        "data": [
            {
                "attributes": {
                    "id": str(uuid.uuid4()),
                    "name": "Series A",
                    "description": "Our first funding round",
                    "allocation": 1000000.00,
                    "price_per_unit": 100.00,
                    "minimum_investment": 10000.00,
                    "type": "equity",
                    "raised": 500000.00,
                    "start_date": "2024-09-01T00:00:00Z",
                    "end_date": "2024-12-31T23:59:59Z",
                    "investor_count": 5,
                    "status": "approved",
                }
            }
        ]
    }
    return Response(mock_response)


@api_view(["GET"])
def investor_profile(request, pk):
    mock_response = {
        "data": {
            "attributes": {
                "id": pk,
                "username": "John Investor",
                "email": "john@investor.com",
                "available_funds": 1000000.00,
                "total_invested": 500000.00,
            }
        }
    }
    return Response(mock_response)


@api_view(["GET"])
def investor_investments(request, pk):
    mock_response = {
        "data": [
            {
                "attributes": {
                    "id": str(uuid.uuid4()),
                    "deal_name": "Series A - Startup Inc.",
                    "investment_amount": 100000.00,
                    "investment_date": "2024-09-15T14:30:00Z",
                }
            }
        ]
    }
    return Response(mock_response)


@api_view(["GET"])
def admin_list_users(request):
    mock_response = {
        "data": [
            {
                "attributes": {
                    "id": str(uuid.uuid4()),
                    "username": "John Doe",
                    "email": "johndoe@example.com",
                    "role": "investor",
                    "is_active": True,
                    "date_joined": "2024-08-31T12:36:39.416269Z",
                }
            },
            {
                "attributes": {
                    "id": str(uuid.uuid4()),
                    "username": "Jane Startup",
                    "email": "jane@startup.com",
                    "role": "startup",
                    "is_active": True,
                    "date_joined": "2024-08-31T12:46:18.887573Z",
                }
            },
        ]
    }
    return Response(mock_response)


@api_view(["GET"])
def admin_list_deals(request):
    mock_response = {
        "data": [
            {
                "attributes": {
                    "id": str(uuid.uuid4()),
                    "name": "Series A - Startup Inc.",
                    "startup_name": "Startup Inc.",
                    "allocation": 1000000.00,
                    "raised": 500000.00,
                    "status": "approved",
                }
            }
        ]
    }
    return Response(mock_response)
