class Player(object):
    def play_turn(self, warrior):
        '''
        Current strategy in determining what action to undertake
        1. Get information on surroundings
        2. Take care of personal safety.
        3. Move towards objective.
           1. Free all prisoners
           2. Move to stairs

        Possible list of improvements to get more points
        a. Run for exit without healing if possible to get time bonus
        b. clear a level before going to the stairs (stair avoidance)
                (could be improved by not using random direction)
        c. Clearing of all mobs
        '''

        self.warrior = warrior
        self.surroundings = self.sense_surroundings()

        # Move if current surroundings are clear
        self.sounds = warrior.listen()

        if self.check_rest_needed() & self.check_safe_to_rest():
            warrior.rest_()
            return
        elif self.check_threatened():
            print 'Ram is feeling threatened, starting to bind enemies'
            self.bind_adjacent_enemy()
            return
        elif self.check_No_Enemies_near() >= 1:
            print 'Ram is confident he can slay this beast! Attacking!'
            self.attack_adjacent_enemy()
            return
        elif self.check_captive_near():
            self.free_captive()
            return
        else:
            direction = self.determine_direction_of_next_objective()
            if self.sounds != []:
                direction = self.avoid_stairs(direction)
            warrior.walk_(direction)
            return

    def get_possible_directions(self):
        possible_directions = ['forward', 'backward', 'left', 'right']
        for direction, place in self.surroundings.iteritems():
            if place.is_wall():
                possible_directions.remove(direction)
        return possible_directions

    def avoid_stairs(self, direction):
        possible_directions = self.get_possible_directions()
        if self.warrior.feel(direction).is_stairs():
            print " Ram don't want to go up stairs yet, changing direction'"
            possible_directions.remove(direction)
            direction = possible_directions[0]

        return direction


    def determine_direction_of_next_objective(self):
        '''
        Goes over all sounds and sets direction to run towards first sound.
        No smartness in here yet.
        '''
        for sound in self.sounds:
            if sound.is_captive():
                direction = self.warrior.direction_of(sound)
                return direction
            elif sound.is_enemy():
                direction = self.warrior.direction_of(sound)
                return direction

        direction = self.warrior.direction_of_stairs()
        return direction

    def bind_adjacent_enemy(self):
        for direction, place in self.surroundings.iteritems():
            if place.is_enemy():
                self.warrior.bind_(direction)
                return

    def attack_adjacent_enemy(self):
        for direction, place in self.surroundings.iteritems():
            if place.is_enemy():
                self.warrior.attack_(direction)
                return

    def free_captive(self):
        for direction, place in self.surroundings.iteritems():
            if place.is_captive():
                self.warrior.rescue_(direction)
                return

    def check_safe_to_rest(self):
        safe = True
        for place in self.surroundings.itervalues():
            if place.is_enemy():
                safe = False
        return safe

    def check_No_Enemies_near(self):
        NoOfEnemies = 0
        for place in self.surroundings.itervalues():
            if place.is_enemy():
                NoOfEnemies += 1
        return NoOfEnemies

    def check_captive_near(self):
        NoOfPrisoners = 0
        for place in self.surroundings.itervalues():
            if place.is_captive():
                NoOfPrisoners += 1
        return NoOfPrisoners

    def check_threatened(self):
        NoOfEnemies = self.check_No_Enemies_near()
        if NoOfEnemies >= 2:
            return True
        elif NoOfEnemies >= 1 and self.warrior.health() < 5:
            return True
        else:
            return False

    def check_rest_needed(self):
        health = self.warrior.health()
        if self.sounds is None:
            print 'Ram no need rest! all work is done. [%s HP]' % health
            return False
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

