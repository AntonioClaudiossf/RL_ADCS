using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;


public class AttitudeManager : MonoBehaviour
{
	readonly float G = 100f;
	//Transform[] ReactionWheel;
	public GameObject Earth;
	public GameObject Satellite;
	public GameObject Frame_setpoint;
	public bool train;
	private bool should_end_episode = false;

	public Quaternion Setpoint_Orientation;
	public Quaternion Actual_quat;
	public int cnt = 0;
	private float threshold = 0.001f;
	private float TorqueRWX = 0.0f;
	private float TorqueRWY = 0.0f;
	private float TorqueRWZ = 0.0f;
	public float q_error;

	Rigidbody satellite;
	
		
    // Start is called before the first frame update
   void Start()
    {
        //ReactionWheel = GameObject.FindGameObjectsWithTag("ReactionWheel");
        InitialVelocity();
        //SetResetParameteres();
    }
    
    private void FixedUpdate()
    {
    	Gravity();
    }
    /*
    void WheelTorque()
    {
    	Vector3 Torque = Vector3.zero;
    	Rigidbody rb_RW = GetComponent<Rigidbody>();
        foreach(Transform wheelTransform in ReactionWheel)
        {
            // Calcula o vetor do centro de massa até a roda de reação
            Vector3 torqueDirection = wheelTransform.position - rb_RW.worldCenterOfMass;

            // Calcula o torque usando o produto cruzado entre o vetor de posição e a direção da roda de reação
            Vector3 torque = Vector3.Cross(torqueDirection.normalized, wheelTransform.up) * torqueAmount;

            // Adiciona o torque total
            totalTorque += torque;
        }

        // Aplica o torque total ao Rigidbody
        rb.AddTorque(totalTorque);
    }*/
    
    public void Gravity()
    {
    	
		float m1 = Earth.GetComponent<Rigidbody>().mass;
		float m2 = Satellite.GetComponent<Rigidbody>().mass;
		float r = Vector3.Distance(Satellite.transform.position,Earth.transform.position);
		Vector3 force = (Earth.transform.position - Satellite.transform.position).normalized*(G*(m1*m2)/(r*r));
		Satellite.GetComponent<Rigidbody>().AddForce(force);
    }
    
    public void InitialVelocity()
    {
		float m2 = Earth.GetComponent<Rigidbody>().mass;
		float r = Vector3.Distance(Earth.transform.position,Satellite.transform.position);
		Satellite.transform.LookAt(Earth.transform);
		Satellite.GetComponent<Rigidbody>().velocity += Satellite.transform.right * Mathf.Sqrt((G*m2)/r);		
    }
    
    public float ComputeReward()
    {
		Quaternion Quat_actual = Satellite.transform.localRotation;
		Quaternion quat_inv = Quaternion.Inverse(Satellite.transform.localRotation);
		
		float alpha_q = 0.5f;	
		float alpha_w = 0.1f	;	
		float prod_int = (Quat_actual.w*Setpoint_Orientation.w + Quat_actual.x*Setpoint_Orientation.x + Quat_actual.y*Setpoint_Orientation.y + Quat_actual.z*Setpoint_Orientation.z);
		float wc_mag = Satellite.GetComponent<Rigidbody>().angularVelocity.magnitude;
		q_error = 1-(prod_int*prod_int);
    	float reward = 0.0f;

    	    	
    	if(train)
    	{
    		if(q_error<threshold)
    		{
    			cnt+=1;
    			return 0.3f;
    		}
    		else
    		{    			
    			reward = -alpha_q*q_error-alpha_w*wc_mag;
				return reward;
    		}
    	}
    	else
    	{
    		if(should_end_episode){
            	should_end_episode = false;
                return 1;
            }
            else{
                return 0;
            }
    	}
    }
    
    public void SetResetParameteres(bool reset_episode = true)
    {
    	cnt = 0;
    	if(reset_episode)
    	{
			//Set initial angular velocity
			float x_vel_init = Random.Range(-0.01f,0.01f);
			float y_vel_init = Random.Range(-0.01f,0.01f);
			float z_vel_init = Random.Range(-0.01f,0.01f);
			Satellite.GetComponent<Rigidbody>().angularVelocity = new Vector3(x_vel_init,y_vel_init,z_vel_init);
			//Set init orientation
			
			float Roll_init  = Random.Range(-180.0f,180.0f);
			float Pitch_init = Random.Range(-90.0f,90.0f);
			float Yaw_init   = Random.Range(-180.0f,180.0f);
			Satellite.transform.localRotation = EulerAnglesToQuaternion(Roll_init,Pitch_init,Yaw_init);
		}
		//Set a Setpoint orientation
		float Roll  = Random.Range(-180.0f,180.0f);
		float Pitch = Random.Range(-90f,90.0f);
		float Yaw   = Random.Range(-180f,180.0f);
		Setpoint_Orientation = EulerAnglesToQuaternion(Roll,Pitch,Yaw);
		Frame_setpoint.transform.localRotation = Setpoint_Orientation;  
    }
    
