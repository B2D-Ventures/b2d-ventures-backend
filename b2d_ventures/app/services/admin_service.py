"""The module defines the AdminService class and AdminError."""

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.utils import timezone

from b2d_ventures.app.models import User, Deal, Investment, Meeting


class AdminError(Exception):
    """Custom Exception for admin-related errors."""


class AdminService:
    """Class definition for AdminService."""

    @staticmethod
    def list_users():
        """
        List all users.

        :return: QuerySet of all users.
        """
        try:
            return User.objects.all()
        except Exception as e:
            raise AdminError(f"Error listing users: {str(e)}")

    @staticmethod
    def get_user_details(user_id):
        """
        Get details of a specific user.

        :param user_id: ID of the user.
        :return: User object.
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist")
        except Exception as e:
            raise AdminError(f"Error getting user details: {str(e)}")

    @staticmethod
    def list_deals():
        """
        List all deals.

        :return: QuerySet of all deals.
        """
        try:
            return Deal.objects.all()
        except Exception as e:
            raise AdminError(f"Error listing deals: {str(e)}")

    @staticmethod
    def approve_deal(deal_id):
        """
        Approve a specific deal.

        :param deal_id: ID of the deal to approve.
        :return: Updated Deal object.
        """
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.status = "approved"
            deal.save()
            return deal
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except Exception as e:
            raise AdminError(f"Error approving deal: {str(e)}")

    @staticmethod
    def reject_deal(deal_id):
        """
        Reject a specific deal.

        :param deal_id: ID of the deal to reject.
        :return: Updated Deal object.
        """
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.status = "rejected"
            deal.save()
            return deal
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except Exception as e:
            raise AdminError(f"Error rejecting deal: {str(e)}")

    @staticmethod
    def list_investments():
        """
        List all investments.

        :return: QuerySet of all investments.
        """
        try:
            return Investment.objects.all()
        except Exception as e:
            raise AdminError(f"Error listing investments: {str(e)}")

    @staticmethod
    def list_meetings():
        """
        List all meetings.

        :return: QuerySet of all meetings.
        """
        try:
            return Meeting.objects.all()
        except Exception as e:
            raise AdminError(f"Error listing meetings: {str(e)}")

    @staticmethod
    def get_dashboard_data():
        """
        Get admin dashboard data.

        :return: Dictionary containing dashboard data.
        """
        try:
            today = timezone.now().date()
            thirty_days_ago = today - timezone.timedelta(days=30)

            total_users = User.objects.count()
            new_users_last_30_days = User.objects.filter(
                created_at__gte=thirty_days_ago
            ).count()

            total_deals = Deal.objects.count()
            active_deals = Deal.objects.filter(status="active").count()

            total_investments = Investment.objects.count()
            total_investment_amount = (
                Investment.objects.aggregate(Sum("amount"))["amount__sum"] or 0
            )

            total_meetings = Meeting.objects.count()
            upcoming_meetings = Meeting.objects.filter(date__gte=today).count()

            return {
                "total_users": total_users,
                "new_users_last_30_days": new_users_last_30_days,
                "total_deals": total_deals,
                "active_deals": active_deals,
                "total_investments": total_investments,
                "total_investment_amount": total_investment_amount,
                "total_meetings": total_meetings,
                "upcoming_meetings": upcoming_meetings,
            }
        except Exception as e:
            raise AdminError(f"Error getting dashboard data: {str(e)}")

    @staticmethod
    def delete_user(user_id):
        """
        Delete a specific user.

        :param user_id: ID of the user to delete.
        """
        try:
            user = User.objects.get(id=user_id)
            user.delete()
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f"User with id {user_id} does not exist")
        except Exception as e:
            raise AdminError(f"Error deleting user: {str(e)}")

    @staticmethod
    def delete_meeting(meeting_id):
        """
        Delete a specific meeting.

        :param meeting_id: ID of the meeting to delete.
        """
        try:
            meeting = Meeting.objects.get(id=meeting_id)
            meeting.delete()
        except Meeting.DoesNotExist:
            raise ObjectDoesNotExist(f"Meeting with id {meeting_id} does not exist")
        except Exception as e:
            raise AdminError(f"Error deleting meeting: {str(e)}")


    @staticmethod
    def delete_investment(investment_id):
        """
        Delete a specific investment.

        :param investment_id: ID of the investment to delete.
        """
        try:
            investment = Investment.objects.get(id=investment_id)
            investment.delete()
        except Investment.DoesNotExist:
            raise ObjectDoesNotExist(
                f"Investment with id {investment_id} does not exist"
            )
        except Exception as e:
            raise AdminError(f"Error deleting investment: {str(e)}")

    @staticmethod
    def delete_deal(deal_id):
        """
        Delete a specific deal.

        :param deal_id: ID of the deal to delete.
        """
        try:
            deal = Deal.objects.get(id=deal_id)
            deal.delete()
        except Deal.DoesNotExist:
            raise ObjectDoesNotExist(f"Deal with id {deal_id} does not exist")
        except Exception as e:
            raise AdminError(f"Error deleting deal: {str(e)}")
