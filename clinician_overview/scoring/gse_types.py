from typing import Literal

type GSEQuestion = Literal[1,2,3,4,5,6,7,8,9,10]
type GSEResponse = Literal[1,2,3,4]
type GSEForm = dict[GSEQuestion, GSEResponse]