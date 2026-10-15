(function () {
  'use strict';

  var data = window.KCDayNightLocations || { locations: {}, aliases: {} };
  delete window.KCDayNightLocations;
  var DAY = 86400000;
  var RAD = Math.PI / 180;
  var EPOCH = 2451545;

  function solarDay(cycle, latitude, longitude) {
    var approximate = cycle + 0.0009 - longitude / 360;
    var anomaly = RAD * (357.5291 + 0.98560028 * approximate);
    var center = RAD * (1.9148 * Math.sin(anomaly) + 0.02 * Math.sin(2 * anomaly) + 0.0003 * Math.sin(3 * anomaly));
    var ecliptic = anomaly + center + RAD * 102.9372 + Math.PI;
    var declination = Math.asin(Math.sin(ecliptic) * Math.sin(RAD * 23.4397));
    var transit = EPOCH + approximate + 0.0053 * Math.sin(anomaly) - 0.0069 * Math.sin(2 * ecliptic);
    var noon = (transit - 2440587.5) * DAY;
    var phi = latitude * RAD;
    var cosine = (Math.sin(-0.833 * RAD) - Math.sin(phi) * Math.sin(declination)) /
      (Math.cos(phi) * Math.cos(declination));
    if (cosine <= -1) return { noon: noon, polar: 'day' };
    if (cosine >= 1) return { noon: noon, polar: 'night' };
    var halfDay = Math.acos(cosine) / (2 * Math.PI) * DAY;
    return { noon: noon, sunrise: noon - halfDay, sunset: noon + halfDay };
  }

  function browserZone() {
    try {
      return Intl.DateTimeFormat().resolvedOptions().timeZone;
    } catch (error) {
      return '';
    }
  }

  function state(date, zone) {
    date = date || new Date();
    zone = zone === undefined ? browserZone() : zone;
    var own = Object.prototype.hasOwnProperty;
    var name = own.call(data.aliases, zone) ? data.aliases[zone] : zone;
    var location = own.call(data.locations, name) ? data.locations[name] : null;
    var now = date.getTime();
    if (!location) {
      var hour = date.getHours();
      var next = new Date(now);
      next.setHours(hour < 6 ? 6 : hour < 18 ? 18 : 30, 0, 0, 0);
      return { mode: hour >= 6 && hour < 18 ? 'day' : 'night', nextChange: next.getTime() };
    }
    var cycle = Math.round(now / DAY + 2440587.5 - EPOCH - 0.0009 + location[1] / 360);
    var today = solarDay(cycle, location[0], location[1]);
    var mode = today.polar || 'night';
    var nextChange = now + DAY;
    for (var offset = -1; offset <= 2; offset++) {
      var solar = offset === 0 ? today : solarDay(cycle + offset, location[0], location[1]);
      if (!solar.polar && now >= solar.sunrise && now < solar.sunset) mode = 'day';
      [solar.sunrise, solar.sunset, solar.noon + DAY / 2].forEach(function (boundary) {
        if (boundary > now && boundary < nextChange) nextChange = boundary;
      });
    }
    return { mode: mode, nextChange: nextChange };
  }

  var initial = state();
  window.KCDayNight = {
    state: state,
    applyInitial: function () {
      document.body.classList.remove('day-mode', 'night-mode');
      document.body.classList.add(initial.mode + '-mode');
    }
  };
})();
