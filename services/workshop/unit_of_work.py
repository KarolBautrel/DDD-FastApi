from repository.workshop.computer_repository import ComputerRepository
from sqlalchemy.orm import sessionmaker
import db.engine as engine
from event_store.event_store import EventStore
from configs import RedisKeys
from schemas.workshop.schemas import PartChangeDTO
from domain.workshop.model import Computer
from domain.workshop.value_objects import RamCube, Processor, GraphicsCard
from typing import Tuple, List
from configs import RedisKeys


class WorkshopUnitOfWork:
    def __init__(self):
        self.Base = sessionmaker(autocommit=False, autoflush=False, bind=engine.engine)
        self.session = self.Base()
        self.repository = ComputerRepository(self.session)
        self.event_store = EventStore()
        self.event_mapper = {
            RedisKeys.PART_CHANGED.value: (PartChangeDTO, self.change_part),
        }
        self.parts_mapper = {
            "ram_cube": RamCube,
            "processor": Processor,
            "graphics_card": GraphicsCard,
        }

    def get_computer_by_id(self, id):
        return self.repository.get_computer_by_id(id)

    def get_computer_by_backref(self, backref):
        return self.repository.get_computer_by_backref(backref)

    def change_part(self, part_change_dto: PartChangeDTO):
        computer = self.repository.get_computer_by_backref(
            part_change_dto.computer_backref
        )
        part_name = self.parts_mapper.get(part_change_dto.part_name)
        part = self.repository.get_part_by_backref(
            part_name, part_change_dto.part_backref
        )
        if part is None:
            raise Exception("Wrong part")

        self.repository.update_computer(computer, [(str(part_name), part)])

    def create_computer(
        self, ram: RamCube, processor: Processor, graph_card: GraphicsCard
    ):
        self.repository.create_computer(ram, processor, graph_card)

    def commit_transaction(self):
        self.session.commit()

    def check_event_store(self, key):
        shipment = self.event_store.subscribe_event(key)

        ProperSchema = self.event_mapper.get(key, None)[0]
        proper_action = self.event_mapper.get(key, None)[1]
        import pdb

        pdb.set_trace()
        if ProperSchema is None or proper_action is None:
            raise Exception
        proper_action(ProperSchema(**shipment))
