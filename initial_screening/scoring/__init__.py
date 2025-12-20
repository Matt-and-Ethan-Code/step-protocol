from .itq_types import *
from .itq_dichotomous import score as itq_dichotomous_score, ItqDichotomousScore # type: ignore
from .itq_dimensional import score as itq_dimensional_score, ItqDimensionalScore # type: ignore

from .pcl5_types import *
from .pcl5_diagnostic import score as pcl5_score, Pcl5Score # type: ignore


from .dass21_types import *
from .dass21 import score as dass21_score, Dass21Score # type: ignore

from .gse_types import *
from .gse import score as gse_score, GSEScore # type: ignore

from .dest_types import *
from .dest import score as dest_score, DesTScore # type: ignore