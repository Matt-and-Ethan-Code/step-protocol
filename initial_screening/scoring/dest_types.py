from typing import Literal

type DesTQuestion = Literal[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
type DesTResponse = Literal[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
type DesTForm = dict[DesTQuestion, DesTResponse]