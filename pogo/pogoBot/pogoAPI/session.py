# Load Generated Protobuf
import threading
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .getter import Getter
from .location import Location
from .pokedex import pokedex, teams
from .state import State

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'

class PogoSession():

    lock = threading.Lock()

    def __init__(self, session, authProvider, location, logger, api):
        self.session = session
        self.logger = logger
        self.authProvider = authProvider
        self.api = api
        self._state = State()
        self.lock = threading.Lock()
        self.location = location
        self.authTicket = None
        self.getter = Getter(self._state, location, api)
        time.sleep(2)
        self.getter.run()

    def getReqSession(self):
        return self.session

    """def wrapInRequest(self, payload, **kwargs):
        # If we haven't authenticated before
        info = None
        if not self.authTicket:
            info = RequestEnvelope_pb2.RequestEnvelope.AuthInfo(
                provider=self.authProvider,
                token=RequestEnvelope_pb2.RequestEnvelope.AuthInfo.JWT(
                    contents=self.accessToken,
                    unknown2=59
                )
            )
        # Build Envelope
        coords = self.getter.getCoordinates()
        latitude = kwargs.get('latitude', coords[0])
        longitude = kwargs.get('longitude', coords[1])
        altitude = coords[2]
        req = RequestEnvelope_pb2.RequestEnvelope(
            status_code=2,
            request_id=self.getter.getRPCId(),
            longitude=longitude,
            latitude=latitude,
            altitude=altitude,
            auth_ticket=self.authTicket,
            unknown12=989,
            auth_info=info
        )
        req.requests.extend(payload)
        self.addUnknown6(req)

        return req

    def requestOrThrow(self, req, url=None):
        if url is None:
            url = self.endpoint

        # Send request
        rawResponse = self.session.post(url, data=req.SerializeToString())

        # Parse it out
        res = ResponseEnvelope_pb2.ResponseEnvelope()
        res.ParseFromString(rawResponse.content)

        # Update Auth ticket if it exists
        if res.auth_ticket.start:
            self.authTicket = res.auth_ticket

        return res

    def request(self, req, url=None):
        try:
            return self.requestOrThrow(req, url)
        except Exception as e:
            self.logger.error(e)
            raise GeneralPogoException('Probably server fires.')

    def wrapAndRequest(self, payload, **kwargs):
        res = self.request(self.wrapInRequest(payload, **kwargs))
        if res == []:
            self.logger.critical(res)
            self.logger.critical('Servers seem to be busy. Exiting.')
            raise Exception('No Valid Response.')

        return res"""

    # Parse the default responses
    def parseDefault(self, res):
        self.getter.parseDefault(res)

    def setCoordinates(self, latitude, longitude):
        self.location.setCoordinates(latitude, longitude)

    def changeLocation(self, loc):
        # Restart all requests
        self.getter.pause()
        time.sleep(3)
        self.location.setLocation(loc)
        self.getter.clear()
        time.sleep(1)
        self.session.makeNew()
        self.getter.unpause(locChanged=True)

    def cleanPokemon(self, pokemons = None):
        r = []
        if pokemons is None:
            pokemons = self.checkAllPokemon()
        for poke in pokemons:
            r.append({
                'encounter_id': poke.encounter_id,
                'pokemon_id': poke.pokemon_data.pokemon_id,
                'name': pokedex[poke.pokemon_data.pokemon_id],
                'latitude': poke.latitude,
                'longitude': poke.longitude,
                'time_remaining': poke.time_till_hidden_ms
            })
        return r

    def cleanStops(self):
        r = []
        stops = list(self.checkAllStops())
        plat, plon, alt = self.getter.getCoordinates()
        seenIds = {}
        for stop in stops:
            if self.location.getDistance(plat, plon, stop.latitude, stop.longitude) < 300:
                if stop.id not in seenIds:
                    seenIds[stop.id] = True
                    r.append({
                        'id': stop.id,
                        'latitude': stop.latitude,
                        'longitude': stop.longitude,
                        'lure': bool(stop.lure_info.encounter_id)
                    })
        return r

    def cleanPlayerInfo(self):
        data = self.checkPlayerData()
        stats = self.checkPlayerStats()
        pokecoin = stardust = 0
        for i in data.currencies:
            if i.name == 'STARDUST':
                stardust = i.amount
            elif i.name == 'POKECOIN':
                pokecoin = i.amount
        inventory, maxInventory = self.getter.getInventoryCapacity()
        pokemon, maxPokemon = self.getter.getPokemonCapacity()
        d = {
            'username': data.username,
            'team': teams[str(data.team)],
            'level': stats.level,
            'xp': stats.experience - stats.prev_level_xp,
            'maxXp': stats.next_level_xp - stats.prev_level_xp,
            'stardust': stardust,
            'pokecoin': pokecoin,
            'gender': 'Male' if data.avatar.gender == 0 else 'Female',
            'inventory': inventory,
            'maxInventory': maxInventory,
            'pokemon': pokemon,
            'maxPokemon': maxPokemon
        }
        return d

    # Get encounter
    def encounterPokemon(self, pokemon):
        # Create request
        self.api.encounter(
            encounter_id=pokemon.encounter_id,
            spawn_point_id=pokemon.spawn_point_id,
            player_latitude=self.location.latitude,
            player_longitude=self.location.longitude
        )
        # Parse
        # self._state.encounter.ParseFromString(res.returns[0])

        # Return everything
        # return self._state.encounter

    # Upon Encounter, try and catch
    def catchPokemon(self, pokemon, pokeball=1):

        # Create request
        self.api.catch_pokemon(
            encounter_id=pokemon.encounter_id,
            pokeball=pokeball,
            normalized_reticle_size=1.950,
            spawn_point_guid=pokemon.spawn_point_id,
            hit_pokemon=True,
            spin_modifier=0.850,
            normalized_hit_position=1.0
        )
        # Send
        # res = self.wrapAndRequest(payload)
        # Parse
        # self._state.catch.ParseFromString(res.returns[0])

        # Return everything
        # return self._state.catch

    # Use a razz berry or the like
    def useItemCapture(self, item_id, pokemon):

        # Create request
        self.api.use_item_capture(
            item_id=item_id,
            encounter_id=pokemon.encounter_id,
            spawn_point_id=pokemon.spawn_point_id
        )
        # Send
        # res = self.wrapAndRequest(payload)

        # Parse
        # self._state.itemCapture.ParseFromString(res.returns[0])

        # Return everything
        # return self._state.itemCapture

    # Evolve Pokemon
    def evolvePokemon(self, pokemon):
        self.api.evolve_pokemon(pokemon_id=pokemon.id)

        # Send
        # res = self.wrapAndRequest(payload)

        # Parse
        # self._state.evolve.ParseFromString(res.returns[0])

        # Return everything
        # return self._state.evolve

    # Transfer Pokemon
    def releasePokemon(self, pokemon):

        self.api.release_pokemon(pokemon_id=pokemon.id)

        # Parse
        #self._state.release.ParseFromString(res.returns[0])

        # Return everything
        #return self._state.release

    # Throw away items
    def recycleItem(self, item_id, count):

        self.api.recycle_inventory_item(
            item_id=item_id,
            count=count
        )

        # Parse
        # self._state.recycle.ParseFromString(res.returns[0])

        # Return everything
        # return self._state.recycle

    # set an Egg into an incubator
    def setEgg(self, item, pokemon):
        self.api.use_item_egg_incubator(
            item_id=item.id,
            pokemon_id=pokemon.id
        )

        # self._state.incubator.ParseFromString(res.returns[0])

        # Return everything
        # return self._state.incubator

    def setCaughtPokemon(self, *args):
        self.getter.setCaughtPokemon(*args)

    def setPastStop(self, *args):
        self.getter.setPastStop(*args)

    def walkToWithoutStop(self, olatitude, olongitude, *args, **kwargs):
        for i in self.walkTo(olatitude, olongitude, *args, **kwargs):
            continue

    # These act as more logical functions.
    # Might be better to break out seperately
    # Walk over to position in meters
    def walkTo(self, olatitude, olongitude, epsilon=10, step=35, delay=1):
        # Calculate distance to position
        latitude, longitude, _ = self.getter.getCoordinates()
        dist = closest = Location.getDistance(
            latitude,
            longitude,
            olatitude,
            olongitude
        )

        # Run walk
        divisions = closest / step
        if (abs(divisions) < 1):
            divisions = 1
        dLat = (olatitude - latitude) / divisions
        dLon = (olongitude - longitude) / divisions
        self.logger.info("Walking %f meters. This will take %f seconds..." % (dist, delay * dist / step))
        while dist > epsilon:
            self.logger.debug("%f m -> %f m away", closest - dist, closest)
            newLat = latitude + dLat
            if dLat > 0 and newLat > olatitude:
                latitude = olatitude
            elif dLat < 0 and newLat < olatitude:
                latitude = olatitude
            else:
                latitude = newLat
            newLon = longitude + dLon
            if dLon > 0 and newLon > olongitude:
                longitude = olongitude
            elif dLon < 0 and newLon < olongitude:
                longitude = olongitude
            else:
                longitude = newLon
            self.setCoordinates(
                latitude,
                longitude
            )
            yield # Search for stops in between
            time.sleep(delay)
            dist = Location.getDistance(
                latitude,
                longitude,
                olatitude,
                olongitude
            )

    def pause(self):
        self.getter.pause()
        self.session.stop()

    def checkPlayerStats(self):
        return self._state.playerStats

    def checkProfile(self):
        return self._state.profile

    def checkPlayerData(self):
        return self._state.player_data

    def checkAllPokemon(self):
        return self.getter.pokemon.values()

    def checkAllForts(self):
        return self.getter.forts.values()

    def checkAllStops(self):
        return self.getter.stops.values()

    def checkUnspinnedStops(self):
       return self.getter.filterUnspinnedStops(self.checkAllStops())

    # Check, so we don't have to start another request
    def checkEggs(self):
        return self._state.eggs

    def checkInventory(self):
        return self.getter.inventory

    def checkBadges(self):
        return self._state.badges

    def checkDownloadSettings(self):
        return self._state.settings