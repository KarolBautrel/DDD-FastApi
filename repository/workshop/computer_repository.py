from domain.workshop.model import Computer
from typing import List, Tuple
from domain.workshop.value_objects import RamCube, Processor, GraphicsCard
from uuid import uuid4


class ComputerRepository:
    def __init__(self, session):
        self.session = session

    def get_computer_by_id(self, id):
        return self.session.query(Computer).filter(Computer.id == id).first()

    def get_computer_by_backref(self, backref):
        return self.session.query(Computer).filter(Computer.backref == backref).first()

    def update_computer(self, computer: Computer, fields_attrs: List[Tuple[str, any]]):
        computer_db = (
            self.session.query(Computer)
            .filter(Computer.backref == computer.backref)
            .first()
        )
        if computer_db is None:
            raise Exception("Computer not found")

        for data in fields_attrs:
            setattr(computer, data[0], data[1])  # model, field, value

    def create_computer(
        self, ram: RamCube, processor: Processor, graph_card: GraphicsCard
    ):
        computer = Computer(
            processor=processor, ram=ram, graph_card=graph_card, backref=str(uuid4())
        )
        self.session.add(computer)

    def get_part_by_backref(self, part_name, backref):
        return (
            self.session.query(part_name).filter(part_name.backref == backref).first()
        )
