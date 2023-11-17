using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FollowCam : MonoBehaviour
{
    // Start is called before the first frame update
    
    public GameObject target;
    public float moveSpeed;
    public bool teste;
    
    // Update is called once per frame
    void Update()
    {
        if(target != null && teste)
        {
        	transform.LookAt((target.transform.position));
        	transform.position = Vector3.Lerp(transform.position, target.transform.position, Time.deltaTime * moveSpeed);
        }
    }
}
