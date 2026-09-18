from dataclasses import dataclass
from typing import Literal

type NumericResponse = Literal[0,1,2,3,4,5,6,7,8,9,10]
@dataclass(frozen=True)
class SoloQuestionnaire:
  client_id: str
  provider_email: str
  stress_before_elements: NumericResponse
  stress_after_elements: NumericResponse
  step_2: NumericResponse
  step_5pod1_first: NumericResponse
  step_5pod1_last: NumericResponse
  step_5pod2_first: NumericResponse
  step_5pod2_last: NumericResponse
  step_5pod3_first: NumericResponse
  step_5pod3_last: NumericResponse
  step_6: NumericResponse