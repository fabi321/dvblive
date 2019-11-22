from typing import Dict, Tuple, List
from elementpath import select
from xml.etree import ElementTree


elementpath_concat_fixed: bool = False

stoerung: str = "for $x in //StopEvent[descendant::EstimatedTime]/descendant::*[local-name(.)='SituationNumber'] return //PtSituation[*[local-name(.)='SituationNumber'] = $x]/*[local-name(.)='Description']"
location_lon: str = "//GeoPosition/Longitude/text()"
location_lat: str = "//GeoPosition/Latitude/text()"
prefix: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram']$LINEREF])"
first: str = "[1]"
lons: str = "/descendant::Projection/Position/Longitude/text()"
lats: str = "/descendant::Projection/Position/Latitude/text()"
stops: str = "/descendant::TimedLeg/*/StopPointRef/text()"
stop_names: str = "/descendant::TimedLeg/*/StopPointName/Text/text()"
line_number: str = "/descendant::ServiceSection/PublishedLineName/Text/text()"
line_string: str = "/descendant::ServiceSection/normalize-space(RouteDescription/Text)"
line_trias_id: str = "/descendant::ServiceSection/LineRef/text()"
line_start: str = "/descendant::ServiceSection/../OriginStopPointRef/text()"
line_start_name: str = "/descendant::ServiceSection/../OriginText/Text/text()"
line_end: str = "/descendant::ServiceSection/../DestinationStopPointRef/text()"
line_end_name: str = "/descendant::ServiceSection/../DestinationText/Text/text()"
stop_name_ref: str = "/descendant::StopPointRef/text()"
stop_name_lon: str = "/descendant::Longitude/text()"
stop_name_lat: str = "/descendant::Latitude/text()"
stop_name_name: str = "/descendant::StopPointName/Text/text()"
service_section: str = "/descendant::ServiceSection"
service: str = "/descendant::Service"
projection: str = "/descendant::Projection"
timed_leg: str = "/descendant::TimedLeg"
this_call: str = "/descendant::ThisCall"

def construct_simple_xpath(trip: bool, is_lineref: bool, single: bool, original_string, **kwargs) -> str:
    if trip:
        temp_pre = prefix
    else:
        temp_pre = prefix.replace('TripResult', 'StopEventResult')
    if is_lineref:
        temp_pre = temp_pre.replace('$LINEREF', "[descendant::LineRef='$LINEREF']")
    else:
        temp_pre = temp_pre.replace('$LINEREF', '')
    for i, j in kwargs.items():
        try:
            temp_pre = temp_pre.replace('$' + i.upper(), j)
        except TypeError:
            pass
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
    'line_start': ("OriginStopPointRef/text()", service),
    'line_start_name': ("OriginText/Text/text()", service),
    'line_end': ("DestinationStopPointRef/text()", service),
    'line_end_name': ("DestinationText/Text/text()", service),
    'journey_ref': ("JourneyRef/text()", service)
}

def concat_not_working_workaround(xpath: str, tree: ElementTree.ElementTree, **kwargs):
    origin, entities = xpath.split('/concat(')
    entities: str = entities[:-1]
    entities: List[str] = entities.split(', ')
    output: List[str] = []
    regions: List[ElementTree.Element] = select(tree, origin, **kwargs)
    for i in regions:
        lists: List[List[str]] = []
        for j in entities:
            if j.find("'") == -1:
                temp_result = select(i, j, **kwargs)
                if isinstance(temp_result, list):
                    lists.append(temp_result)
                else:
                    lists.append([temp_result])
            else:
                lists.append([j.replace("'", '')])
        length: int = 0
        for j in lists:
            if len(j) > length:
                length = len(j)
        output_list: List[str] = []
        for j in range(length):
            string: str = ''
            for k in lists:
                if len(k) > 1:
                    string += k[j]
                elif len(k) == 1:
                    string += k[0]
            output_list.append(string)
        output += output_list
    return output


def construct_complex_xpath(type: str, is_lineref: bool, single: bool, *args: str, tree: ElementTree.ElementTree, **kwargs) -> List[str]:
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
                extension += prefixes[i][1:] + '/' + xpaths[i] + ", ' # ', "
            extension = extension[:-9] + ')'
        if type == 'StopEvent':
            extension = extension.replace(timed_leg, this_call)
        xpath = construct_simple_xpath(trip, is_lineref, single, extension, **kwargs)
        elementtree_kwargs: Dict[str, Any] = {'namespaces': kwargs.get('namespaces')}
        if elementpath_concat_fixed:
            return select(tree, xpath, **elementtree_kwargs)
        return concat_not_working_workaround(xpath, tree, **elementtree_kwargs)
    else:
        raise NotImplementedError('Unknown type ' + type + ' at construct_complex_xpath.')
