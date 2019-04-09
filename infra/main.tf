data "aws_vpc" "default"{
  default = true
}

data "aws_subnet_ids" "all"{
  vpc_id = "${data.aws_vpc.default.id}"
}

data "aws_availability_zones" "all" {
  
}

#--------------------------------------------------------
# CREATE A LOAD BALANCER AND TARGET GROUP
#
#
#--------------------------------------------------------
resource "aws_lb" "EAD-CA-LOADBALANCER" {
  name                = "${var.KEY_NAME}-loadbalancer"
  internal            = false
  load_balancer_type  = "application"
  subnets             = ["${data.aws_subnet_ids.all.ids}"]
  security_groups     = ["${aws_security_group.EAD-CA-SECURITYGROUP-LOADBALANCER.id}"]
  idle_timeout        = "60"

  tags = {
    Name              = "${var.KEY_NAME}-loadbalancer"
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }

}

resource "aws_lb_target_group" "EAD-CA-TARGETGRP" {
  name                = "${var.KEY_NAME}-targetgroup"
  port                = "${var.PORT_HTTP}"
  protocol            = "${var.PROTOCOL_HTTP}"
   
  vpc_id              = "${data.aws_vpc.default.id}"
  target_type         = "instance"
  
  
  health_check {
    healthy_threshold   = 5 # Number of consecutive passing checks for Healthy 
    unhealthy_threshold = 2 # Number of consecutive failing checks for UnHealthy
    timeout             = 5 # Time in Seconds that no-response equals UnHealthy
    interval            = 30 # Time Between Health Checks on an instance
    protocol            = "${var.PROTOCOL_HTTP}"
    matcher             = "200" # Codes to indicate a successful responce
  }

  tags = {
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }
}

resource "aws_lb_listener" "EAD-CA-LB-LISTENER" {
  load_balancer_arn   = "${aws_lb.EAD-CA-LOADBALANCER.arn}"
  port                = "${var.PORT_HTTP}"
  protocol            = "${var.PROTOCOL_HTTP}"

  default_action {
    target_group_arn  = "${aws_lb_target_group.EAD-CA-TARGETGRP.arn}"
    type              = "forward"
  }
}

#--------------------------------------------------------
# CREATE A AUTO SCALE GROUP & LAUNCH CONFIGURATION
#
#
#--------------------------------------------------------

resource "aws_autoscaling_group" "EAD-CA-AUTOSCALEGRP" {
  name                      = "${var.KEY_NAME}-autoscalegroup"

  launch_configuration      = "${aws_launch_configuration.EAD-CA-LAUNCH-CONFIG.id}"
  availability_zones        = ["${data.aws_availability_zones.all.names}"]

  vpc_zone_identifier       = ["${data.aws_subnet_ids.all.ids}"]

  min_size                  = "${var.NUMBER_OF_INSTANCES}"
  max_size                  = "${var.NUMBER_OF_INSTANCES}"
  desired_capacity          = "${var.NUMBER_OF_INSTANCES}"

  health_check_type         = "ELB"
  health_check_grace_period = "300"
  default_cooldown          = "60"

  target_group_arns         = ["${aws_lb_target_group.EAD-CA-TARGETGRP.arn}"]
  

  tags = {
    key                     = "Name"
    value                   = "${var.KEY_NAME}-WebServer"
    propagate_at_launch     = true
  }
}

resource "aws_autoscaling_attachment" "EAD-CA-AUTOSCALE-ATTACH" {
  
  alb_target_group_arn       = "${aws_lb_target_group.EAD-CA-TARGETGRP.arn}"
  autoscaling_group_name     = "${aws_autoscaling_group.EAD-CA-AUTOSCALEGRP.id}"

}

resource "aws_launch_configuration" "EAD-CA-LAUNCH-CONFIG" {
  name              = "${var.KEY_NAME}-launchconfigurator"
  image_id          = "${var.AMI}"
  instance_type     = "${var.INSTANCE_TYPE}"
  security_groups   = ["${aws_security_group.EAD-CA-SECURITYGROUP-AUTOSCALE.id}"]
  
  root_block_device {
    volume_type = "standard"
    volume_size = "80"
  }

  ephemeral_block_device {
    device_name = "/dev/xvdg"
    virtual_name = "ephemeral0"
  }


  lifecycle {
    create_before_destroy = true
  }
}

#--------------------------------------------------------
# CREATE A SECURITY GROUP
#
#
#--------------------------------------------------------
resource "aws_security_group" "EAD-CA-SECURITYGROUP-AUTOSCALE" {
  name                = "${var.KEY_NAME}-securitygrp-autoscalegrp"
  description         = "Allow HTTP and SSL Traffic to the instances in autoscale group"
  vpc_id              = "${data.aws_vpc.default.id}"

  ingress {
    from_port         = 80
    to_port           = 80
    protocol          = "TCP"
    cidr_blocks       = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port         = 22
    to_port           = 22
    protocol          = "TCP"
    cidr_blocks       = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_security_group" "EAD-CA-SECURITYGROUP-LOADBALANCER" {
  name                = "${var.KEY_NAME}-securitygrp-loadbalancer"
  description         = "Allow HTTP Traffic to the Load Balancer Only"
  vpc_id              = "${data.aws_vpc.default.id}"

  ingress {
    from_port         = 80
    to_port           = 80
    protocol          = "TCP"
    cidr_blocks       = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }

  lifecycle {
    create_before_destroy = true
  }

}

#--------------------------------------------------------
# CREATE A SNS TOPIC RESOURCES
#
#
#--------------------------------------------------------
resource "aws_sns_topic" "EAD-CA-SNS-TOPIC-TESTRESULT" {
  name                = "${var.KEY_NAME}-test-results-notify"
  display_name        = "${var.KEY_NAME} Test Results Notificiation"
}

resource "aws_sns_topic_subscription" "EAD-CA-SNS-SUBSCRIPTION-TESTRESULT" {
  topic_arn               = "${aws_sns_topic.EAD-CA-SNS-TOPIC-TESTRESULT.arn}"
  protocol                = "sms"
  endpoint                = "${var.CA_AUTHOR_PHONE}"
  endpoint_auto_confirms  = true
}
