
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from base.api.serializer import RoomSerializer



@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
         'GET / api/rooms', 
         'GET /api/room/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.room.all()
    roomsSerialized = RoomSerializer(rooms,many = True)
    return Response(roomsSerialized.data)

@api_view(['GET'])
def getRoom(request,pk):
    room = Room.room.get(id=pk)
    roomSerialized = RoomSerializer(room,many=False)
    return Response(roomSerialized.data)