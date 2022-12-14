import numpy as np
import src.utilities.utilities as util

from src.routing_algorithms.BASE_routing import BASE_routing

class GeoRouting(BASE_routing):
    def __init__(self, drone, simulator):
        BASE_routing.__init__(self, drone, simulator)

    def relay_selection(self, opt_neighbors, packet):
        """
        This function returns a relay for packets according to geographic routing using C2S criteria.

        @param packet:
        @param opt_neighbors: a list of tuples (hello_packet, drone)
        @return: The best drone to use as relay or None if no relay is selected

            STEP 1: implement Nearest with Forwarding Progress, Most Forwarding progress,
            Compass Routing  considering the current position of d_0 (self.drone) and
                    the last known position of N(d_0) (drones in opt_neighbours)
            STEP 2: implement NFP, MFP, CR and C2S considering the next target position of d_0 and N(d_0)
            STEP 3: compare the performances of STEP1 and STEP2
            OPTIONAL: design and implement your own heuristic (you can consider all the info in the hello packets)
        """

        GREEDY_HEURISTIC = "MYC2S"  # "MFP"

        assert GREEDY_HEURISTIC in ["NFP", "MFP", "CR", "MYC2S"]

        relay = None
        depot_pos = self.drone.depot.coords
        drone_pos = (
            self.drone.coords
        )  # self.drone.next_target()  # STEP 2 |self.drone.coords # STEP 1 |

        min_FP = self.drone.communication_range
        max_FP = 0
        min_CR = 90
        min_distance = (util.config.ENV_HEIGHT**2 + util.config.ENV_WIDTH**2) ** 0.5

        for hello_pkt, neighbor in opt_neighbors:

            neighbor_pos = (
                hello_pkt.cur_pos
            )  # STEP 1 | hello_pkt.next_target  # STEP 2 |

            if GREEDY_HEURISTIC == "NFP":

                FP = util.projection_on_line_between_points(
                    drone_pos, depot_pos, neighbor_pos
                )
                if FP < min_FP:

                    min_FP = FP
                    relay = neighbor

            elif GREEDY_HEURISTIC == "MFP":

                FP = util.projection_on_line_between_points(
                    drone_pos, depot_pos, neighbor_pos
                )
                if FP > max_FP:

                    max_FP = FP
                    relay = neighbor

            elif GREEDY_HEURISTIC == "CR":

                angle = abs(
                    util.angle_between_points(drone_pos, depot_pos, neighbor_pos)
                )
                if angle < min_CR:

                    min_CR = angle
                    relay = neighbor

            elif GREEDY_HEURISTIC == "MYC2S":
                distance = util.euclidean_distance(
                    neighbor_pos,  # neighbor_pos, neighbor.next_target(), neighbor.coords, hello_pkt.next_target,
                    depot_pos,
                )
                if min(min_distance, distance) < min_distance:
                    min_distance = distance
                    relay = neighbor

        return relay
