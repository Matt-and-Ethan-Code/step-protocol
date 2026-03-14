from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from typing import Callable, ParamSpec, TypeVar
from django.contrib.auth.models import AbstractBaseUser

P = ParamSpec("P")
R = TypeVar("R", bound=HttpResponse)

def clinician_required(view_fn: Callable[P, R]) -> Callable[P, R]:
  """
  Guards a route handler to check that the user is logged in AND is a clinician.
  """
  return login_required(
    user_passes_test(
      user_is_clinician,
      login_url="clinician/clinician-required"
    )(view_fn)
  )


def user_is_clinician(user: AbstractBaseUser) -> bool:
  # TODO
  return True
