package com.unimelb.swen30006.metromadness.tracks;

import java.awt.geom.Point2D.Float;

import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.unimelb.swen30006.metromadness.trains.Train;

public class DualTrack extends Track {

	public boolean forwardOccupied;
	public boolean backwardOccupied;
	
	public DualTrack(Float start, Float end, Color col) {
		super(start, end, col);
		this.forwardOccupied = false;
		this.backwardOccupied = false;
	}
	
	public void render(ShapeRenderer renderer){
		renderer.rectLine(startPos.x, startPos.y, endPos.x, endPos.y, LINE_WIDTH);
		renderer.setColor(new Color(245f/255f,245f/255f,245f/255f,0.5f).lerp(this.trackColour, 0.5f));
		renderer.rectLine(startPos.x, startPos.y, endPos.x, endPos.y, LINE_WIDTH/3);
		renderer.setColor(this.trackColour);
	}
	
	@Override
	public void enter(Train t){
		if(t.forward){
			this.forwardOccupied = true;
		} else {
			this.backwardOccupied = true;
		}
	}

	@Override
	public boolean canEnter(boolean forward) {
		if(forward){
			return !this.forwardOccupied;
		} else {
			return !this.backwardOccupied;
		}
	}

	@Override
	public void leave(Train t) {
		if(t.forward){
			this.forwardOccupied = false;
		} else {
			this.backwardOccupied = false;
		}
	}
	
	
	
	
	


}
