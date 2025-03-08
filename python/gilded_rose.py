# -*- coding: utf-8 -*-

class GildedRose:
    def __init__(self, items):
        self.items = items
        self.strategies = {
            "Aged Brie": AgedBrieStrategy(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassStrategy(),
            "Sulfuras, Hand of Ragnaros": SulfurasStrategy(),
        }

    def update_quality(self):
        for item in self.items:
            strategy = self.strategies.get(item.name, ConjuredStrategy() if "Conjured" in item.name else DefaultStrategy())
            strategy.update(item)


class ItemStrategy:
    """ Classe de base pour toutes les stratégies de mise à jour des items. """
    
    def update(self, item):
        raise NotImplementedError("Chaque stratégie doit implémenter la méthode update()")


class DefaultStrategy(ItemStrategy):
    """ Stratégie par défaut pour les objets normaux. """

    def update(self, item):
        self.decrease_quality(item)
        item.sell_in -= 1
        if item.sell_in < 0:
            self.decrease_quality(item)

    def decrease_quality(self, item, amount=1):
        item.quality = max(0, item.quality - amount)


class AgedBrieStrategy(ItemStrategy):
    """ Stratégie pour le fromage Aged Brie (augmente en qualité avec le temps). """

    def update(self, item):
        self.increase_quality(item)
        item.sell_in -= 1
        if item.sell_in < 0:
            self.increase_quality(item)

    def increase_quality(self, item, amount=1):
        item.quality = min(50, item.quality + amount)


class BackstagePassStrategy(ItemStrategy):
    """ Stratégie pour les billets de concert (augmente en qualité mais tombe à 0 après). """

    def update(self, item):
        if item.sell_in <= 0:
            item.quality = 0
        else:
            self.increase_quality(item)
            if item.sell_in <= 10:
                self.increase_quality(item)
            if item.sell_in <= 5:
                self.increase_quality(item)
        item.sell_in -= 1

    def increase_quality(self, item, amount=1):
        item.quality = min(50, item.quality + amount)


class ConjuredStrategy(ItemStrategy):
    """ Stratégie pour les objets Conjured (se dégradent 2 fois plus vite). """

    def update(self, item):
        self.decrease_quality(item, 2)
        item.sell_in -= 1
        if item.sell_in < 0:
            self.decrease_quality(item, 2)

    def decrease_quality(self, item, amount=1):
        item.quality = max(0, item.quality - amount)


class SulfurasStrategy(ItemStrategy):
    """ Stratégie pour Sulfuras (ne change jamais). """

    def update(self, item):
        pass  # Sulfuras ne perd jamais en qualité ni en sell_in

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
