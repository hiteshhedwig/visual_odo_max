
**Structure from motion** - The problem of recovering relative camera poses and three-dimensional (3-D) structure from a set of camera images (calibrated or noncalibrated).
- VO is a particular case of SFM. SFM is more general and tackles the problem of 3-D reconstruction of both the structure and camera poses from sequentially ordered or unordered image sets.

> 	Interesting fact : The problem of estimating a vehicles egomotion from visual input alone started in the early 1980s and was described by moravec [5]. It is interesting to observe thatmost of the early research in vo [5][9] was done for planetary rovers and was motivated by the nasa mars exploration program in the endeavor to provide all-terrain rovers with the capability to measure their 6-degree-of-freedom (dof) motion in the presence of wheel slippage in uneven and rough terrains. The work of moravec stands out not only for presenting the first motion-estimation pipelinewhose main functioning blocks are still used todaybut also for  describing one of the earliest corner detectors (after the first one proposed in 1974 by hannah [10]) which is known today as the moravec corner detector [11], a predecessor of the one proposed by forstner [12] and harris and stephens [3], [82].


"Most of the research done in VO has been produced using stereo cameras"

-> "Keyframe selection is a very important step in VO and should always be done before updating the motion"

So far in common that the 3-D points are triangulated for every stereo pair, and the relative motion is solved as a 3-D-to-3-D point registration (alignment) problem. A completely different approach was proposed in 2004 by Nister et al.. Their paper is known not only for coining the term VO but also for providing the first real-time long-run implementation with a robust outlier rejection scheme

Two things Nister did better/improved :
- contrary to all previous works, they did not track features among frame but detected features (Harris corners) independently in all frames and only allowed matches between features. This has the benefit of avoiding feature drift during cross-correlation-based tracking.
- they did not compute the relative motion as a 3-D-to-3-D point registration problem but as a 3-D-to-two-dimensional (2-D) camera-pose estimation problem (these methods are described in the “Motion Estimation” section). Finally, they incorporated RANSAC outlier rejection into the motion estimation step.


## Reducing the Drift

Since VO works by computing the camera path incrementally (pose after pose), the errors introduced by each new frame-to-frame motion accumulate over time. This generates a drift of the estimated trajectory from the real path. For some applications, it is of utmost importance to keep drift as small as possible, which can be done through local optimization over the last m camera poses. This approach—called *sliding window bundle adjustment or windowed bundle adjustmen*t.


>VO is only concerned with the local consistency of the trajectory, whereas SLAM with the global consistency


