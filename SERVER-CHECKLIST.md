# Server Prerequisites Checklist

Run these commands on your server (141.76.16.16) to verify everything is ready for deployment.

## 1. Check Firewall Ports

### Check if ports are open:
```bash
# Check port 80 (HTTP - REQUIRED for Let's Encrypt)
sudo netstat -tlnp | grep :80
# Or
sudo ss -tlnp | grep :80

# Check port 443 (HTTPS)
sudo netstat -tlnp | grep :443
# Or
sudo ss -tlnp | grep :443
```

### Open ports if needed:

**For UFW (Ubuntu/Debian):**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status
```

**For firewalld (RHEL/CentOS):**
```bash
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

**For iptables:**
```bash
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables-save
```

## 2. Test Port Accessibility from Outside

From your **local machine**, test if ports are reachable:

```bash
# Test port 80
telnet 141.76.16.16 80
# Or
curl -I http://141.76.16.16
# Or
nc -zv 141.76.16.16 80

# Test port 443
telnet 141.76.16.16 443
# Or
nc -zv 141.76.16.16 443
```

If these fail, the firewall is blocking traffic.

## 3. Verify DNS

From **any machine**:
```bash
dig habit.wiwi.tu-dresden.de
# Should show: 141.76.16.16

# Or
nslookup habit.wiwi.tu-dresden.de
# Should show: 141.76.16.16
```

## 4. Check Docker is Running

On the **server**:
```bash
docker ps
# Should list running containers

docker --version
# Should show Docker version 20.10+

docker compose version
# Should show Docker Compose v2.0+
```

## 5. Check Nothing is Using Ports 80/443

On the **server**:
```bash
# Check what's listening on port 80
sudo lsof -i :80

# Check what's listening on port 443
sudo lsof -i :443
```

**IMPORTANT:** If something else (like Apache, Nginx, or another Traefik) is already using these ports, you need to stop them first:

```bash
# Stop Apache
sudo systemctl stop apache2

# Stop Nginx
sudo systemctl stop nginx

# Or stop via Portainer if it's another container
```

## 6. Verify Portainer Access

From your **local machine**:
```bash
# Check Portainer is accessible
curl -k https://your-portainer-url:9000
# Or open in browser: https://141.76.16.16:9000
```

---

## Expected Results:

✅ **Port 80:** Open and accessible from internet
✅ **Port 443:** Open and accessible from internet
✅ **DNS:** habit.wiwi.tu-dresden.de → 141.76.16.16
✅ **Docker:** Running on server
✅ **Ports 80/443:** Not in use by other services
✅ **Portainer:** Accessible and working

Once all checks pass, you're ready to deploy via Portainer!

---

## After Deployment - Verify SSL Works

Once deployed via Portainer, check Traefik obtained the certificate:

### In Portainer:
1. Go to **Containers** → **h3-proxy**
2. Click **Logs**
3. Look for:
   ```
   level=info msg="Certificate obtained for domain habit.wiwi.tu-dresden.de"
   ```

### From your local machine:
```bash
# Test HTTPS
curl -I https://habit.wiwi.tu-dresden.de

# Check certificate issuer
echo | openssl s_client -servername habit.wiwi.tu-dresden.de -connect habit.wiwi.tu-dresden.de:443 2>/dev/null | openssl x509 -noout -issuer
# Should show: issuer=C = US, O = Let's Encrypt
```

---

## Troubleshooting

### If SSL certificate fails:

1. **Check Traefik logs in Portainer** for ACME errors
2. **Verify port 80 is accessible** from internet (Let's Encrypt needs this!)
3. **Check DNS is correct** and propagated
4. **Wait a few minutes** - certificate generation can take 1-2 minutes
5. **Check Let's Encrypt status**: https://letsencrypt.status.io/

### Common issues:

- ❌ **Port 80 blocked** → Let's Encrypt can't verify domain
- ❌ **DNS not pointing to server** → Let's Encrypt can't reach your server
- ❌ **Another service using port 80/443** → Traefik can't bind to ports
- ❌ **Rate limit hit** → You've requested too many certificates (50/week limit)

---

## NO CERTBOT NEEDED!

🎉 **Traefik handles everything automatically!**

- No certbot installation
- No manual certificate requests
- No cron jobs for renewal
- No certificate file management

Traefik does it all inside the Docker container!
