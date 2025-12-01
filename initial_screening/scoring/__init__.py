from typing import Literal

from initial_screening.scoring.itq_dichotomous import score as itq_dichotomous_score, ItqDichotomousScore # type: ignore
from initial_screening.scoring.itq_dimensional import score as itq_dimensional_score, ItqDimensionalScore # type: ignore
type ItqQuestion = Literal[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
type ItqResponse = Literal[0,1,2,3,4]
type ItqForm = dict[ItqQuestion, ItqResponse]

from initial_screening.scoring.pcl5_diagnostic import score as pcl5_score, Pcl5Score # type: ignore
type Pcl5Question = Literal[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
type Pcl5Response = Literal[0,1,2,3,4]
type Pcl5Form = dict[Pcl5Question, Pcl5Response]


type Dass21Question = Literal[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]
type Dass21Response = Literal[0,1,2,3]
type Dass21Form = dict[Dass21Question, Dass21Response]