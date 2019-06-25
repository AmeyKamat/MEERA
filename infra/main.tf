provider "aws" {
  region = "us-east-1"
}

output "meera_public_ip" {
    value               = aws_lightsail_static_ip.meera_static_ip.ip_address
}

resource "aws_lightsail_static_ip_attachment" "meera_static_ip_attachment" {
    static_ip_name      = "${aws_lightsail_static_ip.meera_static_ip.name}"
    instance_name       = "${aws_lightsail_instance.meera_instance.name}"
}


resource "aws_lightsail_static_ip" "meera_static_ip" {
    name                = "meera_static_ip"
}

resource "aws_lightsail_instance" "meera_instance" {
    name                = "meera_instance"
    availability_zone   = "us-east-1a"
    blueprint_id        = "ubuntu_16_04_2"
    bundle_id           = "small_2_0"
    key_pair_name       = "${aws_lightsail_key_pair.meera_key_pair.name}"

    provisioner "remote-exec" {
        inline = [
            "sudo apt install git",
            "cd ~",
            "git clone https://github.com/AmeyKamat/MEERA.git",
            "cd MEERA",
            "sudo chmod +x scripts/create-swapfile.sh",
            "sudo chmod +x setup.sh",
            "sudo chmod +w .env",
            "sudo ./scripts/create-swapfile.sh",
            "sudo ./setup.sh"
        ]
        connection {
            type        = "ssh"
            host        = "${self.public_ip_address}"
            private_key = "${file("meera")}"
            user        = "ubuntu"
            timeout     = "15m"
        }
    }

    provisioner "file" {
        source          = ".env"
        destination     = "/home/ubuntu/MEERA/.env"
        connection {
            type        = "ssh"
            host        = "${self.public_ip_address}"
            user        = "ubuntu"
            private_key = "${file("meera")}"
            timeout     = "20s"
        }
    }

    provisioner "remote-exec" {
        inline = [
            "cd /home/ubuntu/MEERA",
            "screen -S meera_server -dm sudo ./meera.sh deploy server &",
            "sleep 5",
            "screen -S meera_client -dm sudo ./meera.sh deploy telegram-client &",
            "sleep 5"
        ]
        connection {
            type        = "ssh"
            host        = "${self.public_ip_address}"
            private_key = "${file("meera")}"
            user        = "ubuntu"
            timeout     = "50s"
        }
    }

    provisioner "local-exec" {
        command         = "aws lightsail --region 'us-east-1' open-instance-public-ports --instance-name '${self.name}' --port-info fromPort='8000',toPort='8000',protocol='tcp'"
    }
}

resource "aws_lightsail_key_pair" "meera_key_pair" {
    name                = "meera_key_pair"
    public_key          = "${file("meera.pub")}"
}

