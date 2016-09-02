package com.unimelb.swen30006.metromadness.passengers;

import java.util.ArrayList;
import java.util.Random;

import com.unimelb.swen30006.metromadness.stations.Station;
import com.unimelb.swen30006.metromadness.tracks.Line;

public class PassengerGenerator {
	
	// The station that passengers are getting on
	public Station s;
	// The line they are travelling on
	public ArrayList<Line> lines;
	
	// The max volume
	public float maxVolume;
	
	public PassengerGenerator(Station s, ArrayList<Line> lines, float max){
		this.s = s;
		this.lines = lines;
		this.maxVolume = max;
	}
	
	public Passenger[] generatePassengers(){
		int count = (int) (Math.random()*maxVolume);
		Passenger[] passengers = new Passenger[count];
		for(int i=0; i<count; i++){
			passengers[i] = generatePassenger();
		}
		return passengers;
	}
	
	public Passenger generatePassenger(){
		// Pick a random station from the line
		Line l = this.lines.get((int)Math.random()*(this.lines.size()-1));
		int current_station = l.stations.indexOf(this.s);
		boolean forward = Math.random()>0.5f;
		
		// If we are the end of the line then set our direction forward or backward
		if(current_station == 0){
			forward = true;
		}else if (current_station == l.stations.size()-1){
			forward = false;
		}
		
		// Find the station
		//int index = (int) ( forward ? Math.random()*(current_station+1) : Math.random()*(current_station-1));
		int index = 0;
		Random random = new Random();
		if (forward){
			index = random.nextInt(l.stations.size() -1-current_station) + current_station + 1;
		}else {
			index = current_station - 1 - random.nextInt(current_station);
		}
		Station s = l.stations.get(index);
		
		return this.s.generatePassenger(s);
	}
	
}
