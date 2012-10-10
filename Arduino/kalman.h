
#ifndef _KALMAN_H_
#define _KALMAN_H_


struct KALDATA {
  float P[2][2];    //covariance matrix.
  float angle;
  float q_bias;    //gyro estimate
  float rate;
  float Pdot[4];
  float err;
};

void kalmanInitState(KALDATA p_kd);

void state_update(
    const float		q_m	/* Pitch gyro measurement */,
    KALDATA p_kd,
    float dt
    
);

void
kalman_update(
    const float		angle_m, //measured angle
    KALDATA p_kd
);


#endif
