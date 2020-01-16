location_information_request_stop: str = """<?xml version="1.0" encoding="UTF-8"?>
<Trias xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xmlns="http://www.vdv.de/trias">
    <ServiceRequest>
        <siri:RequestTimestamp>2018-04-11T11:00:00</siri:RequestTimestamp>
        <siri:RequestorRef>OpenService</siri:RequestorRef>
        <RequestPayload>
            <LocationInformationRequest>
                <LocationRef>
                    <LocationName>
                        <Text>$STATION</Text>
                    </LocationName>
                </LocationRef>
                <Restrictions>
                    <Type>stop</Type>
                    <IncludePtModes>true</IncludePtModes>
                </Restrictions>
            </LocationInformationRequest>
        </RequestPayload>
    </ServiceRequest>
</Trias>"""

# noinspection PyPep8
trip_request: str = """<?xml version="1.0" encoding="UTF-8"?>
<Trias version="1.2" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ServiceRequest>
    <siri:RequestTimestamp>2019-10-11T11:00:00</siri:RequestTimestamp>
    <siri:RequestorRef>OpenService</siri:RequestorRef>
    <RequestPayload>
      <TripRequest>
        <Origin>
          <LocationRef>
            <StopPointRef>$START_ID</StopPointRef>
          </LocationRef>
          <DepArrTime>$TIME</DepArrTime>
        </Origin>
        <Destination>
          <LocationRef>
            <StopPointRef>$STOP_ID</StopPointRef>
          </LocationRef>
        </Destination>
        <Params>
          <PtModeFilter>
            <Exclude>false</Exclude>
            <PtMode>tram</PtMode>
          </PtModeFilter>
          <NumberOfResults>10</NumberOfResults>
          <InterchangeLimit>1</InterchangeLimit>
          <AlgorithmType>minChanges</AlgorithmType>
          <IncludeTrackSections>true</IncludeTrackSections>
          <IncludeEstimatedTimes>true</IncludeEstimatedTimes>
          <IncludeSituationInfo>true</IncludeSituationInfo>
          <IncludeIntermediateStops>true</IncludeIntermediateStops>
          $POLYGONS
        </Params>
      </TripRequest>
    </RequestPayload>
  </ServiceRequest>
</Trias>"""

stop_request: str = """<?xml version="1.0" encoding="UTF-8"?>
<Trias version="1.2" xmlns="http://www.vdv.de/trias" xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <ServiceRequest>
    <siri:RequestTimestamp>2018-04-11T11:00:00</siri:RequestTimestamp>
    <siri:RequestorRef>OpenService</siri:RequestorRef>
    <RequestPayload>
      <StopEventRequest>
        <Location>
          <LocationRef>
            <StopPointRef>$STATION</StopPointRef>
          </LocationRef>
          <DepArrTime>$TIME</DepArrTime>
        </Location>
        <Params>
          <NumberOfResults>$NUMBER_OF_RESULTS</NumberOfResults>
          <StopEventType>arrival</StopEventType>
          <IncludePreviousCalls>false</IncludePreviousCalls>
          <IncludeOnwardCalls>false</IncludeOnwardCalls>
          <IncludeRealtimeData>true</IncludeRealtimeData>
        </Params>
      </StopEventRequest>
    </RequestPayload>
  </ServiceRequest>
</Trias>"""
stop_name_request: str = """<?xml version="1.0" encoding="UTF-8"?>
<Trias xmlns:siri="http://www.siri.org.uk/siri" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.2" xmlns="http://www.vdv.de/trias"
       xsi:schemaLocation="http://www.vdv.de/trias file:///C:/Develop/dvblive/trias-xsd-v1.2/Trias.xsd">
    <ServiceRequest>
        <siri:RequestTimestamp>2018-04-11T11:00:00</siri:RequestTimestamp>
        <siri:RequestorRef>OpenService</siri:RequestorRef>
        <RequestPayload>
            <LocationInformationRequest>
                <LocationRef>
                    <LocationName>
                        <Text>$NAME</Text>
                    </LocationName>
                </LocationRef>
                <Restrictions>
                    <Type>stop</Type>
                    <IncludePtModes>true</IncludePtModes>
                </Restrictions>
            </LocationInformationRequest>
        </RequestPayload>
    </ServiceRequest>
</Trias>"""
