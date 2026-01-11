from typing import Literal

type ItqQuestion = Literal[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
type ItqResponse = Literal[0,1,2,3,4]
type ItqForm = dict[ItqQuestion, ItqResponse]