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
  security_groups     = ["${aws_security_group.EAD-CA-SECURITYGROUP.id}"]
  

  tags = {
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }

}

resource "aws_lb_target_group" "EAD-CA-TARGETGRP" {
  name                = "${var.KEY_NAME}-targettroup"
  port                = 80
  protocol            = "HTTP"
  
  
  vpc_id              = "${data.aws_vpc.default.id}"
  target_type         = "instance"

  
  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    protocol            = "HTTP"
    matcher             = "200"
  }

  tags = {
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }
}

resource "aws_lb_listener" "EAD-CA-LB-LISTENER" {
  load_balancer_arn   = "${aws_lb.EAD-CA-LOADBALANCER.arn}"
  port                = "80"
  protocol            = "HTTP"

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
  name                 = "${var.KEY_NAME}-autoscalegroup"

  launch_configuration = "${aws_launch_configuration.EAD-CA-LAUNCH-CONFIG.id}"
  availability_zones  = ["${data.aws_availability_zones.all.names}"]

  min_size            = "${var.NUMBER_OF_INSTANCES}"
  max_size            = "${var.NUMBER_OF_INSTANCES}"
  desired_capacity    = "${var.NUMBER_OF_INSTANCES}"

  health_check_type   = "ELB"
  health_check_grace_period = "100"

  target_group_arns   = ["${aws_lb_target_group.EAD-CA-TARGETGRP.arn}"]

  tags = {
    key               = "Name"
    value             = "${var.KEY_NAME}-WebServer"
    propagate_at_launch = true
  }
}

resource "aws_launch_configuration" "EAD-CA-LAUNCH-CONFIG" {
  name              = "${var.KEY_NAME}-launchconfigurator"
  image_id          = "${var.AMI}"
  instance_type     = "${var.INSTANCE_TYPE}"
  security_groups   = ["${aws_security_group.EAD-CA-SECURITYGROUP.id}"]
  
  lifecycle {
    create_before_destroy = true
  }
}

#--------------------------------------------------------
# CREATE A SECURITY GROUP
#
#
#--------------------------------------------------------
resource "aws_security_group" "EAD-CA-SECURITYGROUP" {
  name                = "${var.KEY_NAME}-securitygrp"
  description         = "Allow HTTP Traffic for CA"
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

  tags = {
    Author            = "${var.CA_AUTHOR_NAME}"
    Purpose           = "${var.CA_PURPOSE}"
    Environment       = "${var.CA_ENVIRONMENT}"
  }

  lifecycle {
    create_before_destroy = true
  }

}