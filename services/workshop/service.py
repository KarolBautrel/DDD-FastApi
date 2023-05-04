from services.workshop.unit_of_work import WorkshopUnitOfWork
from domain.workshop.model import Computer


class WorkshopService:
    def __init__(self):
        self.unit_of_work = WorkshopUnitOfWork()

    def change_part(self, computer_id, part_ref):
        computer = self.get_computer_by_id(computer_id)
        computer_domain_model = self.map_computer_domain_model(computer)
        # TODO FURTHER LOGIC - NO POWER TODAY

    def get_compuer_by_id(self, computer_id):
        computer = self.unit_of_work.get_computer_by_id(computer_id)
        if computer is None:
            raise Exception("No computer")

    def map_computer_domain_model(self, computer):
        return Computer(**computer)  # not sure if it works
