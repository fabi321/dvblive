from typing import Dict, Tuple, List


stoerung: str = "for $x in //StopEvent[descendant::EstimatedTime]/descendant::*[local-name(.)='SituationNumber'] return //PtSituation[*[local-name(.)='SituationNumber'] = $x]/*[local-name(.)='Description']"
location_lon: str = "//GeoPosition/Longitude/text()"
location_lat: str = "//GeoPosition/Latitude/text()"
prefix: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram']$LINEREF])"
first: str = "[1]"
lons: str = "/descendant::Projection/Position/Longitude/text()"
lats: str = "/descendant::Projection/Position/Latitude/text()"
stops: str = "/descendant::TimedLeg/*/StopPointRef/text()"#replace(.,'([a-z]*:[0-9]*:[0-9]*):.*','$1')"
stop_names: str = "/descendant::TimedLeg/*/StopPointName/Text/text()"
line_number: str = "/descendant::ServiceSection/PublishedLineName/Text/text()"
line_string: str = "/descendant::ServiceSection/normalize-space(RouteDescription/Text)"
line_trias_id: str = "/descendant::ServiceSection/LineRef/text()"
line_start: str = "/descendant::ServiceSection/../OriginStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
line_start_name: str = "/descendant::ServiceSection/../OriginText/Text/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
line_end: str = "/descendant::ServiceSection/../DestinationStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
line_end_name: str = "/descendant::ServiceSection/../DestinationText/Text/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
stop_name_ref: str = "/descendant::StopPointRef/text()"
stop_name_lon: str = "/descendant::Longitude/text()"
stop_name_lat: str = "/descendant::Latitude/text()"
stop_name_name: str = "/descendant::StopPointName/Text/text()"
service_section: str = "/descendant::ServiceSection"
projection: str = "/descendant::Projection"
timed_leg: str = "/descendant::TimedLeg"
this_call: str = "/descendant::ThisCall"

def construct_simple_xpath(trip: bool, lineref: bool, single: bool, original_string, lineref_name: str = None) -> str:
    if trip:
        temp_pre = prefix
    else:
        temp_pre = prefix.replace('TripResult', 'StopEventResult')
    if lineref:
        temp_pre = temp_pre.replace('$LINEREF', "[descendant::LineRef='$LINEREF']")
    else:
        temp_pre = temp_pre.replace('$LINEREF', '')
    if lineref_name:
        temp_pre = temp_pre.replace('$LINEREF', lineref_name)
    if single:
        return temp_pre + first + original_string
    return temp_pre + original_string

paths: Dict[str, Tuple[str, str]] = {
    'lons': ("Position/Longitude/text()", projection),
    'lats': ("Position/Latitude/text()", projection),
    'stops': ("*/StopPointRef/text()", timed_leg),
    'stop_names': ("*/StopPointName/Text/text()", timed_leg),
    'timetable_times': ("*/ServiceArrival/TimetabledTime/text()", timed_leg),
    'estimated_times': ("*/ServiceArrival/EstimatedTime/text()", timed_leg),
    'line_number': ("PublishedLineName/Text/text()", service_section),
    'line_string': ("normalize-space(RouteDescription/Text)", service_section),
    'line_trias_id': ("LineRef/text()", service_section),
    'line_start': ("../OriginText/Text/text()", service_section),
    'line_start_name': ("../OriginText/Text/text()", service_section),
    'line_end': ("../DestinationStopPointRef/text()", service_section),
    'line_end_name': ("../DestinationText/Text/text()", service_section)
}

def construct_complex_xpath(type: str, lineref: bool, single: bool, *args: str, lineref_name: str = None) -> str:
    if not args:
        raise NotImplementedError('Tried to run construct_complex_xpath without xpath names')
    if type == 'StopEvent' or type == 'Trip':
        trip: bool = True
        if type == 'StopEvent':
            trip = False
        xpaths: List[str] = []
        prefixes: List[str] = []
        for i in args:
            xpaths.append(paths[i][0])
            prefixes.append(paths[i][1])
        extension: str
        if prefixes.count(prefixes[0]) == len(prefixes):
            extension = prefixes[0] + '/concat('
            for i in xpaths:
                extension += i + ", ' # ', "
            extension = extension[:-9] + ')'
        else:
            extension = '/concat('
            for i in range(len(xpaths)):
                extension += prefixes[i] + '/' + xpaths[i] + ", ' # ', "
            extension = extension[:-9] + ')'
        if type == 'StopEvent':
            extension = extension.replace(timed_leg, this_call)
        return construct_simple_xpath(trip, lineref, single, extension, lineref_name=lineref_name)
    else:
        raise NotImplementedError('Unknown type ' + type + ' at construct_complex_xpath.')
