from threading import local


# Архитектурный системный паттерн - UnitOfWork
class UnitOfWork:
    """
    Паттерн - Unit Of Work
    """
    # Работает с конкретным потоком
    current = local()

    def __init__(self):
        """
        :return:
        """
        self.new_items = []
        self.dirty_items = []
        self.removed_items = []

    def mapper_registry(self, MapperRegistry):
        """
        :param MapperRegistry:
        :return:
        """
        self.MapperRegistry = MapperRegistry

    def new_reg(self, obj):
        """
        :param obj:
        :return:
        """
        self.new_items.append(obj)

    def register_dirty(self, obj):
        """
        :param obj:
        :return:
        """
        self.dirty_items.append(obj)

    def remove_reg(self, obj):
        """
        :param obj:
        :return:
        """
        self.removed_items.append(obj)

    def commit(self):
        """
        :return:
        """
        self.new_input()
        self.item_update()
        self.item_delete()

        self.new_items.clear()
        self.dirty_items.clear()
        self.removed_items.clear()

    def new_input(self):
        """
        :return:
        """
        print(self.new_items)
        for obj in self.new_items:
            print(f"Вывожу {self.MapperRegistry}")
            self.MapperRegistry.get_mapper(obj).data_insert(obj)

    def item_update(self):
        """
        :return:
        """
        for obj in self.dirty_items:
            self.MapperRegistry.get_mapper(obj).data_update(obj)

    def item_delete(self):
        """
        :return:
        """
        for obj in self.removed_items:
            self.MapperRegistry.get_mapper(obj).data_delete(obj)

    @staticmethod
    def new_current():
        """
        :return:
        """
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        """
        :param unit_of_work:
        :return:
        """
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        """
        :return:
        """
        return cls.current.unit_of_work


class ThingDomain:

    def mark_new(self):
        """
        :return:
        """
        UnitOfWork.get_current().new_reg(self)

    def mark_dirty(self):
        """
        :return:
        """
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        """
        :return:
        """
        UnitOfWork.get_current().remove_reg(self)
