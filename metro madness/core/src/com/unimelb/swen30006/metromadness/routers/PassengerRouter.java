/**
 * 
 */
package com.unimelb.swen30006.metromadness.routers;

import com.unimelb.swen30006.metromadness.passengers.Passenger;
import com.unimelb.swen30006.metromadness.stations.Station;

public interface PassengerRouter {

	public boolean shouldLeave(Station current, Passenger p);
	
}
