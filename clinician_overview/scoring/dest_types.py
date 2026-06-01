from typing import Literal

type DesTQuestion = Literal[1,2,3,4,5,6,7,8]
type DesTResponse = Literal[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
type DesTForm = dict[DesTQuestion, DesTResponse]