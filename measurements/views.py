from django.shortcuts import render,get_object_or_404

from .models import Measurements
from .forms import MeasurementModelForm

from geopy.geocoders import Photon

from geopy.distance import geodesic
#get_center_coordinates,get_zoom,get_geo,get_ip_address
from .utils import *

import folium

# Create your views here.

def calculate_distance_view(request):

    distance=None
    destination=None
    obj=get_object_or_404(Measurements,id=1)
    form=MeasurementModelForm(request.POST or None)
    ##user_agent = name of app
    geolocator=Photon(user_agent="measurements")

    ip_=get_ip_address(request)
    print(ip_)
    ip="72.14.207.99"
    country,city,lat,lon =get_geo(ip)
    #print("Location country:",country)
    #print("Location city:",city)
    #print("Location latitude and longitude:",lat,lon)

    location=geolocator.geocode(city)
    #print("###",location)

    #location coordinates
    l_lat=lat
    l_lon=lon
    pointA=(l_lat,l_lon)

    #initial folium map
    m=folium.Map(width=1100,height=400,location=get_center_coordinates(l_lat,l_lon),zoom_start=8)

    #location marker
    folium.Marker([l_lat,l_lon],tooltip="Click here for more",popup=city["city"],
                  icon=folium.Icon(color="purple")).add_to(m)

    if form.is_valid():
        instance=form.save(commit=False)
        destination_=form.cleaned_data.get("destination")
        destination=geolocator.geocode(destination_)
        print(destination)
        #destination coordinates
        d_lat=destination.latitude
        d_lon=destination.longitude

        pointB=(d_lat,d_lon)
        #distance calculation
        distance=round(geodesic(pointA,pointB).km,2)

        #folium map modification
        m=folium.Map(width=800,height=400,location=get_center_coordinates(l_lat,l_lon,d_lat,d_lon),
                     zoom_start=get_zoom(distance))

        #location marker
        folium.Marker([l_lat,l_lon],tooltip="Click here for more",popup=city["city"],
                  icon=folium.Icon(color="purple")).add_to(m)
        #destination marker
        folium.Marker([d_lat,d_lon],tooltip="Click here for more",popup=destination,
                  icon=folium.Icon(color="red",icon="cloud")).add_to(m)
        #draw the line between the location and destination
        line=folium.PolyLine(locations=[pointA,pointB],weight=8,color="blue")
        m.add_child(line)

        instance.location=location
        instance.distance=distance
        instance.save()
    else:
        pass
    #converting into html which is later used by using {{map}safe}} in main.html
    m=m._repr_html_()


    context={
        'distance':distance,
        'destination':destination,
        'form':form,
        'map':m,
        }

    return render(request,"measurements/main.html",context)


