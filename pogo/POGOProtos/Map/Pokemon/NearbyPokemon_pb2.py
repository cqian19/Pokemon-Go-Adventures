# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: POGOProtos/Map/Pokemon/NearbyPokemon.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from POGOProtos.Enums import PokemonId_pb2 as POGOProtos_dot_Enums_dot_PokemonId__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='POGOProtos/Map/Pokemon/NearbyPokemon.proto',
  package='POGOProtos.Map.Pokemon',
  syntax='proto3',
  serialized_pb=_b('\n*POGOProtos/Map/Pokemon/NearbyPokemon.proto\x12\x16POGOProtos.Map.Pokemon\x1a POGOProtos/Enums/PokemonId.proto\"r\n\rNearbyPokemon\x12/\n\npokemon_id\x18\x01 \x01(\x0e\x32\x1b.POGOProtos.Enums.PokemonId\x12\x1a\n\x12\x64istance_in_meters\x18\x02 \x01(\x02\x12\x14\n\x0c\x65ncounter_id\x18\x03 \x01(\x06\x62\x06proto3')
  ,
  dependencies=[POGOProtos_dot_Enums_dot_PokemonId__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_NEARBYPOKEMON = _descriptor.Descriptor(
  name='NearbyPokemon',
  full_name='POGOProtos.Map.Pokemon.NearbyPokemon',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pokemon_id', full_name='POGOProtos.Map.Pokemon.NearbyPokemon.pokemon_id', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance_in_meters', full_name='POGOProtos.Map.Pokemon.NearbyPokemon.distance_in_meters', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='encounter_id', full_name='POGOProtos.Map.Pokemon.NearbyPokemon.encounter_id', index=2,
      number=3, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=104,
  serialized_end=218,
)

_NEARBYPOKEMON.fields_by_name['pokemon_id'].enum_type = POGOProtos_dot_Enums_dot_PokemonId__pb2._POKEMONID
DESCRIPTOR.message_types_by_name['NearbyPokemon'] = _NEARBYPOKEMON

NearbyPokemon = _reflection.GeneratedProtocolMessageType('NearbyPokemon', (_message.Message,), dict(
  DESCRIPTOR = _NEARBYPOKEMON,
  __module__ = 'POGOProtos.Map.Pokemon.NearbyPokemon_pb2'
  # @@protoc_insertion_point(class_scope:POGOProtos.Map.Pokemon.NearbyPokemon)
  ))
_sym_db.RegisterMessage(NearbyPokemon)


# @@protoc_insertion_point(module_scope)