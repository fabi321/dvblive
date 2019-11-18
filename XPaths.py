stoerung: str = "for $x in //StopEvent[descendant::EstimatedTime]/descendant::*[local-name(.)='SituationNumber'] return //PtSituation[*[local-name(.)='SituationNumber'] = $x]/*[local-name(.)='Description']"
lon: str = "//GeoPosition/Longitude/text()"
lat: str = "//GeoPosition/Latitude/text()"
lons_with_lineref: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram'][LineRef='$LINEREF']])[1]/descendant::Projection/Position/Longitude/text()"
lats_with_lineref: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram'][LineRef='$LINEREF']])[1]/descendant::Projection/Position/Latitude/text()"
stops_with_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1][LineRef='$LINEREF'])[1]/descendant::TimedLeg/*/StopPointRef/text()"#replace(.,'([a-z]*:[0-9]*:[0-9]*):.*','$1')"
line_number_with_lineref: str = "//ServiceSection[*/PtMode='tram'][LineRef='$LINEREF']/PublishedLineName/Text/text()"
line_string_with_lineref: str = "//ServiceSection[*/PtMode='tram'][LineRef='$LINEREF']/normalize-space(RouteDescription/Text)"
line_trias_id_with_lineref: str = "//ServiceSection[*/PtMode='tram'][LineRef='$LINEREF']/LineRef/text()"
line_start_with_lineref: str = "//ServiceSection[*/PtMode='tram'][LineRef='$LINEREF']/../OriginStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
line_end_with_lineref: str = "//ServiceSection[*/PtMode='tram'][LineRef='$LINEREF']/../DestinationStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
lons_without_lineref: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram']])[1]/descendant::Projection/Position/Longitude/text()"
lats_without_lineref: str = "(//TripResult[descendant::Service[count(ServiceSection) = 1]/ServiceSection[Mode/PtMode = 'tram']])[1]/descendant::Projection/Position/Latitude/text()"
stops_without_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1])[1]/descendant::TimedLeg/*/StopPointRef/text()"#replace(.,'([a-z]*:[0-9]*:[0-9]*):.*','$1')"
line_number_without_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1])[1]/descendant::ServiceSection/PublishedLineName/Text/text()"
line_string_without_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1])[1]/descendant::ServiceSection/normalize-space(RouteDescription/Text)"
line_trias_id_without_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1])[1]/descendant::ServiceSection/LineRef/text()"
line_start_without_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1])[1]/descendant::ServiceSection/../OriginStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
line_end_without_lineref: str = "(//TripResult[count(descendant::ServiceSection) = 1])[1]/descendant::ServiceSection/../DestinationStopPointRef/text()"#replace(., '([a-z]*:[0-9]*:[0-9]*):.*', '$1')"
