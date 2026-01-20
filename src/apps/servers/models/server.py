from django.db import models

class Server(models.Model):
    name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    provider = models.ForeignKey(to='ServerProvider', on_delete=models.SET_NULL, blank=True, null=True, related_name='servers')

    organization = models.ForeignKey(to='users.Organization', on_delete=models.CASCADE, related_name='servers')

    agent_url = models.URLField(blank=True, null=True)
    agent_token = models.CharField(max_length=255, blank=True, null=True)

    # TODO: VPN details

    # TODO: Operating System details (Model???)
    # os_family = models.CharField(max_length=20, choices=[('linux', 'Linux'), ('windows', 'Windows'), ('macos', 'macOS')])
    # os_distribution = models.CharField(max_length=100, blank=True, null=True)
    # os_version = models.CharField(max_length=100, blank=True, null=True)
    # architecture = models.CharField(max_length=50, blank=True, null=True)
    # kernel_version = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Server"
        verbose_name_plural = "Servers"

class ServerIp(models.Model):
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, related_name='ips')
    ip_address = models.GenericIPAddressField()
    is_public = models.BooleanField(default=False)
    ssh_port = models.PositiveIntegerField(default=22)
    label = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} ({self.server.name})"

    class Meta:
        verbose_name = "Server IP"
        verbose_name_plural = "Server IPs"

class ServerUser(models.Model):
    server = models.ForeignKey(to=Server, on_delete=models.CASCADE, related_name='users')
    username = models.CharField(max_length=150)
    allow_ssh = models.BooleanField(default=True)

    public_keys = models.ManyToManyField(to='users.SshPublicKey', blank=True, related_name='server_users')

    def __str__(self):
        return f"{self.username} on {self.server.name}"

    class Meta:
        verbose_name = "Server User"
        verbose_name_plural = "Server Users"