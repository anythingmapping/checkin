#-*- coding: utf-8 -*-
from django.http import *
from django import template
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import fromstr
from world.models import Member
from django.contrib.gis.measure import Distance, D
from django.contrib.gis.geoip import GeoIP

def checkin(request):
    g = GeoIP()
    userip = get_client_ip(request)
    print userip
    mycountry = g.country(userip)
    cc = mycountry["country_name"]
    return render_to_response("checkin.html",locals())
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def showusers(request):
    me = Member.objects.get(name = "me")
    print me.point
    others = Member.objects.filter(point__distance_lt=(me.point, D(km=1000000000)))
    myarray = []
    for otherusers in others.distance(me.point):
        #print (otherusers.point.y, otherusers.point.x)
        myarray.append([otherusers.name, otherusers.image, round(otherusers.distance.km,3),
           int(otherusers.point.y), int(otherusers.point.x)])

    return render_to_response("show.html",locals())


@csrf_exempt
def register(request):


    if request.method == 'POST':
        uname = request.POST.get("username")
        uimage = request.POST.get("userimage")
        ulong = request.POST.get("long")
        ulat = request.POST.get("lat")
        pnt = fromstr('POINT(%s %s)' %(ulat, ulong), srid=4326)
        print (pnt)
        
        newmember = Member(name=uname, image = uimage, point = pnt)
        newmember.save()



        return HttpResponse('welldone')
    else:
        return HttpResponse('error')
