from rest_framework import permissions
from b2d_ventures.app.models import Investor, Startup

class IsInvestor(permissions.BasePermission):
  """
  Custom permission to only allow investors to access their own resources.
  """
  def has_permission(self, request, view):
      try:
          investor = Investor.objects.get(user=request.user)
          if 'pk' in view.kwargs:
              return str(investor.id) == view.kwargs['pk']
          return True
      except Investor.DoesNotExist:
          return False

  def has_object_permission(self, request, view, obj):
      try:
          investor = Investor.objects.get(user=request.user)
          return obj.id == investor.id
      except Investor.DoesNotExist:
          return False

class IsStartup(permissions.BasePermission):
  """
  Custom permission to only allow startups to access their own resources.
  """
  def has_permission(self, request, view):
      try:
          startup = Startup.objects.get(user=request.user)
          if 'pk' in view.kwargs:
              return str(startup.id) == view.kwargs['pk']
          return True
      except Startup.DoesNotExist:
          return False

  def has_object_permission(self, request, view, obj):
      try:
          startup = Startup.objects.get(user=request.user)
          return obj.id == startup.id
      except Startup.DoesNotExist:
          return False

class IsInvestorOrStartup(permissions.BasePermission):
  """
  Custom permission to allow both investors and startups to access specific shared resources.
  """
  def has_permission(self, request, view):
      return (
          Investor.objects.filter(user=request.user).exists() or
          Startup.objects.filter(user=request.user).exists()
      )