    public bool CheckTerminationConditions()
    {
    	bool should_end_episode = false;
    	float Wc_x = Mathf.Abs(Satellite.GetComponent<Rigidbody>().angularVelocity.x);
    	float Wc_y = Mathf.Abs(Satellite.GetComponent<Rigidbody>().angularVelocity.y);
    	float Wc_z = Mathf.Abs(Satellite.GetComponent<Rigidbody>().angularVelocity.z);
    	
    	if(cnt==50)
    	{
    		should_end_episode = true;
    		SetResetParameteres(false);
    		cnt=0;
    	}
    	//if(Wc_x>0.5 || Wc_y>0.5 || Wc_z>0.5)should_end_episode = true;
    	//if(Satellite.GetComponent<Rigidbody>().angularVelocity.magnitude>0.1)should_end_episode = true;
    	return should_end_episode;
    } 
    
    public void Act(ActionBuffers actionBuffers)
    {
    	float act2torque = 2f/1000f; //Maximum torque of eacth Reaction Whell 2mN.m
    	TorqueRWX = Mathf.Clamp(actionBuffers.ContinuousActions[0], -1f, 1f)*act2torque;
    	TorqueRWY = Mathf.Clamp(actionBuffers.ContinuousActions[1], -1f, 1f)*act2torque;
    	TorqueRWZ = Mathf.Clamp(actionBuffers.ContinuousActions[2], -1f, 1f)*act2torque;
    	Satellite.GetComponent<Rigidbody>().AddTorque(new Vector3(TorqueRWX,TorqueRWY,TorqueRWZ),ForceMode.Force);
    }
    
    public void GetObservations(VectorSensor sensor)
    {	
		//Torque appliyed
		sensor.AddObservation(TorqueRWX);
    	sensor.AddObservation(TorqueRWY);
    	sensor.AddObservation(TorqueRWZ);
		//Quaterion orientation Satellite 
    	Actual_quat = Satellite.transform.localRotation;
    	sensor.AddObservation(Satellite.transform.localRotation);
    	//Desired orientation Satellite
    	sensor.AddObservation(Setpoint_Orientation);
    	//Angular velocity Satellite
    	sensor.AddObservation(Satellite.GetComponent<Rigidbody>().angularVelocity);
    }
    
    private Quaternion EulerAnglesToQuaternion(float roll, float pitch, float yaw) // roll (x), pitch (y), yaw (z), angles are in degrees
	{
		//Sequence XYZ
		// Abbreviations for the various angular functions
		roll = roll*Mathf.PI/180.0f;
		pitch = pitch*Mathf.PI/180.0f;
		yaw = yaw*Mathf.PI/180.0f;

		float cr = Mathf.Cos(roll * 0.5f);
		float sr = Mathf.Sin(roll * 0.5f);
		float cp = Mathf.Cos(pitch * 0.5f);
		float sp = Mathf.Sin(pitch * 0.5f);
		float cy = Mathf.Cos(yaw * 0.5f);
		float sy = Mathf.Sin(yaw * 0.5f);

		Quaternion q;
		q.w = cr * cp * cy - sr * sp * sy;
		q.x = sr * cp * cy + cr * sp * sy;
		q.y = cr * sp * cy - sr * cp * sy;
		q.z = cr * cp * sy + sr * sp * cy;

		return q;
	}
	
	private Vector3 QuaternionToEulerAngles(Quaternion q) 
	{
		//Sequence XYZ
		float roll;
		float pitch;
		float yaw; 
		// roll (x-axis rotation)
		float sinr_cosp = 2f * (q.w * q.x + q.y * q.z);
		float cosr_cosp = 1f - 2f * (q.x * q.x + q.y * q.y);
		roll = Mathf.Atan2(sinr_cosp, cosr_cosp);

		// pitch (y-axis rotation)
		float sinp = Mathf.Sqrt(1f + 2f * (q.w * q.y - q.x * q.z));
		float cosp = Mathf.Sqrt(1f - 2f * (q.w * q.y - q.x * q.z));
		pitch = 2 * Mathf.Atan2(sinp, cosp) - (Mathf.PI / 2f);

		// yaw (z-axis rotation)
		float siny_cosp = 2f * (q.w * q.z + q.x * q.y);
		float cosy_cosp = 1f - 2f * (q.y * q.y + q.z * q.z);
		yaw = Mathf.Atan2(siny_cosp, cosy_cosp);

		return new Vector3(roll*180.0f/Mathf.PI,pitch*180.0f/Mathf.PI,yaw*180.0f/Mathf.PI);
	}
    
}
