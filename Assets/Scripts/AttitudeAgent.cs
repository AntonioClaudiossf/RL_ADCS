using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using System.IO;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators; 


public class AttitudeAgent : Agent
{
	
	private AttitudeManager manager;

    public override void Initialize()
    {
        manager = GetComponent<AttitudeManager>();
        manager.SetResetParameteres();   
        
    }
    
    // Initialize Episode
    public override void OnEpisodeBegin()
    {
        manager.SetResetParameteres();
    }
    
    // Collect Observations    
    public override void CollectObservations(VectorSensor sensor)
    {
        this.manager.GetObservations(sensor);
    }
    
    // On Action Received    
    public override void OnActionReceived(ActionBuffers actionBuffers)
    {   
        float reward_obtained = 0;
        this.manager.Act(actionBuffers);
        reward_obtained += manager.ComputeReward();
        SetReward(reward_obtained);
        if(!this.manager.train && reward_obtained == 1) EndEpisode(); 
        if(this.manager.CheckTerminationConditions())   EndEpisode();
    } 
       
    /*public override void Heuristic(in ActionBuffers actionsOut)
    {
        var action = actionsOut.ContinuousActions;
        for(int i=0;i<action.Length;i++){
           if(i==0) action[i] = Input.GetAxis("Base"); 
           else if(i==action.Length-1) action[i] = Input.GetAxis("Gripper");
           else action[i] = Input.GetAxis("Joint"+i.ToString());
        } 
    }*/


}
