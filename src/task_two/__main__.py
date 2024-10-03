from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import (
    ParamSpec,
    TypeAlias,
    Type,
    Iterable,
    Tuple,
    List,
    Iterator,
    Set,
    Dict,
)
from itertools import count
import random
import sys

# Incomplete Entity Component System

P = ParamSpec("P")
EntityId: TypeAlias = int


class Component(ABC): ...


class System(ABC):
    priority = 0

    @abstractmethod
    def process(self, *args: P.args, **kwargs: P.kwargs): ...


_entity_count: Iterator[int] = count(start=1)
_components: Dict[Type[Component], Set[EntityId]] = {}
_entities: Dict[EntityId, Dict[Type[Component], Component]] = {}
_systems: List[System] = []


def create_entity(*components: Component) -> EntityId:
    if (entity := next(_entity_count)) not in _entities:
        _entities[entity] = {}
    for component in components:
        add_component(entity, component)
    return entity


def add_component(entity: EntityId, component: Component):
    if (component_class := type(component)) not in _components:
        _components[component_class] = set()
    _components[component_class].add(entity)
    _entities[entity][component_class] = component


def get_components(
    *component_classes: Type[Component],
) -> Iterable[Tuple[EntityId, List[Type[Component]]]] | None:
    try:
        for entity in set.intersection(
            *[_components[cls] for cls in component_classes]
        ):
            yield entity, [_entities[entity][cls] for cls in component_classes]
    except KeyError:
        pass


def add_system(system: System, priority: int = 0):
    system.priority = priority
    _systems.append(system)
    _systems.sort(key=lambda sys: sys.priority, reverse=True)


def process_systems(*args: P.args, **kwargs: P.kwargs):
    for system in _systems:
        system.process(*args, **kwargs)


# Components


@dataclass
class Action(Component):
    value: str


@dataclass
class ActionList(Component):
    value: List[str]


@dataclass
class Enemy(Component):
    name: str


@dataclass
class Hero(Component):
    name: str


@dataclass
class City(Component):
    name: str


@dataclass
class MediaSource(Component):
    name: str
    intro: str


# Systems


class AttackSystem(System):
    def process(self, hero: Hero, city: City, media: MediaSource):
        enemies = [
            (enemy, action)
            for _, (enemy, action, _city) in get_components(Enemy, Action, City)
            if _city.name == city
        ]
        enemy, action = random.choice(enemies)
        print("({}) *{}*".format(enemy.name, action.value))


class DefenseSystem(System):
    def process(self, hero: Hero, city: City, media: MediaSource):
        for _, (_hero, action_list) in get_components(Hero, ActionList):
            if _hero.name == hero:
                count = random.randint(1, len(action_list.value))
                choices = random.sample(action_list.value, k=len(action_list.value))[
                    :count
                ]

                for action in choices:
                    print("({}) *{}*".format(_hero.name, action))
                break


class NewsSystem(System):
    def process(self, hero: Hero, city: City, media: MediaSource):
        for _, (_media,) in get_components(MediaSource):
            if _media.name == media:
                print("~ {} {} saved {}! ~".format(_media.intro, hero, city))


def main():
    if len(sys.argv) != 4:
        print("Invalid number of arguments. Pass hero, city and media source")
        sys.exit(1)

    create_entity(Enemy("Joker"), City("Gotham"), Action("brings anarchy"))
    create_entity(
        Enemy("LeagueOfShadows"),
        City("Gotham"),
        Action("inspires terror with psychotropic gas"),
    )
    create_entity(
        Enemy("Catzilla"),
        City("Tokyo"),
        Action("breaks buildings with its tail and meows chthonically"),
    )
    create_entity(Enemy("Ykuza"), City("Tokyo"), Action("take the government hostage"))
    create_entity(
        Hero("Batman"),
        ActionList(
            [
                "methodically beats with fists",
                "threatens in a low voice",
                "throws shurikens",
            ]
        ),
    )
    create_entity(
        Hero("Catwoman"),
        ActionList(
            [
                "sharpens claws on enemies' faces",
                "smiles mysteriously",
                "jumps like lightning",
            ]
        ),
    )
    create_entity(MediaSource("Radio", "*creaks* Important news, residents!"))
    create_entity(
        MediaSource("TV", "*ahem-ahem* Breaking news! Today is a great day because")
    )

    add_system(AttackSystem())
    add_system(DefenseSystem())
    add_system(NewsSystem())

    _, hero, city, media = sys.argv
    process_systems(hero, city, media)


main()
