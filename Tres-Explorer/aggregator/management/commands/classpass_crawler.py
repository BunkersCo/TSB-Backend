


import os, sys
base = os.path.dirname(os.path.dirname(__file__))
base_parent = os.path.dirname(base)
sys.path.append(base)
sys.path.append(base_parent)

from django.core.management.base import BaseCommand, CommandError
import sys, os, time, random, time

from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = ''
from django.conf import settings



import requests
import base64
import json
from lxml import html
import re
from django.db.models import Q

# crawler settings
useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0'
use_cache = 1
headers = {
    'User-Agent': useragent,
}
base_path = ''

from aggregator.models import Studioentry

class Command(BaseCommand):
    help = 'Example command taking an argument from the command line and with access to model '

    def add_arguments(self, parser):
        parser.add_argument('type', nargs='+', type=str)
        parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):

        # fetch studios
        if  "studios" in options['type'][0]:
            print "\nfetching studios\n"
            self.get_studios(options['id'][0])
        
        # fetch studio
        if "studio" in options['type'][0]:
            print "\nfetching studios\n"
            self.get_studio(options['id'][0])

        # fetch smart
        if "smart" in options['type'][0]:
            misinf = Studioentry.objects.filter(Q(website="") | Q(phone="") | Q(city="") | Q(state="") | Q(zipcode=""))
            for studio in misinf:
                print "launching scraper: ", studio.name.encode('utf-8'), studio.id
                self.get_studio(studio.id)

        print "finish"


    def get_studios(self,id):
        url = "https://classpass.com/a/GetStudios?msaId=" + str(id)
        print "url: ", url
        response = self.cache_or_fetch(url)
        #print response
        data = json.loads(response)
        #pprint(data)
        for studio in data["response"]["studios"]:
            #print studio
            classpass_id = str(studio["id"])
            name = studio["name"].encode('utf-8')
            slug = str(studio["alias"])

            if 'location' in studio.keys():
                if type(studio["location"]) is dict:
                    latitude = str(studio["location"]["lat"])
                if type(studio["location"]) is dict:
                    longitude = str(studio["location"]["lon"])

            print classpass_id + "\t" + name + "\t" + slug + "\t" + latitude + "\t" + longitude
            
            # find
            studio = self.get_or_create(Studioentry, classpass_id=classpass_id, slug=slug, name=name )
            # and update
            studio.latitude=latitude
            studio.longitude=longitude
            studio.save()

        print "studios"

    def get_studio(self,id):
        indb = Studioentry.objects.get(id=id)
        url = "https://classpass.com/" + str(indb.slug)
        response = self.cache_or_fetch(url)
        tree = html.fromstring(response)
        
        title_summary = tree.xpath('//div/p[@class="text--upper text--light mb"]')
        if title_summary:
            title_summary = title_summary[-1]
        #else:
            #return
        complete_address = tree.xpath('//p[@class="mv0"]')[-1].text_content()

        address = complete_address.split("\n")
        address1 = ""
        address2 = ""
        address3 = ""
        city = ""
        state = ""
        zipcode = ""
        phone = ""
        website = ""
        full_address = ""

        for line in address:
            if line:
                line = line.replace("\t","").replace("  ","")
                if "Get directions" not in line and line is not "":
                    
                    arr = line.split(' ')
                    if type(arr) is list:
                        ar = arr[-1].replace(" ","")
                        
                        if ar.isdigit():
                            if int(ar) > 0:
                                if len(arr[-2]) == 2:
                                    zipcode = ar
                                    state = arr[-2]
                                    city = arr[0]
                                    if arr[1] is not arr[-2]:
                                        if arr[1].isdigit():
                                            print "skip"
                                        else:
                                            city += " " + arr[1]
                                    if arr[2] is not arr[-2]:
                                        if arr[2].isdigit():
                                            print "skip"
                                        else:
                                            city += " " + arr[2]
                            else:
                                address2 = line         
                                    
                        else:
                            
                            full_address += line

        city = city.strip().rstrip(',')
        
        meta = tree.xpath('//p[@class="mb0"]')
        if type(meta) is list:
            for info in meta:

                data = info.text_content()

                phonetest = re.sub('[^0-9]+', ' ', data)
                phonePattern = re.compile(r'(\d{3})\D*(\d{3})\D*(\d{4})\D*(\d*)$')
                if phonePattern.search(phonetest):
                    ph = phonePattern.search(phonetest).groups()

                    if type(ph) is tuple:
                        phone = "(" + str(ph[0]) + ") " + str(ph[1]) + "-" + str(ph[2])

                else:
                    if self.is_valid_hostname(data):
                        website = data
                

        if title_summary:
            title_summary = title_summary[-1]

        complete_address = tree.xpath('//p[@class="mv0"]')[-1].text_content()

        geom = "POINT("+str(indb.longitude)+" "+str(indb.latitude)+")"

        indb.address=full_address.strip(",")
        indb.address_2=address2
        indb.state = state
        indb.zipcode = zipcode
        indb.city = city
        indb.phone = phone
        indb.website = website
        indb.geom = geom
        indb.save()


        





    def is_valid_hostname(self,hostname):        
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        if len(hostname) > 253:
            return False
        if re.match(r"[\d.]+$", hostname):
            return False

        allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))



    def get_or_create(self,model, **kwargs):
        instance = model.objects.filter(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            instance.save()
            return instance

    def cache_or_fetch(self,url):
        # handle caching
        encoded = base64.b64encode(url).replace('/','')
        if os.path.exists(base_path+'cache/' + encoded) and use_cache:
            f = open(base_path+'cache/' + encoded,'r')
            text = f.read()
        else:
            page = requests.get(url, headers=headers)
            f = open(base_path+'cache/' + encoded,'w')
            text = page.text
            text = text.encode('utf8');
            f.write(text)
        return text
