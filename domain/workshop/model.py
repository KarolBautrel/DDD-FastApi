from domain.workshop.value_objects import RamCube, GraphicsCard, Processor


class Computer:
    def __init__(
        self,
        ram_cube: RamCube,
        graphics_card: GraphicsCard,
        processor: Processor,
        backref: str,
    ):
        self.ram_cube = ram_cube
        self.graphics_card = graphics_card
        self.processor = processor
        self.backref = backref
        self.order_refs = [
            self.ram_cube.order_ref,
            self.graphics_card.order_ref,
            self.processor.order_ref,
        ]

    def change_part(self, part, line):
        part_change_map = {
            "RamCube": self.change_ram,
            "GraphicsCard": self.change_card,
            "Processor": self.change_processor,
        }
        if self.able_to_change(part, line):
            proper_part_method = part_change_map.get(part.__class__.__name__, None)
            if proper_part_method is None:
                raise Exception
            proper_part_method(part)

    def able_to_change(self, part, line):
        return part.order_ref not in self.order_refs and line.qty > 0

    def change_ram(self, ram_cube):
        self.ram_cube = ram_cube
        # Send event

    def change_card(self, graphics_card):
        self.graphics_card = graphics_card
        # Send event

    def change_processor(self, processor):
        self.processor = processor
        # Send event
