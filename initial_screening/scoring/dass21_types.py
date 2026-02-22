from typing import Literal

Dass21Question = Literal[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
Dass21Response = Literal[0,1,2,3]
Dass21Form = dict[Dass21Question, Dass21Response]
Dass21Severity = Literal['normal', 'mild', 'moderate', 'severe', 'extremely severe']