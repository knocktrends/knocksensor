# Notifications!

from flask import Flask, request, Response, render_template, jsonify, json
from knockserver import app
from knockserver.database import db_session
from knockserver.models import AccessPattern, PatternPiece, Device, ProfileJoin, User, NotificationPreferences
import requests, time

def send_query(endpoint, key):
    requests.get('https://maker.ifttt.com/trigger/' + endpoint + '/with/key/' + key)

def pattern_success(access_pattern, device_identifier):
    send_unlock(access_pattern, device_identifier)
    send_success_notification(access_pattern, device_identifier)

def send_unlock(access_pattern, device_identifier):
    device = Device.query.filter(Device.identifier == device_identifier).first()
    
    for profile in ProfileJoin.query.filter(ProfileJoin.pattern_id == access_pattern.id).filter(ProfileJoin.device_id == 1).all():
        
        for user in User.query.filter(User.id == profile.user_id).all():
            send_query(profile.door_name, user.ifttt_secret)

def send_success_notification(access_pattern, device_identifier):
    device = Device.query.filter(Device.identifier == device_identifier).first()
    params = {}

    for profile in ProfileJoin.query.filter(ProfileJoin.device_id == 1).all():
        user = User.query.filter(User.id == profile.user_id).first()
        
        for notification in NotificationPreferences.query.filter(NotificationPreferences.id == profile.preference_id).all():
            if (not in_dnd_mode(notification)):
                send_query(notification.name, user.ifttt_secret)

def send_failure_notification(device_identifier):
    device = Device.query.filter(Device.identifier == device_identifier).first()

    for profile in ProfileJoin.query.filter(ProfileJoin.device_id == 1).all():
        user = User.query.filter(User.id == profile.user_id).first()
        
        for notification in NotificationPreferences.query.filter(NotificationPreferences.id == profile.preference_id).all():
            
            if(notification.failed_attempts_threshold >= 0 and device.failure_count % notification.failed_attempts_threshold == 0):
                send_query(notification.failure_endpoint, user.ifttt_secret)

##
# Uses UTC time
#
def in_dnd_mode(notification):
    utc_seconds_today = int(time.time()) % 86400
    minutes_today = utc_seconds_today/60

    if((notification.send_no_earlier and minutes_today < notification.send_no_earlier) or (notification.send_no_later and minutes_today > notification.send_no_later)):
        return True
    else:
        return False
