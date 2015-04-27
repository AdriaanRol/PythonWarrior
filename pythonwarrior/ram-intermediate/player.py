class Player(object):
    def play_turn(self, warrior):
        '''
        Current strategy in determining what action to undertake
        1. Get information on surroundings
        2. Take care of personal safety.
        3. Move towards objective.

        Possible list of improvements to get more points
        a. Run for exit without healing if possible to get time bonus
        b. clear a level before going to the stairs
        '''

        self.warrior = warrior
        direction_of_stairs = warrior.direction_of_stairs()
        self.surroundings = self.sense_surroundings()
        if self.check_rest_needed() & self.check_surroundings_safe():
            warrior.rest_()
            return
        elif self.check_threatened():
            print 'Ram is feeling threatened, starting to bind enemies'
            self.bind_adjacent_enemy()
            return

        if self.surroundings[direction_of_stairs].is_enemy():
            print 'Attacking %s in %s direction' % (
                self.surroundings[direction_of_stairs],
                direction_of_stairs)
            warrior.attack_(direction_of_stairs)
            return
        else:
            warrior.walk_(direction_of_stairs)
            return

    def bind_adjacent_enemy(self):
        for direction, place in self.surroundings.iteritems():
            if place.is_enemy():
                self.warrior.bind_(direction)
                return

    def check_surroundings_safe(self):
        safe = True
        for place in self.surroundings.itervalues():
            if place.is_enemy():
                safe = False
        return safe

    def check_threatened(self):
        nOofEnemies = 0
        for place in self.surroundings.itervalues():
            if place.is_enemy():
                nOofEnemies += 1
        if nOofEnemies >= 2:
            return True
        elif nOofEnemies >= 1 and self.warrior.health() < 5:
            return True
        else:
            return False

    def check_rest_needed(self):
        health = self.warrior.health()
        if health < 19:
            print 'Ram is feeling weak, he needs to rest... [%s HP]' % health
            return True
        else:
            print 'Ram is feeling strong! [%s HP]' % health
            return False

    def sense_surroundings(self):
        surroundings = {}
        surroundings['forward'] = self.warrior.feel('forward')
        surroundings['backward'] = self.warrior.feel('backward')
        surroundings['left'] = self.warrior.feel('left')
        surroundings['right'] = self.warrior.feel('right')
        print 'Sensing surroundings... '
        return surroundings

