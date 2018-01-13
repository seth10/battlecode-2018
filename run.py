import battlecode as bc
import random
import sys
import traceback

gc = bc.GameController()
directions = list(bc.Direction)
random.seed(6137)

gc.queue_research(bc.UnitType.Rocket)

my_team = gc.team()

worker_ids = [unit.id for unit in gc.my_units() if unit.unit_type == bc.UnitType.Worker]
print(worker_ids)

launched = False

while True:
    try:
        print("=== Begin round {}! ===".format(gc.round()))
        print("We have {} Karbonite".format(gc.karbonite()))

        for unit in gc.my_units():
            if not unit.location.is_on_map():
                continue
            nearby = gc.sense_nearby_units(unit.location.map_location(), 2)
            
            if unit.unit_type == bc.UnitType.Worker:
                if gc.can_blueprint(unit.id, bc.UnitType.Rocket, bc.Direction.North):
                    gc.blueprint(unit.id, bc.UnitType.Rocket, bc.Direction.North)
                for other in nearby:
                    if gc.can_build(unit.id, other.id):
                        gc.build(unit.id, other.id)

            if unit.unit_type == bc.UnitType.Rocket:
                for other in nearby:
                    if gc.can_load(unit.id, other.id):
                        gc.load(unit.id, other.id)
                if not launched and gc.can_launch_rocket(unit.id, bc.MapLocation(bc.Planet.Mars, 10, 14)):
                    gc.launch_rocket(unit.id, bc.MapLocation(bc.Planet.Mars, 10, 14))
                    print("Launched rocket!!")
                    launched = True

            #print(gc.rocket_landings())

            #d = random.choice(list(bc.Direction))
            #if gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
            #    gc.move_robot(unit.id, d)

    except Exception as e:
        print("Error:", e)
        # use this to show where the error was
        traceback.print_exc()

    gc.next_turn()
    sys.stdout.flush()
    sys.stderr.flush()
