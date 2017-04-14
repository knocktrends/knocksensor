# Notifications!

from flask import Flask, request, Response, render_template, jsonify, json
from knockserver import app
from knockserver.database import db_session
from knockserver.models import AccessPattern, PatternPiece
import requests

def pattern_success(access_pattern, device_identifier):
    send_unlock(access_pattern, device_identifier)
    send_success_notification(access_pattern, device_identifier)

def send_unlock(access_pattern):
    device = Device.query.filter(Device.identifier == device_identifier).first()
    
    for profile in ProfileJoin.query.filter(ProfileJoin.pattern_id == access_pattern.id).filter(ProfileJoin.device_id == device.id).all():
        user in User.query.filter(User.id == profile.user_id).first():
        requests.get('https://maker.ifttt.com/trigger/{access_pattern.name}/with/key/{user.ifttt_secret}')

def send_success_notification(access_pattern):
    device = Device.query.filter(Device.identifier == device_identifier).first()
    params = {}

    for profile in ProfileJoin.query.filter(ProfileJoin.device_id == device.id).all():
        user = User.query.filter(User.id == profile.user_id).first()
        for notification in NotificationPrefrences.query.filter(NotificationPreference.id == profile.id).all():
            requests.get('https://maker.ifttt.com/trigger/{notification.name}/with/key/{user.ifttt_secret}')

def send_failure_notification(device_identifier):
    device = Device.query.filter(Device.identifier == device_identifier).first()
    params = {}
    params['failure_count'] = device.failure_count

    for profile in ProfileJoin.query.filter(ProfileJoin.device_id == device.id).all():
        user = User.query.filter(User.id == profile.user_id).first()
        for notification in NotificationPrefrences.query.filter(NotificationPreference.id == profile.id).all():
            if(notification.failed_attempts_threshold >= 0 and device.failure_count % notification.failed_attempts_threshold == 0):
                requests.get('https://maker.ifttt.com/trigger/{notification.failure_endpoint}/with/key/{user.ifttt_secret}')

##
# Subtracts 5670 minutes (4 hours) to get
# into eastern time-zone.
#
def in_dnd_mode(notification):
    utc_seconds_today = time.time() % 86400
    edt_seconds_today = utc_seconds_today - 14400
    minutes_today = edt_seconds_today/60
    if((minutes_today < notification.send_no_earlier) or (minutes_today > notification.send_no_later)):
        return true
    else:
        return false
