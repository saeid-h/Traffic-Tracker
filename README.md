# Traffic Tracker

This is a rough estimation of traffic flow using OpenCV library.
It was tested by Python 3.9 and OpenCV 4.0



# Requirements

Make sure you have installed the following requirements:

- Python3.9
- OpenCV 4.0
- numpy, imutils, argparse

```bash
git clone https://github.com/saeid-h/Traffic-Tracker.git
# If you do not have python3.9, install it. 
# It might be working with other version of Python, but it's not tested before.

# Make virtual environment
virtualenv -p /usr/bin/python3.9 venv
# Activate the environment
source venv/bin/activate
pip install <libraries>

```

# Demo

Try the [main.py]() 

```bash
python main.py --video-file $YOURVIDEO 
```

You may turn off the layer by adding the following switches:

```bash
python main.py --video-file $YOURVIDEO --no-speed-check
```

```bash
python main.py --video-file $YOURVIDEO --no-heatmap
```

```bash
python main.py --video-file $YOURVIDEO --no-car-detection
```

There hyper paramers that you can change them:
```
--blur-window <int>
--threshold <int>
--object-area <int>
--invalid-length <int>
--dilation-kernel <int>
--dilation-iter <int>
--heatmap-threshold <int>
--speed-limit <int>
```

You may also download a sample video [here](https://spaceeco-my.sharepoint.com/personal/ovunc_spacee_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fovunc%5Fspacee%5Fcom%2FDocuments%2Ftraffic%2Emp4&parent=%2Fpersonal%2Fovunc%5Fspacee%5Fcom%2FDocuments&originalPath=aHR0cHM6Ly9zcGFjZWVjby1teS5zaGFyZXBvaW50LmNvbS86djovZy9wZXJzb25hbC9vdnVuY19zcGFjZWVfY29tL0VmNWxMci16NHpkTWtZMUQ5Tl9jYU9zQlYxTjNfUEJzZkg1WUlVT0hyVEdQb1E%5FcnRpbWU9YmE0Z0pnc0oyVWc)

