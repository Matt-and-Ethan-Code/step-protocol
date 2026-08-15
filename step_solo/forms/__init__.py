from dataclasses import dataclass


type Layout = VerticalLayout | HorizontalLayout
type FormField = FormVideo | FormText

@dataclass(frozen=True)
class Attributed:
    attributes: list[tuple[str, str]]
@dataclass(frozen=True)
class Form(Attributed):
    name: str
    layout: Layout

@dataclass(frozen=True)
class FormVideo(Attributed):
    src: str
    should_preload: bool

@dataclass(frozen=True)
class FormText(Attributed):
    src: str

@dataclass(frozen=True)
class FormList(Attributed):
    items: list[str]
@dataclass(frozen=True)
class FormImage(Attributed):
    src: str

@dataclass(frozen=True)
class VerticalLayout(Attributed):
    fields: list[FormField]

@dataclass(frozen=True)
class HorizontalLayout(Attributed):
    fields: list[FormField]
    


