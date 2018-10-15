from django.db import models
import json

def subsequences(iterable, length):
    return [iterable[i: i + length] for i in range(len(iterable) - length + 1)]

class ScreenManager(models.Manager):

    def isAvailable(self,screen,seats): # returns availablility of given row and seat number
        seats = seats['seats']
        for row in seats.keys():
            cur = super().get_queryset().filter(screen=screen,row=row)
            if len(cur) == 0:
                return False
            for seat in seats[row]:
                if seat in json.loads(cur[0].seats_unavailable) or seat > cur[0].number_of_seats-1 or seat < 0:
                    return False
        return True

    def allAvailable(self,screen,row=None): # returns all available seats
        rows = super().get_queryset().filter(screen=screen)
        if row:
            rows = super().get_queryset().filter(screen=screen,row=row)
        available = {}
        for row in rows:
            available[row.row] = [i for i in range(0,row.number_of_seats) if i not in json.loads(row.seats_unavailable)]
        return available

    def returnContigous(self,screen,choice,count): # return available contigous seats as per input
        row = super().get_queryset().filter(screen=screen,row=choice['row'])[0]
        available = []
        blocks = json.loads(row.aisle_seats)
        for block in range(0,len(blocks),2):
            temp = []
            for seat in range(blocks[block],blocks[block+1]+1):
                if self.isAvailable(screen,{'seats':{ choice['row'] : [seat] }}):
                    temp.append(seat)
                else:
                    temp = []
                    break
            for cur_block in subsequences(temp,int(count)):
                if choice['seat'] in cur_block:
                    available.append({"availableSeats":{ choice['row'] : cur_block }})

        return json.dumps(available)


    def book(self,screen,seats): #books seats while syncing with isAvailable()
        if self.isAvailable(screen,seats):
            seats = seats['seats']
            for row in seats.keys():
                booked = json.loads(super().get_queryset().filter(screen=screen,row=row)[0].seats_unavailable)
                for seat in seats[row]:
                    booked += [seat]
                temp = super().get_queryset().filter(screen=screen,row=row)[0]
                temp.seats_unavailable = json.dumps(booked)
                temp.save()
            return True
        else:
            return False

# model for screen
class Screen(models.Model):
    row = models.CharField(max_length=10,default='') #row name
    screen = models.CharField(max_length=20,default='') #name of cinema
    number_of_seats = models.IntegerField(default='') #number of seats available at cinema
    aisle_seats = models.CharField(max_length=200,default='') #asile seats save as stringified JSON data
    seats_unavailable = models.CharField(max_length=200,default='') #booked seats save as stringified JSON data
    objects = ScreenManager() #calling ScreenManager defined above
