using UnityEngine;
using System.Collections;

public class WorldAxis : MonoBehaviour
{
	float size = 1f;
	
	public GameObject Satellite;

	void OnDrawGizmos ()
	{
		Vector3 position = Satellite.transform.position;
		
		Gizmos.color = Color.red;
		Gizmos.matrix = transform.localToWorldMatrix;
		Gizmos.DrawRay(Vector3.zero,new Vector3(5f,0f,0f));

		Gizmos.color = Color.green;
		Gizmos.matrix = transform.localToWorldMatrix;
		Gizmos.DrawRay(Vector3.zero,new Vector3(0f,5f,0f));

		Gizmos.color = Color.blue;
		Gizmos.matrix = transform.localToWorldMatrix;
		Gizmos.DrawRay(Vector3.zero,new Vector3(0f,0f,5f));
	}
}
