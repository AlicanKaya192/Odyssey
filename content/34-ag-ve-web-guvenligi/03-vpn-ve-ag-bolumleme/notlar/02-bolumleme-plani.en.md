The questions to ask when you start splitting a network, and a small
example plan.

## Step by step

1. **List the assets:** which devices and servers are there, and which are
   the most valuable (the database, backups, management interfaces)?
2. **Split into zones:** devices with the same level of trust and the same
   job go in the same zone. What serves the internet goes in the DMZ,
   guests in a separate zone.
3. **Write down the flows:** which zone has to talk to which zone, **on
   which port**? Every line should have a reason.
4. **Deny by default:** every flow not in the list is closed.
5. **Watch:** refused attempts between zones are logged; a staff computer
   scanning in the server zone is an incident.

## Example plan

| Zone | Network | Who |
|---|---|---|
| DMZ | `10.10.0.0/24` | Web server |
| Servers | `10.20.0.0/24` | Database |
| Staff | `10.30.0.0/24` | Laptops |
| Guest | `10.99.0.0/24` | Visitors |

| Source | Destination | Port | Reason |
|---|---|---|---|
| Internet | DMZ | 443 | The website |
| DMZ | Servers | 5432 | The web server reads the database |
| Staff | DMZ | 443 | Internal users open the site too |
| Guest | Internet | 80, 443 | Internet only |

Everything else is refused. There is no path from the internet to the
servers or from guests to staff.

## Common mistakes

- **Zones but no rules:** the networks are separated but the firewall
  between them says "allow everything". The segmentation stays on paper.
- **A management interface open to everyone:** the management page of the
  printer or the camera can be reached from every zone.
- **Backups in the same zone:** when the attacker reaches the servers, they
  reach the backups too.
- **Everything open to whoever comes over the VPN:** the VPN is treated as
  a zone; only the needed flows from it as well.
- **The single path is overlooked:** the narrow path (web server →
  database) is the place to protect and watch most.
