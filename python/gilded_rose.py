# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue  # "Sulfuras" ne change jamais

            degradation = 1
            if "Conjured" in item.name:
                degradation = 2  # Les objets conjurés se détériorent deux fois plus vite

            # Mettre à jour la qualité selon le type d'objet
            if item.name == "Aged Brie":
                self.update_aged_brie(item)
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.update_backstage_passes(item)
            else:
                self.update_regular_item(item, degradation)

            # Mise à jour de la date de vente
            item.sell_in -= 1

            # Si l'item est expiré, on met à jour la qualité encore une fois
            if item.sell_in < 0:
                self.handle_expired_item(item, degradation)

    def update_aged_brie(self, item):
        """Aged Brie augmente en qualité au fil du temps."""
        self.increase_quality(item)
        if item.sell_in < 0:
            self.increase_quality(item)  # Double augmentation après expiration
    
    def update_backstage_passes(self, item):
        """Backstage passes augmentent rapidement puis chutent à 0 après le concert."""
        if item.sell_in < 0:
            item.quality = 0
        else:
            self.increase_quality(item)
            if item.sell_in < 10:
                self.increase_quality(item)
            if item.sell_in < 5:
                self.increase_quality(item)

    def update_regular_item(self, item, degradation):
        """Les objets normaux se dégradent normalement."""
        self.decrease_quality(item, degradation)

    def handle_expired_item(self, item, degradation):
        """Gérer les items après leur expiration."""
        if item.name == "Aged Brie":
            self.increase_quality(item)  # Double augmentation après expiration
        elif item.name != "Backstage passes to a TAFKAL80ETC concert":
            self.decrease_quality(item, degradation)  # Double dégradation

    def increase_quality(self, item):
        """Augmente la qualité d'un item sans dépasser 50."""
        if item.quality < 50:
            item.quality += 1

    def decrease_quality(self, item, factor=1):
        """Diminue la qualité d'un item sans descendre en dessous de 0."""
        item.quality = max(0, item.quality - factor)

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
