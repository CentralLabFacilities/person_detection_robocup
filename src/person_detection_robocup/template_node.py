#!/usr/bin/env python3

import rospy
import os
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clf_person_recognition_msgs.srv import (
    SetPersonTemplate,
    SetPersonTemplateRequest,
    SetPersonTemplateResponse,
)
import rospkg


def call_template_image_service():
    """
    Calls the 'template_image_upload_service' service with an image loaded from disk.
    """
    rospy.wait_for_service("/robocup_tracker/set_template")

    try:
        # Initialize ROS node
        rospy.init_node("template_image_client_node")

        # Get the package path
        rospack = rospkg.RosPack()
        package_path = rospack.get_path("person_detection_robocup")

        # Construct the image path
        # template_img_path = os.path.join(package_path, "templates", "dude3.png")
        template_img_path = os.path.join(package_path, "templates", "letemplate.png")

        # Load the image using OpenCV
        image = cv2.imread(template_img_path, cv2.IMREAD_COLOR)

        if image is None:
            rospy.logerr(f"Failed to load image from: {template_img_path}")
            return

        rospy.loginfo("Image loaded successfully!")

        # Convert the image to a ROS Image message
        bridge = CvBridge()
        ros_image = bridge.cv2_to_imgmsg(image, encoding="bgr8")

        # Create a service proxy
        template_image_service = rospy.ServiceProxy(
            "/robocup_tracker/set_template", SetPersonTemplate
        )

        # Call the service
        response = template_image_service(ros_image)

        if response.success:
            rospy.loginfo("Service call successful!")
        else:
            rospy.logwarn("Service call failed!")

    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")


if __name__ == "__main__":
    call_template_image_service()
