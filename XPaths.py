stoerung: str = "for $x in //StopEvent[descendant::EstimatedTime]/descendant::*[local-name(.)='SituationNumber'] return //PtSituation[*[local-name(.)='SituationNumber'] = $x]/*[local-name(.)='Description']"
location_lon: str = "//GeoPosition/Longitude/text()"
location_lat: str = "//GeoPosition/Latitude/text()"
with_lineref: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram'][LineRef='$LINEREF']])"
without_lineref: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram']])"
first: str = "[1]"
lons: str = "/descendant::Projection/Position/Longitude/text()"
lats: str = "/descendant::Projection/Position/Latitude/text()"
stops: str = "/descendant::TimedLeg/*/StopPointRef/text()"#replace(.,'([a-z]*:[0-9]*:[0-9]*):.*','$1')"
line_number: str = "/descendant::ServiceSection/PublishedLineName/Text/text()"
line_string: str = "/descendant::ServiceSection/normalize-space(RouteDescription/Text)"
line_trias_id: str = "/descendant::ServiceSection/LineRef/text()"
line_start: str = "/descendant::ServiceSection/../OriginStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
line_end: str = "/descendant::ServiceSection/../DestinationStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"


def construct_xpath(lineref: bool, single: bool, original_string):
    if lineref and single:
        return with_lineref + first + original_string
    elif lineref:
        return with_lineref + original_string
    elif single:
        return without_lineref + first + original_string
    return without_lineref + original_string
