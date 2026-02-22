from typing import Literal

GSEQuestion = Literal[1,2,3,4,5,6,7,8,9,10]
GSEResponse = Literal[1,2,3,4]
GSEForm = dict[GSEQuestion, GSEResponse]