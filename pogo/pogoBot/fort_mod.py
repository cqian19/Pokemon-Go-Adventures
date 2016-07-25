import logging
from pogoAPI.location import Location

class fortHandler():

    def __init__(self, session):
        self.session = session

    # Basic solution to spinning all forts.
    # Since traveling salesman problem, not
    # true solution. But at least you get
    # those step in
    def sortCloseForts(self):
        # Sort nearest forts (pokestop)
        logging.info("Sorting Nearest Forts:")
        latitude, longitude, _ = self.session.getCoordinates()
        ordered_forts = []
        stops = self.session.getAllStops()
        for fort in stops:
            dist = Location.getDistance(
                latitude,
                longitude,
                fort.latitude,
                fort.longitude
            )
            ordered_forts.append({'distance': dist, 'fort': fort})

        ordered_forts = sorted(ordered_forts, key=lambda k: k['distance'])
        return [instance['fort'] for instance in ordered_forts]

    # Find the fort closest to user
    def findClosestFort(self):
        # Find nearest fort (pokestop)
        logging.info("Finding Nearest Fort:")
        return self.sortCloseForts(self.session)[0]

    # Walk to fort and spin
    def walkAndSpin(self, fort):
        # No fort, demo == over
        if fort:
            logging.info("Spinning a Fort:")
            # Walk over
            self.session.walkTo(fort.latitude, fort.longitude)
            # Give it a spin
            fortResponse = self.session.getFortSearch(fort)
            logging.info(fortResponse)

    # Walk and spin everywhere
    def walkAndSpinMany(self, forts):
        for fort in forts:
            self.walkAndSpin(self.session, fort)