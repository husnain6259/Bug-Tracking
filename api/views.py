from rest_framework.response import Response
from rest_framework.decorators import api_view
from project.models import Project
from .seralizers import ProjectSerializer

@api_view(['GET'])
def getRoute(request):
    routes=[
        # yeh ap k large application mein easy ap k access mil jati ha
        'GET /api',
        'GET /api/projects',
        'GET /api/projects/:id'

    ]
    return Response(routes)

# ab jo room bany ha us k get b krna ha

@api_view(['GET'])
def getProjects(request):
    project=Project.objects.all()
    serializer=ProjectSerializer(project,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProjects(request,pk):
    room=Project.objects.get(id=pk)
    serializer=ProjectSerializer(room,many=False)
    return Response(serializer.data)


@api_view(['POST'])
def addProject(request):
    seralizer=ProjectSerializer(data=request.data)
    if seralizer.is_valid():
        seralizer.save()
    return Response(seralizer.data)

# agar hum ny update krna ho project k api mein 
@api_view(['PUT'])
def updateProject(request):
    if request.method=="PUT":
        project=Project.objects.all()
        serializer=ProjectSerializer(project,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data["success"]="updated"
        return Response(serializer.data)